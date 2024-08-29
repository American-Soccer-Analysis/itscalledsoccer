import json
from io import StringIO
from logging import getLevelName, getLogger
from typing import Dict, List, Optional, Union

import requests
from cachecontrol import CacheControl
from cachecontrol.heuristics import ExpiresAfter
from pandas import DataFrame, concat, isnull, read_json
from rapidfuzz import fuzz, process


class AmericanSoccerAnalysis:
    """Wrapper around the ASA Shiny API"""

    API_VERSION = "v1"
    BASE_URL = f"https://app.americansocceranalysis.com/api/{API_VERSION}/"
    LEAGUES = ["nwsl", "mls", "uslc", "usl1", "usls", "nasl", "mlsnp"]
    MAX_API_LIMIT = 1000
    LOGGER = getLogger(__name__)

    def __init__(
        self,
        proxies: Optional[dict] = None,
        logging_level: Optional[str] = "WARNING",
        lazy_load: Optional[bool] = True,
    ) -> None:
        """Class constructor

        Args:
            proxies (Optional[dict], optional): A dictionary containing proxy mappings, see https://docs.python-requests.org/en/latest/user/advanced/#proxies. Defaults to None.
            logging_level (Optional[str], optional): A string representing the logging level of the logger. Defaults to "WARNING".
            lazy_load (Optional[bool], optional): A boolean indicating whether to lazy load all entity data on initialization. Defaults to True.
        """
        SESSION = requests.session()
        if proxies:
            SESSION.proxies.update(proxies)
        CACHE_SESSION = CacheControl(SESSION, heuristic=ExpiresAfter(days=1))

        if logging_level:
            if logging_level.upper() in [
                "DEBUG",
                "INFO",
                "WARNING",
                "ERROR",
                "CRITICAL",
            ]:
                self.LOGGER.setLevel(getLevelName(logging_level.upper()))
            else:
                self.LOGGER.info(f"Logging level {logging_level} not recognized!")

        self.session = CACHE_SESSION
        self.base_url = self.BASE_URL
        self.lazy_load = lazy_load

        self.players: DataFrame = None
        self.teams: DataFrame = None
        self.stadia: DataFrame = None
        self.managers: DataFrame = None
        self.referees: DataFrame = None

        if self.lazy_load:
            self.LOGGER.info(
                "Lazy loading enabled. Initializing client without entity data."
            )
        else:
            self.LOGGER.info(
                "Lazy loading disabled. Initializing client with entity data."
            )
            self.players = self._get_entity("player")
            self.teams = self._get_entity("team")
            self.stadia = self._get_entity("stadia")
            self.managers = self._get_entity("manager")
            self.referees = self._get_entity("referee")
        self.LOGGER.info("Finished initializing client")

    def _get_entity(self, type: str) -> DataFrame:
        """Gets all the data for a specific type and
        stores it in a DataFrame.

        Args:
            type (str): type of data to get

        Returns:
            DataFrame: _description_
        """
        plural_type = f"{type}s" if type != "stadia" else f"{type}"
        self.LOGGER.info(f"Gathering all {plural_type}")
        df = DataFrame([])
        for league in self.LEAGUES:
            url = f"{self.BASE_URL}{league}/{plural_type}"
            resp_df = self._execute_query(url, {})
            resp_df = resp_df.assign(competition=league)
            df = concat([df, resp_df], ignore_index=True)
        return df

    def _convert_name_to_id(self, type: str, name: str) -> str:
        """Converts the name of a player, manager, stadium, referee or team
        to their corresponding id.

        Args:
            type (str): type of name to convert
            name (str): name

        Returns:
          str: the matched id
        """
        min_score = 70

        if type == "player":
            lookup = self.players
            names = self.players["player_name"].to_list()
        elif type == "manager":
            lookup = self.managers
            names = self.managers["manager_name"].to_list()
        elif type == "stadium":
            lookup = self.stadia
            names = self.stadia["stadium_name"].to_list()
        elif type == "referee":
            lookup = self.referees
            names = self.referees["referee_name"].to_list()
        elif type == "team":
            lookup = self.teams
            names = self.teams["team_name"].to_list()

        # Getting back nan from the API for some names
        names = [n for n in names if isnull(n) is False]

        matches = process.extractOne(name, names, scorer=fuzz.partial_ratio)
        if matches:
            if matches[1] >= min_score:
                name = matches[0]
            else:
                self.LOGGER.info(f"No match found for {name} due to score")
                return ""
        else:
            self.LOGGER.info(f"No match found for {name}")
            return ""
        matched_id = lookup.loc[lookup[f"{type}_name"] == name, f"{type}_id"].iloc[0]
        return matched_id

    def _convert_names_to_ids(
        self, type: str, names: Union[str, List[str]]
    ) -> Union[str, List[str], None]:
        """Converts a name or list of names to an id or list of ids

        Args:
            type (str): type of name
            names (str,List[str]): a name or list of names

        Returns:
            str or List[str]: the matched ids
        """
        ids: List[str] = []
        if names is None:
            return None
        if isinstance(names, str):
            return self._convert_name_to_id(type, names)
        else:
            for n in names:
                ids.append(self._convert_name_to_id(type, n))
            return ids

    def _check_leagues(self, leagues: Union[str, List[str], None]) -> None:
        """Validates the leagues parameter

        Args:
            leagues (str, List[str], None): league abbreviation or list of league abbreviations
        """
        if leagues:
            if isinstance(leagues, list):
                for league in leagues:
                    if league not in self.LEAGUES:
                        self.LOGGER.info(
                            f"Leagues are limited only to the following options: {self.LEAGUES}."
                        )
                        raise SystemExit(1)
            else:
                if leagues not in self.LEAGUES:
                    self.LOGGER.info(
                        f"Leagues are limited only to the following options: {self.LEAGUES}."
                    )
                    raise SystemExit(1)

    def _check_leagues_salaries(self, leagues: Union[str, List[str], None]) -> None:
        """Validates the leagues parameter for salary searches

        Args:
            leagues (str, List[str], None): league abbreviation or list of league abbreviations
        """
        if leagues:
            if isinstance(leagues, list):
                if any([x != "mls" for x in leagues]):
                    self.LOGGER.info("Only MLS salary data is publicly available.")
                    raise SystemExit(1)
            else:
                if leagues != "mls":
                    self.LOGGER.info("Only MLS salary data is publicly available.")
                    raise SystemExit(1)

    def _check_ids_names(
        self, ids: Union[str, List[str], None], names: Union[str, List[str], None]
    ) -> None:
        """Makes sure only ids or names are passed to a function and verifies
        they are the right data type.

        Args:
            ids (str, List[str], None): a single id or list of ids
            names (str, List[str], None): a single name or list of names
        """
        if ids and names:
            self.LOGGER.info("Please specify only IDs or names, not both.")
            raise SystemExit(1)

        if ids:
            if not isinstance(ids, str) and not isinstance(ids, list):
                self.LOGGER.info("IDs must be passed as a string or list of strings.")
                raise SystemExit(1)

        if names:
            if not isinstance(names, str) and not isinstance(names, list):
                self.LOGGER.info("Names must be passed as a string or list of names.")
                raise SystemExit(1)

    def _filter_entity(
        self,
        entity_all: DataFrame,
        entity_type: str,
        leagues: Union[str, List[str], None],
        ids: Union[str, List[str], None] = None,
        names: Union[str, List[str], None] = None,
    ) -> DataFrame:
        """Filters a DataFrame based on the arguments given.

        Args:
            entity_all (DataFrame): a DataFrame containing the complete set of data
            entity_type (str): the type of data
            leagues (Union[str, List[str], None]): league abbreviation or list of league abbreviations
            ids (str, List[str], None): a single id or list of ids
            names (str, List[str], None): a single name or list of names
        Returns:
            DataFrame
        """
        self._check_leagues(leagues)
        self._check_ids_names(ids, names)

        entity = entity_all

        if names:
            converted_ids = self._convert_names_to_ids(entity_type, names)
        else:
            converted_ids = ids

        if isinstance(leagues, str):
            leagues = [leagues]
        if isinstance(converted_ids, str):
            converted_ids = [converted_ids]

        if leagues:
            entity = entity[entity["competition"].isin(leagues)]

        if converted_ids:
            entity = entity[entity[f"{entity_type}_id"].isin(converted_ids)]

        return entity

    def _execute_query(
        self, url: str, params: Dict[str, Union[str, List[str], None]]
    ) -> DataFrame:
        """Executes a query while handling the max number of responses from the API

        Args:
            url (str): the API endpoint to call
            params (Dict[str, Union[str, List[str], None]): URL query strings

        Returns:
            DataFrame
        """
        for k, v in params.items():
            if isinstance(v, list):
                params[k] = ",".join(v)

        temp_response = self._single_request(url, params)
        response = temp_response

        if isinstance(response, DataFrame):
            offset = self.MAX_API_LIMIT

            while len(temp_response.index) == self.MAX_API_LIMIT:
                params["offset"] = str(offset)
                temp_response = self._single_request(url, params)
                response = concat([response, temp_response], ignore_index=True)
                offset = offset + self.MAX_API_LIMIT

        return response

    def _single_request(
        self, url: str, params: Dict[str, Union[str, List[str], None]]
    ) -> DataFrame:
        """Handles single call to the API

        Args:
            url (str): the API endpoint to call
            params (Dict[str, Union[str, List[str], None]): URL query strings

        Returns:
            DataFrame
        """
        response = self.session.get(url=url, params=params)
        response.raise_for_status()
        resp_df = read_json(StringIO(json.dumps(response.json())))
        return resp_df

    def _get_stats(
        self, leagues: Union[str, List[str]], type: str, entity: str, **kwargs
    ) -> DataFrame:
        """Handles calls to stats APIs

        Args:
            type (str): the API endpoint to call
            entity (str): URL query strings
            leagues (str, List[str], None): league abbreviation or list of league abbreviations

        Keyword Args:
            split_by_teams (bool): Logical indicator to group results by team.
            split_by_seasons (bool): Logical indicator to group results by season.
            split_by_positions (bool): Logical indicator to group results by positions. Results must be grouped by at least one of teams, positions, or seasons.
            player_ids (Union[str, List[str]]): Player IDs on which to filter. Cannot be combined with player_names. Accepts a string or list of strings.
            player_names (Union[str, List[str]]): Player names on which to filter. Partial matches are accepted. Cannot be combined with player_ids. Accepts a string or list of strings.
            team_ids (Union[str, List[str]]): Team IDs on which to filter. Cannot be combined with team_names. Accepts a string or list of strings.
            team_names (Union[str, List[str]]): Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with team_ids. Accepts a string or list of strings.
            game_ids (Union[str, List[str]]): Game IDs on which to filter. Accepts a string or list of strings.

        Returns:
            DataFrame
        """
        self.LOGGER.info(f"get_stats called with {locals()}")
        if type == "salaries":
            self._check_leagues_salaries(leagues)
            if (
                entity == "teams"
                and kwargs.get("split_by_teams", None)
                and kwargs.get("split_by_seasons", None)
                and kwargs.get("split_by_positions", None)
            ):
                kwargs["split_by_teams"] = True
        else:
            self._check_leagues(leagues)

        keys_string = ",".join(list(kwargs.keys()))

        if "player_" in keys_string:
            self._check_ids_names(
                kwargs.get("player_ids", None), kwargs.get("player_names", None)
            )

            if kwargs.get("player_names", None):
                kwargs["player_id"] = self._convert_names_to_ids(
                    "player", kwargs["player_names"]
                )
                kwargs.pop("player_names")
            else:
                kwargs["player_id"] = kwargs["player_ids"]
                kwargs.pop("player_ids")

        if "team_" in keys_string:
            self._check_ids_names(
                kwargs.get("team_ids", None), kwargs.get("team_names", None)
            )

            if kwargs.get("team_names", None):
                kwargs["team_id"] = self._convert_names_to_ids(
                    "team", kwargs["team_names"]
                )
                kwargs.pop("team_names")
            else:
                kwargs["team_id"] = kwargs["team_ids"]
                kwargs.pop("team_ids")

        if kwargs.get("game_ids", None):
            kwargs["game_id"] = kwargs["game_ids"]
            kwargs.pop("game_ids")

        stats = DataFrame([])
        if isinstance(leagues, str):
            url = f"{self.base_url}{leagues}/{entity}/{type}"
            response = self._execute_query(url, kwargs)

            stats = response
        elif isinstance(leagues, list):
            for league in leagues:
                url = f"{self.base_url}{league}/{entity}/{type}"

                response = self._execute_query(url, kwargs)

                stats = concat([stats, response])

        return stats

    def get_stadia(
        self,
        leagues: Union[str, List[str], None] = None,
        ids: Union[str, List[str], None] = None,
        names: Union[str, List[str], None] = None,
    ) -> DataFrame:
        """Get information associated with stadia

        Args:
            leagues (Union[str, List[str], None], optional): league abbreviation or list of league abbreviations. Defaults to None.
            ids (Union[str, List[str], None], optional): a single id or list of ids. Defaults to None.
            names (Union[str, List[str], None], optional): a single name or list of names. Defaults to None.

        Returns:
            DataFrame
        """
        if self.stadia is None:
            self.stadia = self._get_entity("stadia")
        stadia = self._filter_entity(self.stadia, "stadia", leagues, ids, names)
        return stadia

    def get_referees(
        self,
        leagues: Union[str, List[str], None] = None,
        ids: Union[str, List[str], None] = None,
        names: Union[str, List[str], None] = None,
    ) -> DataFrame:
        """Get information associated with referees

        Args:
            leagues (Union[str, List[str], None], optional): league abbreviation or a list of league abbreviations. Defaults to None.
            ids (Union[str, List[str], None], optional): a single referee id or a list of referee ids. Defaults to None.
            names (Union[str, List[str], None], optional): a single referee name or a list of referee names. Defaults to None.

        Returns:
            DataFrame
        """
        if self.referees is None:
            self.referees = self._get_entity("referee")
        referees = self._filter_entity(self.referees, "referee", leagues, ids, names)
        return referees

    def get_managers(
        self,
        leagues: Union[str, List[str], None] = None,
        ids: Union[str, List[str], None] = None,
        names: Union[str, List[str], None] = None,
    ) -> DataFrame:
        """Get information associated with managers

        Args:
            leagues (Union[str, List[str], None], optional): league abbreviation or a list of league abbreviations. Defaults to None.
            ids (Union[str, List[str], None], optional): a single manager id or a list of manager ids. Defaults to None.
            names (Union[str, List[str], None], optional): a single manager name or a list of manager names. Defaults to None.

        Returns:
            DataFrame_
        """
        if self.managers is None:
            self.managers = self._get_entity("manager")
        managers = self._filter_entity(self.managers, "manager", leagues, ids, names)
        return managers

    def get_teams(
        self,
        leagues: Union[str, List[str], None] = None,
        ids: Union[str, List[str], None] = None,
        names: Union[str, List[str], None] = None,
    ) -> DataFrame:
        """Get information associated with teams

        Args:
            leagues (Union[str, List[str], None], optional): league abbreviation or a list of league abbreviations. Defaults to None.
            ids (Union[str, List[str], None], optional): a single team id or a list of team ids. Defaults to None.
            names (Union[str, List[str], None], optional): a single team name or a list of team names. Defaults to None.

        Returns:
            DataFrame_
        """
        if self.teams is None:
            self.teams = self._get_entity("team")
        teams = self._filter_entity(self.teams, "team", leagues, ids, names)
        return teams

    def get_players(
        self,
        leagues: Union[str, List[str], None] = None,
        ids: Union[str, List[str], None] = None,
        names: Union[str, List[str], None] = None,
    ) -> DataFrame:
        """Get information associated with players

        Args:
            leagues (Union[str, List[str], None], optional): league abbreviation or a list of league abbreviations. Defaults to None.
            ids (Union[str, List[str], None], optional): a single player id or a list of player ids. Defaults to None.
            names (Union[str, List[str], None], optional): a single player name or a list of player names. Defaults to None.

        Returns:
            DataFrame_
        """
        if self.players is None:
            self.players = self._get_entity("player")
        players = self._filter_entity(self.players, "player", leagues, ids, names)
        return players

    def get_games(
        self,
        leagues: Union[str, List[str], None] = None,
        game_ids: Union[str, List[str], None] = None,
        team_ids: Union[str, List[str], None] = None,
        team_names: Union[str, List[str], None] = None,
        seasons: Union[str, List[str], None] = None,
        stages: Union[str, List[str], None] = None,
    ) -> DataFrame:
        """Get information related to games

        Args:
            leagues (Union[str, List[str], None], optional): league abbreviation or a list of league abbreviations. Defaults to None.
            game_ids (Union[str, List[str], None], optional): a single game id or a list of game ids. Defaults to None.
            team_ids (Union[str, List[str], None], optional): a single team id or a list of team ids. Defaults to None.
            team_names (Union[str, List[str], None], optional): a single team name or a list of team names. Defaults to None.
            seasons (Union[str, List[str], None], optional): a single year of a league season or a list of years. Defaults to None.
            stages (Union[str, List[str], None], optional): a single stage of competition in which a game took place or list of stages. Defaults to None.

        Returns:
            DataFrame_
        """
        self._check_leagues(leagues)
        self._check_ids_names(team_ids, team_names)

        query: Dict[str, Union[str, List[str], None]] = {}

        if game_ids:
            query["game_id"] = game_ids
        if team_names:
            query["team_id"] = self._convert_names_to_ids("team", team_names)
        if team_ids:
            query["team_id"] = team_ids
        if seasons:
            query["season_name"] = seasons
        if stages:
            query["stage_name"] = stages
        if not leagues:
            leagues = self.LEAGUES

        games = DataFrame([])
        if isinstance(leagues, str):
            games_url = f"{self.base_url}{leagues}/games"
            response = self._execute_query(games_url, query)

            games = response
        elif isinstance(leagues, list):
            for league in leagues:
                games_url = f"{self.base_url}{league}/games"
                response = self._execute_query(games_url, query)

                games = concat([games, response])

        return games.sort_values(by=["date_time_utc"], ascending=False)

    def get_player_xgoals(
        self, leagues: Union[str, List[str]] = LEAGUES, **kwargs
    ) -> DataFrame:
        """Retrieves a DataFrame containing player xG data meeting the specified conditions.

        Args:
            leagues (Union[str, List[str]], optional): League(s) on which to filter. Accepts a string or list of strings.

        Keyword Args:
            minimum_minutes (int): Minimum threshold for sum of minutes played.
            minimum_shots (int): Minimum threshold for sum of shots.
            minimum_key_passes (int): Minimum threshold for sum of key passes.
            player_ids (Union[str, List[str]]): Player IDs on which to filter. Cannot be combined with player_names. Accepts a string or list of strings.
            player_names (Union[str, List[str]]): Player names on which to filter. Partial matches are accepted. Cannot be combined with player_ids. Accepts a string or list of strings.
            team_ids (Union[str, List[str]]): Team IDs on which to filter. Cannot be combined with team_names. Accepts a string or list of strings.
            team_names (Union[str, List[str]]): Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with team_ids. Accepts a string or list of strings.
            season_name (Union[str, List[str]]): Name(s)/year(s) of seasons. Cannot be combined with a date range. Accepts a string or list of strings.
            start_date (str): Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            end_date (str): End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            shot_pattern (Union[str, List[str]]): Describes the possessing actions leading to the shot. Valid keywords include: 'Set piece', 'Corner', 'Free kick', 'Penalty', 'Fastbreak', and 'Regular'. Accepts a string or list of strings.
            split_by_teams (bool): Logical indicator to group results by team.
            split_by_seasons (bool): Logical indicator to group results by season.
            split_by_games (bool): Logical indicator to group results by game.
            stage_name (Union[str, List[str]]): Describes the stage of competition in which a game took place. Accepts a string or list of strings.
            general_position (Union[str, List[str]]): Describes the most common position played by each player over the specified period of time. Valid keywords include: 'GK', 'CB', 'FB', 'DM', 'CM', 'AM', 'W', and 'ST'. Accepts a string or list of strings.

        Returns:
            DataFrame
        """
        player_xgoals = self._get_stats(
            leagues, type="xgoals", entity="players", **kwargs
        )
        return player_xgoals

    def get_player_xpass(
        self, leagues: Union[str, List[str]] = LEAGUES, **kwargs
    ) -> DataFrame:
        """Retrieves a DataFrame containing player xPass data meeting the specified conditions.

        Args:
            leagues (Union[str, List[str]], optional): League(s) on which to filter. Accepts a string or list of strings. Defaults to LEAGUES.

        Keyword Args:
            minimum_minutes (int): Minimum threshold for sum of minutes played.
            minimum_passes (int): Minimum threshold for sum of attempted passes.
            player_ids (Union[str, List[str]]): Player IDs on which to filter. Cannot be combined with player_names. Accepts a string or list of strings.
            player_names (Union[str, List[str]]): Player names on which to filter. Partial matches are accepted. Cannot be combined with player_ids. Accepts a string or list of strings.
            team_ids (Union[str, List[str]]): Team IDs on which to filter. Cannot be combined with team_names. Accepts a string or list of strings.
            team_names (Union[str, List[str]]): Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with team_ids. Accepts a string or list of strings.
            season_name (Union[str, List[str]]): Name(s)/year(s) of seasons. Cannot be combined with a date range. Accepts a string or list of strings.
            start_date (str): Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            end_date (str): End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            pass_origin_third (Union[str, List[str]]): Describes the third of the field from which the pass originated. Valid keywords include: 'Attacking', 'Middle', and 'Defensive'. Accepts a string or list of strings.
            split_by_teams (bool): Logical indicator to group results by team.
            split_by_seasons (bool): Logical indicator to group results by season.
            split_by_games (bool): Logical indicator to group results by game.
            stage_name (Union[str, List[str]]): Describes the stage of competition in which a game took place. Accepts a string or list of strings.
            general_position (Union[str, List[str]]): Describes the most common position played by each player over the specified period of time. Valid keywords include: 'GK', 'CB', 'FB', 'DM', 'CM', 'AM', 'W', and 'ST'. Accepts a string or list of strings.

        Returns:
            DataFrame
        """
        player_xpass = self._get_stats(
            leagues, type="xpass", entity="players", **kwargs
        )
        return player_xpass

    def get_player_goals_added(
        self, leagues: Union[str, List[str]] = LEAGUES, **kwargs
    ) -> DataFrame:
        """Retrieves a DataFrame containing player g+ data meeting the specified conditions.

        Args:
            leagues (Union[str, List[str]], optional): League(s) on which to filter. Accepts a string or list of strings. Defaults to LEAGUES.

        Keyword Args:
            minimum_minutes (int): Minimum threshold for sum of minutes played.
            player_ids (Union[str, List[str]]): Player IDs on which to filter. Cannot be combined with player_names. Accepts a string or list of strings.
            player_names (Union[str, List[str]]): Player names on which to filter. Partial matches are accepted. Cannot be combined with player_ids. Accepts a string or list of strings.
            team_ids (Union[str, List[str]]): Team IDs on which to filter. Cannot be combined with team_names. Accepts a string or list of strings.
            team_names (Union[str, List[str]]): Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with team_ids. Accepts a string or list of strings.
            season_name (Union[str, List[str]]): Name(s)/year(s) of seasons. Cannot be combined with a date range. Accepts a string or list of strings.
            start_date (str): Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            end_date (str): End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            split_by_teams (bool): Logical indicator to group results by team.
            split_by_seasons (bool): Logical indicator to group results by season.
            split_by_games (bool): Logical indicator to group results by game.
            stage_name (Union[str, List[str]]): Describes the stage of competition in which a game took place. Accepts a string or list of strings.
            action_type (Union[str, List[str]]): Describes the goals added (g+) action type. Valid keywords include: 'Dribbling', 'Fouling', 'Interrupting', 'Passing', 'Receiving', and 'Shooting'. Accepts a string or list of strings.
            general_position (Union[str, List[str]]): Describes the most common position played by each player over the specified period of time. Valid keywords include: 'GK', 'CB', 'FB', 'DM', 'CM', 'AM', 'W', and 'ST'. Accepts a string or list of strings.
            above_replacement (bool): Logical indicator to compare players against replacement-level values. This will only return aggregated g+ values, rather than disaggregated g+ values by action type.

        Returns:
            DataFrame
        """
        player_goals_added = self._get_stats(
            leagues, type="goals-added", entity="players", **kwargs
        )
        return player_goals_added

    def get_player_salaries(
        self, leagues: Union[str, List[str]] = "mls", **kwargs
    ) -> DataFrame:
        """Retrieves a DataFrame containing player salary data meeting the specified conditions

        Args:
            leagues (Union[str, List[str]], optional): Leagues on which to filter. Accepts a string or list of strings. Defaults to 'mls'.

        Keyword Args:
            player_ids (Union[str, List[str]]): Player IDs on which to filter. Cannot be combined with player_names. Accepts a string or list of strings.
            player_names (Union[str, List[str]]): Player names on which to filter. Partial matches are accepted. Cannot be combined with player_ids. Accepts a string or list of strings.
            team_ids (Union[str, List[str]]): Team IDs on which to filter. Cannot be combined with team_names. Accepts a string or list of strings.
            team_names (Union[str, List[str]]): Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with team_ids. Accepts a string or list of strings.
            position (Union[str, List[str]]): Describes the general position, as reported by the players' association. Valid keywords include: 'GK', 'D', 'M', and 'F'. Accepts a string or list of strings.
            season_name (Union[str, List[str]]): Name(s)/year(s) of seasons. Cannot be combined with a date range. Accepts a string or list of strings.
            start_date (str): Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            end_date (str): End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.

        Returns:
            DataFrame
        """
        player_salaries = self._get_stats(
            leagues, type="salaries", entity="players", **kwargs
        )
        return player_salaries

    def get_goalkeeper_xgoals(
        self, leagues: Union[str, List[str]] = LEAGUES, **kwargs
    ) -> DataFrame:
        """Retrieves a DataFrame containing goalkeeper xG data meeting the specified conditions.

        Args:
         leagues (Union[str, List[str]], optional): League(s) on which to filter. Accepts a string or list of strings. Defaults to LEAGUES.

        Keyword Args:
            minimum_minutes (int): Minimum threshold for sum of minutes played.
            minimum_shots_faced (int): Minimum threshold for sum of shots faced.
            player_ids (Union[str, List[str]]): Player IDs on which to filter. Cannot be combined with player_names. Accepts a string or list of strings.
            player_names (Union[str, List[str]]): Player names on which to filter. Partial matches are accepted. Cannot be combined with player_ids. Accepts a string or list of strings.
            team_ids (Union[str, List[str]]): Team IDs on which to filter. Cannot be combined with team_names. Accepts a string or list of strings.
            team_names (Union[str, List[str]]): Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with team_ids. Accepts a string or list of strings.
            season_name (Union[str, List[str]]): Name(s)/year(s) of seasons. Cannot be combined with a date range. Accepts a string or list of strings.
            start_date (str): Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            end_date (str): End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            shot_pattern (Union[str, List[str]]): Describes the possessing actions leading to the shot. Valid keywords include: 'Set piece', 'Corner', 'Free kick', 'Penalty', 'Fastbreak', and 'Regular'. Accepts a string or list of strings.
            split_by_teams (bool): Logical indicator to group results by team.
            split_by_seasons (bool): Logical indicator to group results by season.
            split_by_games (bool): Logical indicator to group results by game.
            stage_name (Union[str, List[str]]): Describes the stage of competition in which a game took place. Accepts a string or list of strings.

        Returns:
            DataFrame
        """
        goalkeeper_xgoals = self._get_stats(
            leagues, type="xgoals", entity="goalkeepers", **kwargs
        )
        return goalkeeper_xgoals

    def get_goalkeeper_goals_added(
        self, leagues: Union[str, List[str]] = LEAGUES, **kwargs
    ) -> DataFrame:
        """Retrieves a DataFrame containing goalkeeper g+ data meeting the specified conditions.

        Args:
            leagues (Union[str, List[str]], optional): League(s) on which to filter. Accepts a string or list of strings. Defaults to LEAGUES.

        Keyword Args:
            minimum_minutes (int): Minimum threshold for sum of minutes played.
            player_ids (Union[str, List[str]]): Player IDs on which to filter. Cannot be combined with player_names. Accepts a string or list of strings.
            player_names (Union[str, List[str]]): Player names on which to filter. Partial matches are accepted. Cannot be combined with player_ids. Accepts a string or list of strings.
            team_ids (Union[str, List[str]]): Team IDs on which to filter. Cannot be combined with team_names. Accepts a string or list of strings.
            team_names (Union[str, List[str]]): Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with team_ids. Accepts a string or list of strings.
            season_name (Union[str, List[str]]): Name(s)/year(s) of seasons. Cannot be combined with a date range. Accepts a string or list of strings.
            start_date (str): Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            end_date (str): End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            split_by_teams (bool): Logical indicator to group results by team.
            split_by_seasons (bool): Logical indicator to group results by season.
            split_by_games (bool): Logical indicator to group results by game.
            stage_name (Union[str, List[str]]): Describes the stage of competition in which a game took place. Accepts a string or list of strings.
            action_type (Union[str, List[str]]): Describes the goals added (g+) action type. Valid keywords include: 'Dribbling', 'Fouling', 'Interrupting', 'Passing', 'Receiving', and 'Shooting'. Accepts a string or list of strings.
            above_replacement (bool): Logical indicator to compare players against replacement-level values. This will only return aggregated g+ values, rather than disaggregated g+ values by action type.

        Returns:
            DataFrame
        """
        goalkeeper_goals_added = self._get_stats(
            leagues, type="goals-added", entity="goalkeepers", **kwargs
        )
        return goalkeeper_goals_added

    def get_team_xgoals(
        self, leagues: Union[str, List[str]] = LEAGUES, **kwargs
    ) -> DataFrame:
        """Retrieves a DataFrame containing team xG data meeting the specified conditions.

        Args:
            leagues (Union[str, List[str]], optional): Leagues on which to filter. Accepts a string or list of strings. Defaults to LEAGUES.

        Keyword Args:
            team_ids (Union[str, List[str]]): Team IDs on which to filter. Cannot be combined with team_names. Accepts a string or list of strings.
            team_names (Union[str, List[str]]): Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with team_ids. Accepts a string or list of strings.
            season_name (Union[str, List[str]]): Name(s)/year(s) of seasons. Cannot be combined with a date range. Accepts a string or list of strings.
            start_date (str): Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            end_date (str): End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            shot_pattern (Union[str, List[str]]): Describes the possessing actions leading to the shot. Valid keywords include: 'Set piece', 'Corner', 'Free kick', 'Penalty', 'Fastbreak', and 'Regular'. Accepts a string or list of strings.
            split_by_seasons (bool): Logical indicator to group results by season.
            split_by_games (bool): Logical indicator to group results by game.
            home_only (bool): Logical indicator to only include results from home games.
            away_only (bool): Logical indicator to only include results from away games.
            home_adjusted (bool): Logical indicator to adjust certain values based on the share of home games a team has played during the specified duration.
            even_game_state (bool): Logical indicator to only include shots taken when the score was level.
            stage_name (Union[str, List[str]]): Describes the stage of competition in which a game took place. Accepts a string or list of strings.

        Returns:
            DataFrame
        """
        team_xgoals = self._get_stats(leagues, type="xgoals", entity="teams", **kwargs)
        return team_xgoals

    def get_team_xpass(
        self, leagues: Union[str, List[str]] = LEAGUES, **kwargs
    ) -> DataFrame:
        """Retrieves a DataFrame containing team xPass data meeting the specified conditions.

        Args:
            leagues (Union[str, List[str]], optional): Leagues on which to filter. Accepts a string or list of strings. Defaults to LEAGUES.

        Keyword Args:
            team_ids (Union[str, List[str]]): Team IDs on which to filter. Cannot be combined with team_names. Accepts a string or list of strings.
            team_names (Union[str, List[str]]): Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with team_ids. Accepts a string or list of strings.
            season_name (Union[str, List[str]]): Name(s)/year(s) of seasons. Cannot be combined with a date range. Accepts a string or list of strings.
            start_date (str): Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            end_date (str): End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            pass_origin_third (Union[str, List[str]]): Describes the third of the field from which the pass originated. Valid keywords include: 'Attacking', 'Middle', and 'Defensive'. Accepts a string or list of strings.
            split_by_seasons (bool): Logical indicator to group results by season.
            split_by_games (bool): Logical indicator to group results by game.
            home_only (bool): Logical indicator to only include results from home games.
            away_only (bool): Logical indicator to only include results from away games.
            stage_name (Union[str, List[str]]): Describes the stage of competition in which a game took place. Accepts a string or list of strings.

        Returns:
            DataFrame
        """
        team_xpass = self._get_stats(leagues, type="xpass", entity="teams", **kwargs)
        return team_xpass

    def get_team_goals_added(
        self, leagues: Union[str, List[str]] = LEAGUES, **kwargs
    ) -> DataFrame:
        """Retrieves a DataFrame containing team g+ data meeting the specified conditions.

        Args:
            leagues (Union[str, List[str]], optional): Leagues on which to filter. Accepts a string or list of strings. Defaults to LEAGUES.

        Keyword Args:
            team_ids (Union[str, List[str]]): Team IDs on which to filter. Cannot be combined with team_names. Accepts a string or list of strings.
            team_names (Union[str, List[str]]): Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with team_ids. Accepts a string or list of strings.
            season_name (Union[str, List[str]]): Name(s)/year(s) of seasons. Cannot be combined with a date range. Accepts a string or list of strings.
            split_by_seasons (bool): Logical indicator to group results by season.
            stage_name (Union[str, List[str]]): Describes the stage of competition in which a game took place. Accepts a string or list of strings.
            action_type (Union[str, List[str]]): Describes the goals added (g+) action type. Valid keywords include: 'Dribbling', 'Fouling', 'Interrupting', 'Passing', 'Receiving', and 'Shooting'. Accepts a string or list of strings.
            zone (Union[int, List[int]]): Zone number on pitch. Zones 1-5 are the defensive-most zones, and zones 26-30 are the attacking-most zones. Accepts a number or list of numbers.
            gamestate_trunc (Union[int, List[int]]): Integer (score differential) value between -2 and 2, inclusive. Gamestates more extreme than -2 and 2 have been included with -2 and 2, respectively. Accepts a number or list of numbers.

        Returns:
            DataFrame
        """
        team_goals_added = self._get_stats(
            leagues, type="goals-added", entity="teams", **kwargs
        )
        return team_goals_added

    def get_team_salaries(
        self, leagues: Union[str, List[str]] = "mls", **kwargs
    ) -> DataFrame:
        """Retrieves a DataFrame containing team salary data meeting the specified conditions.

        Args:
            leagues (Union[str, List[str]], optional): Leagues on which to filter. Accepts a string or list of strings. Defaults to 'mls'.

        Keyword Args:
            team_ids (Union[str, List[str]]): Team IDs on which to filter. Cannot be combined with team_names. Accepts a string or list of strings.
            team_names (Union[str, List[str]]): Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with team_ids. Accepts a string or list of strings.
            season_name (Union[str, List[str]]): Name(s)/year(s) of seasons. Cannot be combined with a date range. Accepts a string or list of strings.
            split_by_teams (bool): Logical indicator to group results by team. Results must be grouped by at least one of teams, positions, or seasons. Value is True by default.
            split_by_seasons (bool): Logical indicator to group results by season. Results must be grouped by at least one of teams, positions, or seasons.
            split_by_positions (bool): Logical indicator to group results by positions. Results must be grouped by at least one of teams, positions, or seasons.

        Returns:
            DataFrame
        """
        team_salaries = self._get_stats(
            leagues, type="salaries", entity="teams", **kwargs
        )
        return team_salaries

    def get_game_xgoals(
        self, leagues: Union[str, List[str]] = LEAGUES, **kwargs
    ) -> DataFrame:
        """Retrieves a DataFrame containing game xG data meeting the specified conditions.

        Args:
            leagues (Union[str, List[str]], optional): Leagues on which to filter. Accepts a string or list of strings. Defaults to LEAGUES.

        Keyword Args:
            game_ids (Union[str, List[str]]): Game IDs on which to filter. Accepts a string or list of strings.
            season_name (Union[str, List[str]]): Name(s)/year(s) of seasons. Cannot be combined with a date range. Accepts a string or list of strings.
            start_date (str): Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            end_date (str): End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            stage_name (Union[str, List[str]]): Describes the stage of competition in which a game took place. Accepts a string or list of strings.

        Returns:
            DataFrame
        """
        game_xgoals = self._get_stats(leagues, type="xgoals", entity="games", **kwargs)
        return game_xgoals
