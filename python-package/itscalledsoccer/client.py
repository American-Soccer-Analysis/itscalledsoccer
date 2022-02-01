import json
from logging import getLevelName, getLogger
from typing import Dict, List, Optional, Union

import pandas as pd
import requests
from cachecontrol import CacheControl
from rapidfuzz import fuzz, process


class AmericanSoccerAnalysis:
    """Wrapper around the ASA Shiny API"""

    API_VERSION = "v1"
    BASE_URL = f"https://app.americansocceranalysis.com/api/{API_VERSION}/"
    LEAGUES = ["nwsl", "mls", "uslc", "usl1", "nasl"]
    MAX_API_LIMIT = 1000
    LOGGER = getLogger(__name__)

    def __init__(
        self, proxies: Optional[dict] = None, logging_level: Optional[str] = "WARNING"
    ) -> None:
        """Class constructor

        :param proxies: A dictionary containing proxy mappings, see https://2.python-requests.org/en/master/user/advanced/#proxies
        :param logging_level: A string respresenting the logging level of the logger
        """
        SESSION = requests.session()
        if proxies:
            SESSION.proxies.update(proxies)
        CACHE_SESSION = CacheControl(SESSION)

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
                print(f"Logging level {logging_level} not recognized!")

        self.session = CACHE_SESSION
        self.base_url = self.BASE_URL
        self.players = self._get_entity("player")
        self.teams = self._get_entity("team")
        self.stadia = self._get_entity("stadia")
        self.managers = self._get_entity("manager")
        self.referees = self._get_entity("referee")
        print("Finished initializing client")

    def _get_entity(self, type: str) -> pd.DataFrame:
        """Gets all the data for a specific type and
        stores it in a dataframe.

        :param type: type of data to get
        :returns: dataframe
        """
        plural_type = f"{type}s" if type != "stadia" else f"{type}"
        print(f"Gathering all {plural_type}")
        df = pd.DataFrame([])
        for league in self.LEAGUES:
            url = f"{self.BASE_URL}{league}/{plural_type}"
            response = self.session.get(url).json()
            # Convert list of objects to JSON
            resp_df = pd.read_json(json.dumps(response, default=lambda x: x.__dict__))
            resp_df = resp_df.assign(competition=league)
            df = df.append(resp_df)
        return df

    def _convert_name_to_id(self, type: str, name: str) -> str:
        """Converts the name of a player, manager, stadium, referee or team
        to their corresponding id.

        :param type: type of name to convert
        :param name: name
        :returns: a string
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

        :param type: type of name
        :param names: a name or list of names
        :returns: an id or list of ids
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

        :param leagues: league abbreviation or list of league abbreviations
        """
        if leagues:
            if isinstance(leagues, list):
                for l in leagues:
                    if l not in self.LEAGUES:
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

        :param leagues: league abbreviation or list of league abbreviations
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

        :param ids: a single id or list of ids
        :param names: a single name or list of names
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
        entity_all: pd.DataFrame,
        entity_type: str,
        leagues: Union[str, List[str], None],
        ids: Union[str, List[str], None] = None,
        names: Union[str, List[str], None] = None,
    ) -> pd.DataFrame:
        """Filters a dataframe based on the arguments given.

        :param entity_all: a dataframe containing the complete set of data
        :param entity_type: the type of data
        :param ids: a single id or list of ids
        :param names: a single name or list of names
        :returns: list of dictionaries, e.g. a dataframe converted to JSON
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
    ) -> pd.DataFrame:
        """Executes a query while handling the max number of responses from the API

        :param url: the API endpoint to call
        :param params: URL query strings
        :returns: Dataframe
        """
        temp_response = self._single_request(url, params)
        response = temp_response

        if isinstance(response, pd.DataFrame):
            offset = self.MAX_API_LIMIT

            while len(temp_response) == self.MAX_API_LIMIT:
                params["offset"] = str(offset)
                temp_response = self._execute_query(url, params)
                response = response.append(temp_response)
                offset = offset + self.MAX_API_LIMIT

        return response

    def _single_request(
        self, url: str, params: Dict[str, Union[str, List[str], None]]
    ) -> pd.DataFrame:
        """Handles single call to the API

        :param url: the API endpoint to call
        :param params: URL query strings
        :returns: Dataframe
        """
        response = self.session.get(url=url, params=params)
        response.raise_for_status()
        resp_df = pd.read_json(json.dumps(response.json()))
        return resp_df

    def _get_stats(
        self, leagues: Union[str, List[str]], type: str, entity: str, **kwargs
    ) -> pd.DataFrame:
        """Handles calls to stats APIs

        :param type: the API endpoint to call
        :param entity: URL query strings
        :param leagues:
        :param kwargs: additional keyword arguments
        :returns: Dataframe
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

        stats = pd.DataFrame([])
        if isinstance(leagues, str):
            url = f"{self.base_url}{leagues}/{entity}/{type}"
            response = self._execute_query(url, kwargs)

            stats = response
        elif isinstance(leagues, list):
            for league in leagues:
                url = f"{self.base_url}{league}/{entity}/{type}"

                response = self._execute_query(url, kwargs)

                stats = pd.concat([stats, response])

        return stats

    def get_stadia(
        self,
        leagues: Union[str, List[str]] = None,
        ids: Union[str, List[str]] = None,
        names: Union[str, List[str]] = None,
    ) -> pd.DataFrame:
        """Get information associated with stadia

        :param leagues: league abbreviation or a list of league abbreviations
        :param ids: a single stadium id or a list of stadia ids (optional)
        :param names: a single stadium name or a list of stadia names (optional)
        :returns: Dataframe
        """
        stadia = self._filter_entity(self.stadia, "stadium", leagues, ids, names)
        return stadia

    def get_referees(
        self,
        leagues: Union[str, List[str]] = None,
        ids: Union[str, List[str]] = None,
        names: Union[str, List[str]] = None,
    ) -> pd.DataFrame:
        """Get information associated with referees

        :param leagues: league abbreviation or a list of league abbreviations
        :param ids: a single referee id or a list of referee ids (optional)
        :param names: a single referee name or a list of referee names (optional)
        :returns: Dataframe
        """
        referees = self._filter_entity(self.referees, "referee", leagues, ids, names)
        return referees

    def get_managers(
        self,
        leagues: Union[str, List[str]] = None,
        ids: Union[str, List[str]] = None,
        names: Union[str, List[str]] = None,
    ) -> pd.DataFrame:
        """Get information associated with managers

        :param leagues: league abbreviation or a list of league abbreviations
        :param ids: a single referee id or a list of referee ids (optional)
        :param names: a single referee name or a list of referee names (optional)
        :returns: Dataframe
        """
        managers = self._filter_entity(self.managers, "manager", leagues, ids, names)
        return managers

    def get_teams(
        self,
        leagues: Union[str, List[str]] = None,
        ids: Union[str, List[str]] = None,
        names: Union[str, List[str]] = None,
    ) -> pd.DataFrame:
        """Get information associated with teams

        :param leagues: league abbreviation or a list of league abbreviations
        :param ids: a single team id or a list of team ids (optional)
        :param names: a single team name or a list of team names (optional)
        :returns: Dataframe
        """
        teams = self._filter_entity(self.teams, "team", leagues, ids, names)
        return teams

    def get_players(
        self,
        leagues: Union[str, List[str]] = None,
        ids: Union[str, List[str]] = None,
        names: Union[str, List[str]] = None,
    ) -> pd.DataFrame:
        """Get information associated with players

        :param league: league abbreviation or a list of league abbreviations
        :param ids: a single player id or a list of player ids (optional)
        :param names: a single player name or a list of player names (optional)
        :returns: Dataframe
        """
        players = self._filter_entity(self.players, "player", leagues, ids, names)
        return players

    def get_games(
        self,
        leagues: Union[str, List[str]] = None,
        game_ids: Union[str, List[str]] = None,
        team_ids: Union[str, List[str]] = None,
        team_names: Union[str, List[str]] = None,
        seasons: Union[str, List[str]] = None,
        stages: Union[str, List[str]] = None,
    ) -> pd.DataFrame:
        """Get information related to games

        :param leagues: league abbreviation or a list of league abbreviations
        :param game_ids: a single game id or a list of game ids
        :param team_ids: a single team id or a list of team ids
        :param team_names: a single team name or a list of team names
        :param seasons: a single year of a league season or a list of years
        :param stages: a single stage of competition in which a game took place or list of stages
        :returns: Dataframe
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

        games = pd.DataFrame([])
        if isinstance(leagues, str):
            games_url = f"{self.base_url}{leagues}/games"
            response = self._execute_query(games_url, query)

            games = response
        elif isinstance(leagues, list):
            for league in leagues:
                games_url = f"{self.base_url}{league}/games"
                response = self._execute_query(games_url, query)

                games = pd.concat([games, response])

        return games.sort_values(by=["date_time_utc"], ascending=False)

    def get_player_xgoals(
        self, leagues: Union[str, List[str]] = LEAGUES, **kwargs
    ) -> pd.DataFrame:
        """Retrieves a data frame containing player xG data meeting the specified conditions.
        :param leagues: League(s) on which to filter. Accepts a string or list of strings.
        :param kwargs: The following arguments will be parsed:
            minimum_minutes: Minimum threshold for sum of minutes played.
            minimum_shots: Minimum threshold for sum of shots.
            minimum_key_passes: Minimum threshold for sum of key passes.
            player_ids: Player IDs on which to filter. Cannot be combined with player_names. Accepts a string or list of strings.
            player_names: Player names on which to filter. Partial matches are accepted. Cannot be combined with player_ids. Accepts a string or list of strings.
            team_ids: Team IDs on which to filter. Cannot be combined with team_names. Accepts a string or list of strings.
            team_names: Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with team_ids. Accepts a string or list of strings.
            season_name: Name(s)/year(s) of seasons. Cannot be combined with a date range. Accepts a string or list of strings.
            start_date: Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            end_date: End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            shot_pattern: Describes the possessing actions leading to the shot. Valid keywords include: 'Set piece', 'Corner', 'Free kick', 'Penalty', 'Fastbreak', and 'Regular'. Accepts a string or list of strings.
            split_by_teams: Logical indicator to group results by team.
            split_by_seasons: Logical indicator to group results by season.
            split_by_games: Logical indicator to group results by game.
            stage_name: Describes the stage of competition in which a game took place. Accepts a string or list of strings.
            general_position: Describes the most common position played by each player over the specified period of time. Valid keywords include: 'GK', 'CB', 'FB', 'DM', 'CM', 'AM', 'W', and 'ST'. Accepts a string or list of strings.
        :returns: Dataframe
        """
        player_xgoals = self._get_stats(
            leagues, type="xgoals", entity="players", **kwargs
        )
        return player_xgoals

    def get_player_xpass(
        self, leagues: Union[str, List[str]] = LEAGUES, **kwargs
    ) -> pd.DataFrame:
        """Retrieves a data frame containing player xPass data meeting the specified conditions.
        :param leagues: League(s) on which to filter. Accepts a string or list of strings.
        :param kwargs: The following arguments will be parsed:
            minimum_minutes: Minimum threshold for sum of minutes played.
            minimum_passes: Minimum threshold for sum of attempted passes.
            player_ids: Player IDs on which to filter. Cannot be combined with player_names. Accepts a string or list of strings.
            player_names: Player names on which to filter. Partial matches are accepted. Cannot be combined with player_ids. Accepts a string or list of strings.
            team_ids: Team IDs on which to filter. Cannot be combined with team_names. Accepts a string or list of strings.
            team_names: Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with team_ids. Accepts a string or list of strings.
            season_name: Name(s)/year(s) of seasons. Cannot be combined with a date range. Accepts a string or list of strings.
            start_date: Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            end_date: End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            pass_origin_third: Describes the third of the field from which the pass originated. Valid keywords include: 'Attacking', 'Middle', and 'Defensive'. Accepts a string or list of strings.
            split_by_teams: Logical indicator to group results by team.
            split_by_seasons: Logical indicator to group results by season.
            split_by_games: Logical indicator to group results by game.
            stage_name: Describes the stage of competition in which a game took place. Accepts a string or list of strings.
            general_position: Describes the most common position played by each player over the specified period of time. Valid keywords include: 'GK', 'CB', 'FB', 'DM', 'CM', 'AM', 'W', and 'ST'. Accepts a string or list of strings.
        :returns: Dataframe
        """
        player_xpass = self._get_stats(
            leagues, type="xpass", entity="players", **kwargs
        )
        return player_xpass

    def get_player_goals_added(
        self, leagues: Union[str, List[str]] = LEAGUES, **kwargs
    ) -> pd.DataFrame:
        """Retrieves a data frame containing player g+ data meeting the specified conditions.
        :param leagues: League(s) on which to filter. Accepts a string or list of strings.
        :param kwargs: The following arguments will be parsed:
            minimum_minutes: Minimum threshold for sum of minutes played.
            player_ids: Player IDs on which to filter. Cannot be combined with player_names. Accepts a string or list of strings.
            player_names: Player names on which to filter. Partial matches are accepted. Cannot be combined with player_ids. Accepts a string or list of strings.
            team_ids: Team IDs on which to filter. Cannot be combined with team_names. Accepts a string or list of strings.
            team_names: Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with team_ids. Accepts a string or list of strings.
            season_name: Name(s)/year(s) of seasons. Cannot be combined with a date range. Accepts a string or list of strings.
            start_date: Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            end_date: End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            split_by_teams: Logical indicator to group results by team.
            split_by_seasons: Logical indicator to group results by season.
            split_by_games: Logical indicator to group results by game.
            stage_name: Describes the stage of competition in which a game took place. Accepts a string or list of strings.
            action_type: Describes the goals added (g+) action type. Valid keywords include: 'Dribbling', 'Fouling', 'Interrupting', 'Passing', 'Receiving', and 'Shooting'. Accepts a string or list of strings.
            general_position: Describes the most common position played by each player over the specified period of time. Valid keywords include: 'GK', 'CB', 'FB', 'DM', 'CM', 'AM', 'W', and 'ST'. Accepts a string or list of strings.
            above_replacement: Logical indicator to compare players against replacement-level values. This will only return aggregated g+ values, rather than disaggregated g+ values by action type.
        :returns: Dataframe
        """
        player_goals_added = self._get_stats(
            leagues, type="goals-added", entity="players", **kwargs
        )
        return player_goals_added

    def get_player_salaries(
        self, leagues: Union[str, List[str]] = "mls", **kwargs
    ) -> pd.DataFrame:
        """Retrieves a data frame containing player salary data meeting the specified conditions

        :param leagues: Leagues on which to filter. Accepts a string or list of strings.
        :param kwargs: The following arguments will be parsed:
            player_ids: Player IDs on which to filter. Cannot be combined with player_names. Accepts a string or list of strings.
            player_names: Player names on which to filter. Partial matches are accepted. Cannot be combined with player_ids. Accepts a string or list of strings.
            team_ids: Team IDs on which to filter. Cannot be combined with team_names. Accepts a string or list of strings.
            team_names: Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with team_ids. Accepts a string or list of strings.
            position: Describes the general position, as reported by the players' association. Valid keywords include: 'GK', 'D', 'M', and 'F'. Accepts a string or list of strings.
            season_name: Name(s)/year(s) of seasons. Cannot be combined with a date range. Accepts a string or list of strings.
            start_date: Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            end_date: End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
        :returns: Dataframe
        """
        player_salaries = self._get_stats(
            leagues, type="salaries", entity="players", **kwargs
        )
        return player_salaries

    def get_goalkeeper_xgoals(
        self, leagues: Union[str, List[str]] = LEAGUES, **kwargs
    ) -> pd.DataFrame:
        """Retrieves a data frame containing goalkeeper xG data meeting the specified conditions.
        :param leagues: League(s) on which to filter. Accepts a string or list of strings.
        :param kwargs: The following arguments will be parsed:
            minimum_minutes: Minimum threshold for sum of minutes played.
            minimum_shots_faced: Minimum threshold for sum of shots faced.
            player_ids: Player IDs on which to filter. Cannot be combined with player_names. Accepts a string or list of strings.
            player_names: Player names on which to filter. Partial matches are accepted. Cannot be combined with player_ids. Accepts a string or list of strings.
            team_ids: Team IDs on which to filter. Cannot be combined with team_names. Accepts a string or list of strings.
            team_names: Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with team_ids. Accepts a string or list of strings.
            season_name: Name(s)/year(s) of seasons. Cannot be combined with a date range. Accepts a string or list of strings.
            start_date: Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            end_date: End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            shot_pattern: Describes the possessing actions leading to the shot. Valid keywords include: 'Set piece', 'Corner', 'Free kick', 'Penalty', 'Fastbreak', and 'Regular'. Accepts a string or list of strings.
            split_by_teams: Logical indicator to group results by team.
            split_by_seasons: Logical indicator to group results by season.
            split_by_games: Logical indicator to group results by game.
            stage_name: Describes the stage of competition in which a game took place. Accepts a string or list of strings.
        :returns: Dataframe
        """
        goalkeeper_xgoals = self._get_stats(
            leagues, type="xgoals", entity="goalkeepers", **kwargs
        )
        return goalkeeper_xgoals

    def get_goalkeeper_goals_added(
        self, leagues: Union[str, List[str]] = LEAGUES, **kwargs
    ) -> pd.DataFrame:
        """Retrieves a data frame containing goalkeeper g+ data meeting the specified conditions.
        :param leagues: League(s) on which to filter. Accepts a string or list of strings.
        :param kwargs: The following arguments will be parsed:
            minimum_minutes: Minimum threshold for sum of minutes played.
            player_ids: Player IDs on which to filter. Cannot be combined with player_names. Accepts a string or list of strings.
            player_names: Player names on which to filter. Partial matches are accepted. Cannot be combined with player_ids. Accepts a string or list of strings.
            team_ids: Team IDs on which to filter. Cannot be combined with team_names. Accepts a string or list of strings.
            team_names: Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with team_ids. Accepts a string or list of strings.
            season_name: Name(s)/year(s) of seasons. Cannot be combined with a date range. Accepts a string or list of strings.
            start_date: Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            end_date: End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            split_by_teams: Logical indicator to group results by team.
            split_by_seasons: Logical indicator to group results by season.
            split_by_games: Logical indicator to group results by game.
            stage_name: Describes the stage of competition in which a game took place. Accepts a string or list of strings.
            action_type: Describes the goals added (g+) action type. Valid keywords include: 'Dribbling', 'Fouling', 'Interrupting', 'Passing', 'Receiving', and 'Shooting'. Accepts a string or list of strings.
            above_replacement: Logical indicator to compare players against replacement-level values. This will only return aggregated g+ values, rather than disaggregated g+ values by action type.
        :returns: Dataframe
        """
        goalkeeper_goals_added = self._get_stats(
            leagues, type="goals-added", entity="goalkeepers", **kwargs
        )
        return goalkeeper_goals_added

    def get_team_xgoals(
        self, leagues: Union[str, List[str]] = LEAGUES, **kwargs
    ) -> pd.DataFrame:
        """Retrieves a data frame containing team xG data meeting the specified conditions.

        :param leagues: Leagues on which to filter. Accepts a string or list of strings.
        :param kwargs: The following arguments will be parsed:
            team_ids: Team IDs on which to filter. Cannot be combined with team_names. Accepts a string or list of strings.
            team_names: Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with team_ids. Accepts a string or list of strings.
            season_name: Name(s)/year(s) of seasons. Cannot be combined with a date range. Accepts a string or list of strings.
            start_date: Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            end_date: End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            shot_pattern: Describes the possessing actions leading to the shot. Valid keywords include: 'Set piece', 'Corner', 'Free kick', 'Penalty', 'Fastbreak', and 'Regular'. Accepts a string or list of strings.
            split_by_seasons: Logical indicator to group results by season.
            split_by_games: Logical indicator to group results by game.
            home_only: Logical indicator to only include results from home games.
            away_only: Logical indicator to only include results from away games.
            home_adjusted: Logical indicator to adjust certain values based on the share of home games a team has played during the specified duration.
            even_game_state: Logical indicator to only include shots taken when the score was level.
            stage_name: Describes the stage of competition in which a game took place. Accepts a string or list of strings.
        :returns: Dataframe
        """
        team_xgoals = self._get_stats(leagues, type="xgoals", entity="teams", **kwargs)
        return team_xgoals

    def get_team_xpass(
        self, leagues: Union[str, List[str]] = LEAGUES, **kwargs
    ) -> pd.DataFrame:
        """Retrieves a data frame containing team xPass data meeting the specified conditions.

        :param leagues: Leagues on which to filter. Accepts a string or list of strings.
        :param kwargs: The following arguments will be parsed:
            team_ids: Team IDs on which to filter. Cannot be combined with team_names. Accepts a string or list of strings.
            team_names: Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with team_ids. Accepts a string or list of strings.
            season_name: Name(s)/year(s) of seasons. Cannot be combined with a date range. Accepts a string or list of strings.
            start_date: Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            end_date: End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            pass_origin_third: Describes the third of the field from which the pass originated. Valid keywords include: 'Attacking', 'Middle', and 'Defensive'. Accepts a string or list of strings.
            split_by_seasons: Logical indicator to group results by season.
            split_by_games: Logical indicator to group results by game.
            home_only: Logical indicator to only include results from home games.
            away_only: Logical indicator to only include results from away games.
            stage_name: Describes the stage of competition in which a game took place. Accepts a string or list of strings.
        :returns: Dataframe
        """
        team_xpass = self._get_stats(leagues, type="xpass", entity="teams", **kwargs)
        return team_xpass

    def get_team_goals_added(
        self, leagues: Union[str, List[str]] = LEAGUES, **kwargs
    ) -> pd.DataFrame:
        """Retrieves a data frame containing team g+ data meeting the specified conditions.

        :param leagues: Leagues on which to filter. Accepts a string or list of strings.
        :param kwargs: The following arguments will be parsed:
            team_ids: Team IDs on which to filter. Cannot be combined with team_names. Accepts a string or list of strings.
            team_names: Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with team_ids. Accepts a string or list of strings.
            season_name: Name(s)/year(s) of seasons. Cannot be combined with a date range. Accepts a string or list of strings.
            split_by_seasons: Logical indicator to group results by season.
            stage_name: Describes the stage of competition in which a game took place. Accepts a string or list of strings.
            action_type: Describes the goals added (g+) action type. Valid keywords include: 'Dribbling', 'Fouling', 'Interrupting', 'Passing', 'Receiving', and 'Shooting'. Accepts a string or list of strings.
            zone: Zone number on pitch. Zones 1-5 are the defensive-most zones, and zones 26-30 are the attacking-most zones. Accepts a number or list of numbers.
            gamestate_trunc: Integer (score differential) value between -2 and 2, inclusive. Gamestates more extreme than -2 and 2 have been included with -2 and 2, respectively. Accepts a number or list of numbers.
        :returns: Dataframe
        """
        team_goals_added = self._get_stats(
            leagues, type="goals-added", entity="teams", **kwargs
        )
        return team_goals_added

    def get_team_salaries(
        self, leagues: Union[str, List[str]] = "mls", **kwargs
    ) -> pd.DataFrame:
        """Retrieves a data frame containing team salary data meeting the specified conditions.

        :param leagues: Leagues on which to filter. Accepts a string or list of strings.
        :param kwargs: The following arguments will be parsed:
            team_ids: Team IDs on which to filter. Cannot be combined with team_names. Accepts a string or list of strings.
            team_names: Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with team_ids. Accepts a string or list of strings.
            season_name: Name(s)/year(s) of seasons. Cannot be combined with a date range. Accepts a string or list of strings.
            split_by_teams: Logical indicator to group results by team. Results must be grouped by at least one of teams, positions, or seasons. Value is True by default.
            split_by_seasons: Logical indicator to group results by season. Results must be grouped by at least one of teams, positions, or seasons.
            split_by_positions: Logical indicator to group results by positions. Results must be grouped by at least one of teams, positions, or seasons.
        :returns: Dataframe
        """
        team_salaries = self._get_stats(
            leagues, type="salaries", entity="teams", **kwargs
        )
        return team_salaries

    def get_game_xgoals(
        self, leagues: Union[str, List[str]] = LEAGUES, **kwargs
    ) -> pd.DataFrame:
        """Retrieves a data frame containing game xG data meeting the specified conditions.

        :param leagues: Leagues on which to filter. Accepts a string or list of strings.
        :param kwargs: The following arguments will be parsed:
            game_ids: Game IDs on which to filter. Accepts a string or list of strings.
            season_name: Name(s)/year(s) of seasons. Cannot be combined with a date range. Accepts a string or list of strings.
            start_date: Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            end_date: End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            stage_name: Describes the stage of competition in which a game took place. Accepts a string or list of strings.
        :returns: Dataframe
        """
        game_xgoals = self._get_stats(leagues, type="xgoals", entity="games", **kwargs)
        return game_xgoals
