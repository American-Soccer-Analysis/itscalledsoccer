from logging import getLevelName, getLogger

import requests
from cachecontrol import CacheControl
from cachecontrol.heuristics import ExpiresAfter
from pandas import DataFrame, concat
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
        proxies: dict | None = None,
        logging_level: str | None = "WARNING",
        lazy_load: bool | None = True,
    ) -> None:
        """Class constructor

        Args:
            proxies (dict | None): A dictionary containing proxy mappings, see https://docs.python-requests.org/en/latest/user/advanced/#proxies. Defaults to None.
            logging_level (str | None): A string representing the logging level of the logger. Defaults to "WARNING".
            lazy_load (bool | None): A boolean indicating whether to lazy load all entity data on initialization. Defaults to True.
        """
        session = requests.session()
        if proxies:
            session.proxies.update(proxies)
        cache_session = CacheControl(session, heuristic=ExpiresAfter(days=1))

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

        self.session = cache_session
        self.base_url = self.BASE_URL
        self.lazy_load = lazy_load

        self.players: DataFrame | None = None
        self.teams: DataFrame | None = None
        self.stadia: DataFrame | None = None
        self.managers: DataFrame | None = None
        self.referees: DataFrame | None = None

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

    def _get_entity(self, entity_type: str) -> DataFrame:
        """Gets all the data for a specific type and
        stores it in a DataFrame.

        Args:
            entity_type (str): type of data to get

        Returns:
            DataFrame: All records for the given entity type across all leagues,
          with a "competition" column indicating the source league.
        """
        plural_type = f"{entity_type}s" if entity_type != "stadia" else f"{entity_type}"
        self.LOGGER.info(f"Gathering all {plural_type}")
        frames = []
        for league in self.LEAGUES:
            url = f"{self.base_url}{league}/{plural_type}"
            resp_df = self._execute_query(url, {})
            resp_df = resp_df.assign(competition=league)
            frames.append(resp_df)
        return concat(frames, ignore_index=True) if frames else DataFrame([])

    def _convert_name_to_id(self, entity_type: str, name: str) -> str:
        """Converts the name of a player, manager, stadium, referee or team
        to their corresponding id.

        Args:
            entity_type (str): type of name to convert
            name (str): name

        Returns:
          str: the matched id
        """
        min_score = 70

        TYPE_MAP = {
            "player": ("players", "player_name", "player_id"),
            "manager": ("managers", "manager_name", "manager_id"),
            "stadium": ("stadia", "stadium_name", "stadium_id"),
            "referee": ("referees", "referee_name", "referee_id"),
            "team": ("teams", "team_name", "team_id"),
        }

        if entity_type not in TYPE_MAP:
            raise ValueError(f"Unknown entity type '{entity_type}'.")

        attr, name_col, id_col = TYPE_MAP[entity_type]
        lookup = getattr(self, attr)
        names = lookup[name_col].to_list()

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

        matched_id = lookup.loc[lookup[name_col] == name, id_col].iloc[0]

        return matched_id

    def _convert_names_to_ids(
        self, entity_type: str, names: str | list[str]
    ) -> str | list[str] | None:
        """Converts a name or list of names to an id or list of ids

        Args:
            entity_type (str): type of name
            names (str | list[str]): a name or list of names

        Returns:
            str | list[str]: the matched ids
        """
        ids: list[str] = []
        if names is None:
            return None
        if isinstance(names, str):
            return self._convert_name_to_id(entity_type, names)
        else:
            for n in names:
                ids.append(self._convert_name_to_id(entity_type, n))
            return ids

    def _check_leagues(self, leagues: str | list[str] | None) -> None:
        """Validates the leagues parameter

        Args:
            leagues (str | list[str] | None): league abbreviation or list of league abbreviations
        """
        if leagues:
            if isinstance(leagues, list):
                for league in leagues:
                    if league not in self.LEAGUES:
                        raise ValueError(
                            f"{league} is not a valid league. Must be one of: {self.LEAGUES}"
                        )
            else:
                if leagues not in self.LEAGUES:
                    raise ValueError(
                        f"{leagues} is not valid. Must be one of: {self.LEAGUES}"
                    )

    def _check_leagues_salaries(self, leagues: str | list[str] | None) -> None:
        """Validates the leagues parameter for salary searches

        Args:
            leagues (str | list[str] | None): league abbreviation or list of league abbreviations
        """
        if leagues:
            if isinstance(leagues, list):
                if any([x != "mls" for x in leagues]):
                    raise ValueError("Only MLS salary data is publicly available.")
            else:
                if leagues != "mls":
                    raise ValueError("Only MLS salary data is publicly available.")

    def _check_ids_names(
        self, ids: str | list[str] | None, names: str | list[str] | None
    ) -> None:
        """Makes sure only ids or names are passed to a function and verifies
        they are the right data type.

        Args:
            ids (str | list[str] | None): a single id or list of ids
            names (str | list[str] | None): a single name or list of names
        """
        if ids and names:
            raise ValueError("Please specify only IDs or names, not both.")

        if ids:
            if not isinstance(ids, str) and not isinstance(ids, list):
                raise ValueError("IDs must be passed as a string or list of strings.")

        if names:
            if not isinstance(names, str) and not isinstance(names, list):
                raise ValueError("Names must be passed as a string or list of names.")

    def _filter_entity(
        self,
        entity_all: DataFrame,
        entity_type: str,
        leagues: str | list[str] | None,
        ids: str | list[str] | None = None,
        names: str | list[str] | None = None,
    ) -> DataFrame:
        """Filters a DataFrame based on the arguments given.

        Args:
            entity_all (DataFrame): a DataFrame containing the complete set of data
            entity_type (str): the type of data
            leagues (str | list[str] | None): league abbreviation or list of league abbreviations
            ids (str | list[str] | None): a single id or list of ids
            names (str | list[str] | None): a single name or list of names
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
        self, url: str, params: dict[str, str | list[str] | None]
    ) -> DataFrame:
        """Executes a query while handling the max number of responses from the API

        Args:
            url (str): the API endpoint to call
            params (dict[str, str | list[str] | None): URL query strings

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
        self, url: str, params: dict[str, str | list[str] | None]
    ) -> DataFrame:
        """Handles single call to the API

        Args:
            url (str): the API endpoint to call
            params (dict[str, str | list[str] | None): URL query strings

        Returns:
            DataFrame
        """
        response = self.session.get(url=url, params=params)
        response.raise_for_status()
        resp_df = DataFrame(response.json())
        return resp_df

    def _get_stats(
        self, leagues: str | list[str], stat_type: str, entity: str, **kwargs
    ) -> DataFrame:
        """Handles calls to stats APIs

        Args:
            stat_type (str): the API endpoint to call
            entity (str): URL query strings
            leagues (str | list[str] | None): league abbreviation or list of league abbreviations

        Keyword Args:
            split_by_teams (bool): Logical indicator to group results by team.
            split_by_seasons (bool): Logical indicator to group results by season.
            split_by_positions (bool): Logical indicator to group results by positions. Results must be grouped by at least one of teams, positions, or seasons.
            player_ids (str | list[str]): Player IDs on which to filter. Cannot be combined with player_names. Accepts a string or list of strings.
            player_names (str | list[str]): Player names on which to filter. Partial matches are accepted. Cannot be combined with player_ids. Accepts a string or list of strings.
            team_ids (str | list[str]): Team IDs on which to filter. Cannot be combined with team_names. Accepts a string or list of strings.
            team_names (str | list[str]): Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with team_ids. Accepts a string or list of strings.
            game_ids (str | list[str]): Game IDs on which to filter. Accepts a string or list of strings.

        Returns:
            DataFrame
        """
        self.LOGGER.info(f"get_stats called with {locals()}")
        if stat_type == "salaries":
            self._check_leagues_salaries(leagues)
            if (
                entity == "teams"
                and not kwargs.get("split_by_teams", False)
                and not kwargs.get("split_by_seasons", False)
                and not kwargs.get("split_by_positions", False)
            ):
                kwargs["split_by_teams"] = True
        else:
            self._check_leagues(leagues)

        PLAYER_KEYS = {"player_ids", "player_names"}
        TEAM_KEYS = {"team_ids", "team_names"}
        keys_dict = kwargs.keys()

        if PLAYER_KEYS & keys_dict:
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

        if TEAM_KEYS & keys_dict:
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

        if isinstance(leagues, str):
            stats = DataFrame([])
            url = f"{self.base_url}{leagues}/{entity}/{stat_type}"
            response = self._execute_query(url, kwargs)

            stats = response
        elif isinstance(leagues, list):
            frames = []
            for league in leagues:
                url = f"{self.base_url}{league}/{entity}/{stat_type}"

                response = self._execute_query(url, kwargs)

                frames.append(response)
            stats = concat(frames, ignore_index=True) if frames else DataFrame([])
        return stats

    def get_stadia(
        self,
        leagues: str | list[str] | None = None,
        ids: str | list[str] | None = None,
        names: str | list[str] | None = None,
    ) -> DataFrame:
        """Get information associated with stadia

        Args:
            leagues (str | list[str] | None): league abbreviation or list of league abbreviations. Defaults to None.
            ids (str | list[str] | None): a single id or list of ids. Defaults to None.
            names (str | list[str] | None): a single name or list of names. Defaults to None.

        Returns:
            DataFrame
        """
        if self.stadia is None:
            self.stadia = self._get_entity("stadia")
        stadia = self._filter_entity(self.stadia, "stadia", leagues, ids, names)
        return stadia

    def get_referees(
        self,
        leagues: str | list[str] | None = None,
        ids: str | list[str] | None = None,
        names: str | list[str] | None = None,
    ) -> DataFrame:
        """Get information associated with referees

        Args:
            leagues (str | list[str] | None): league abbreviation or a list of league abbreviations. Defaults to None.
            ids (str | list[str] | None): a single referee id or a list of referee ids. Defaults to None.
            names (str | list[str] | None): a single referee name or a list of referee names. Defaults to None.

        Returns:
            DataFrame
        """
        if self.referees is None:
            self.referees = self._get_entity("referee")
        referees = self._filter_entity(self.referees, "referee", leagues, ids, names)
        return referees

    def get_managers(
        self,
        leagues: str | list[str] | None = None,
        ids: str | list[str] | None = None,
        names: str | list[str] | None = None,
    ) -> DataFrame:
        """Get information associated with managers

        Args:
            leagues (str | list[str] | None): league abbreviation or a list of league abbreviations. Defaults to None.
            ids (str | list[str] | None): a single manager id or a list of manager ids. Defaults to None.
            names (str | list[str] | None): a single manager name or a list of manager names. Defaults to None.

        Returns:
            DataFrame
        """
        if self.managers is None:
            self.managers = self._get_entity("manager")
        managers = self._filter_entity(self.managers, "manager", leagues, ids, names)
        return managers

    def get_teams(
        self,
        leagues: str | list[str] | None = None,
        ids: str | list[str] | None = None,
        names: str | list[str] | None = None,
    ) -> DataFrame:
        """Get information associated with teams

        Args:
            leagues (str | list[str] | None): league abbreviation or a list of league abbreviations. Defaults to None.
            ids (str | list[str] | None): a single team id or a list of team ids. Defaults to None.
            names (str | list[str] | None): a single team name or a list of team names. Defaults to None.

        Returns:
            DataFrame
        """
        if self.teams is None:
            self.teams = self._get_entity("team")
        teams = self._filter_entity(self.teams, "team", leagues, ids, names)
        return teams

    def get_players(
        self,
        leagues: str | list[str] | None = None,
        ids: str | list[str] | None = None,
        names: str | list[str] | None = None,
    ) -> DataFrame:
        """Get information associated with players

        Args:
            leagues (str | list[str] | None): league abbreviation or a list of league abbreviations. Defaults to None.
            ids (str | list[str] | None): a single player id or a list of player ids. Defaults to None.
            names (str | list[str] | None): a single player name or a list of player names. Defaults to None.

        Returns:
            DataFrame
        """
        if self.players is None:
            self.players = self._get_entity("player")
        players = self._filter_entity(self.players, "player", leagues, ids, names)
        return players

    def get_games(
        self,
        leagues: str | list[str] | None = None,
        game_ids: str | list[str] | None = None,
        team_ids: str | list[str] | None = None,
        team_names: str | list[str] | None = None,
        seasons: str | list[str] | None = None,
        stages: str | list[str] | None = None,
        status: str | list[str] | None = None,
    ) -> DataFrame:
        """Get information related to games

        Args:
            leagues (str | list[str] | None): league abbreviation or a list of league abbreviations. Defaults to None.
            game_ids (str | list[str] | None): a single game id or a list of game ids. Defaults to None.
            team_ids (str | list[str] | None): a single team id or a list of team ids. Defaults to None.
            team_names (str | list[str] | None): a single team name or a list of team names. Defaults to None.
            seasons (str | list[str] | None): a single year of a league season or a list of years. Defaults to None.
            stages (str | list[str] | None): a single stage of competition in which a game took place or list of stages. Defaults to None.
            status (str | list[str] | None): Describes the status (IE: if it's been played or otherwise) of a game. Can take a single value or a list of values. Valid keywords include: Abandoned, FullTime, PreMatch. Defaults to None.

        Returns:
            DataFrame
        """
        self._check_leagues(leagues)
        self._check_ids_names(team_ids, team_names)

        query: dict[str, str | list[str] | None] = {}

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
        if status:
            query["status"] = status
        if not leagues:
            leagues = self.LEAGUES

        if isinstance(leagues, str):
            games = DataFrame([])
            games_url = f"{self.base_url}{leagues}/games"
            response = self._execute_query(games_url, query)

            games = response
        elif isinstance(leagues, list):
            frames = []
            for league in leagues:
                games_url = f"{self.base_url}{league}/games"
                response = self._execute_query(games_url, query)

                frames.append(response)
            games = concat(frames, ignore_index=True) if frames else DataFrame([])
        if games.empty:
            return games
        return games.sort_values(by=["date_time_utc"], ascending=False)

    def get_player_xgoals(
        self, leagues: str | list[str] = LEAGUES, **kwargs
    ) -> DataFrame:
        """Retrieves a DataFrame containing player xG data meeting the specified conditions.

        Args:
            leagues (str | list[str]): League(s) on which to filter. Accepts a string or list of strings.

        Keyword Args:
            minimum_minutes (int): Minimum threshold for sum of minutes played.
            minimum_shots (int): Minimum threshold for sum of shots.
            minimum_key_passes (int): Minimum threshold for sum of key passes.
            player_ids (str | list[str]): Player IDs on which to filter. Cannot be combined with player_names. Accepts a string or list of strings.
            player_names (str | list[str]): Player names on which to filter. Partial matches are accepted. Cannot be combined with player_ids. Accepts a string or list of strings.
            team_ids (str | list[str]): Team IDs on which to filter. Cannot be combined with team_names. Accepts a string or list of strings.
            team_names (str | list[str]): Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with team_ids. Accepts a string or list of strings.
            season_name (str | list[str]): Name(s)/year(s) of seasons. Cannot be combined with a date range. Accepts a string or list of strings.
            start_date (str): Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            end_date (str): End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            shot_pattern (str | list[str]): Describes the possessing actions leading to the shot. Valid keywords include: 'Set piece', 'Corner', 'Free kick', 'Penalty', 'Fastbreak', and 'Regular'. Accepts a string or list of strings.
            split_by_teams (bool): Logical indicator to group results by team.
            split_by_seasons (bool): Logical indicator to group results by season.
            split_by_games (bool): Logical indicator to group results by game.
            stage_name (str | list[str]): Describes the stage of competition in which a game took place. Accepts a string or list of strings.
            general_position (str | list[str]): Describes the most common position played by each player over the specified period of time. Valid keywords include: 'GK', 'CB', 'FB', 'DM', 'CM', 'AM', 'W', and 'ST'. Accepts a string or list of strings.

        Returns:
            DataFrame
        """
        player_xgoals = self._get_stats(
            leagues, stat_type="xgoals", entity="players", **kwargs
        )
        return player_xgoals

    def get_player_xpass(
        self, leagues: str | list[str] = LEAGUES, **kwargs
    ) -> DataFrame:
        """Retrieves a DataFrame containing player xPass data meeting the specified conditions.

        Args:
            leagues (str | list[str]): League(s) on which to filter. Accepts a string or list of strings. Defaults to LEAGUES.

        Keyword Args:
            minimum_minutes (int): Minimum threshold for sum of minutes played.
            minimum_passes (int): Minimum threshold for sum of attempted passes.
            player_ids (str | list[str]): Player IDs on which to filter. Cannot be combined with player_names. Accepts a string or list of strings.
            player_names (str | list[str]): Player names on which to filter. Partial matches are accepted. Cannot be combined with player_ids. Accepts a string or list of strings.
            team_ids (str | list[str]): Team IDs on which to filter. Cannot be combined with team_names. Accepts a string or list of strings.
            team_names (str | list[str]): Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with team_ids. Accepts a string or list of strings.
            season_name (str | list[str]): Name(s)/year(s) of seasons. Cannot be combined with a date range. Accepts a string or list of strings.
            start_date (str): Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            end_date (str): End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            pass_origin_third (str | list[str]): Describes the third of the field from which the pass originated. Valid keywords include: 'Attacking', 'Middle', and 'Defensive'. Accepts a string or list of strings.
            split_by_teams (bool): Logical indicator to group results by team.
            split_by_seasons (bool): Logical indicator to group results by season.
            split_by_games (bool): Logical indicator to group results by game.
            stage_name (str | list[str]): Describes the stage of competition in which a game took place. Accepts a string or list of strings.
            general_position (str | list[str]): Describes the most common position played by each player over the specified period of time. Valid keywords include: 'GK', 'CB', 'FB', 'DM', 'CM', 'AM', 'W', and 'ST'. Accepts a string or list of strings.

        Returns:
            DataFrame
        """
        player_xpass = self._get_stats(
            leagues, stat_type="xpass", entity="players", **kwargs
        )
        return player_xpass

    def get_player_goals_added(
        self, leagues: str | list[str] = LEAGUES, **kwargs
    ) -> DataFrame:
        """Retrieves a DataFrame containing player g+ data meeting the specified conditions.

        Args:
            leagues (str | list[str]): League(s) on which to filter. Accepts a string or list of strings. Defaults to LEAGUES.

        Keyword Args:
            minimum_minutes (int): Minimum threshold for sum of minutes played.
            player_ids (str | list[str]): Player IDs on which to filter. Cannot be combined with player_names. Accepts a string or list of strings.
            player_names (str | list[str]): Player names on which to filter. Partial matches are accepted. Cannot be combined with player_ids. Accepts a string or list of strings.
            team_ids (str | list[str]): Team IDs on which to filter. Cannot be combined with team_names. Accepts a string or list of strings.
            team_names (str | list[str]): Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with team_ids. Accepts a string or list of strings.
            season_name (str | list[str]): Name(s)/year(s) of seasons. Cannot be combined with a date range. Accepts a string or list of strings.
            start_date (str): Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            end_date (str): End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            split_by_teams (bool): Logical indicator to group results by team.
            split_by_seasons (bool): Logical indicator to group results by season.
            split_by_games (bool): Logical indicator to group results by game.
            stage_name (str | list[str]): Describes the stage of competition in which a game took place. Accepts a string or list of strings.
            action_type (str | list[str]): Describes the goals added (g+) action type. Valid keywords include: 'Dribbling', 'Fouling', 'Interrupting', 'Passing', 'Receiving', and 'Shooting'. Accepts a string or list of strings.
            general_position (str | list[str]): Describes the most common position played by each player over the specified period of time. Valid keywords include: 'GK', 'CB', 'FB', 'DM', 'CM', 'AM', 'W', and 'ST'. Accepts a string or list of strings.
            above_replacement (bool): Logical indicator to compare players against replacement-level values. This will only return aggregated g+ values, rather than disaggregated g+ values by action type.

        Returns:
            DataFrame
        """
        player_goals_added = self._get_stats(
            leagues, stat_type="goals-added", entity="players", **kwargs
        )
        return player_goals_added

    def get_player_salaries(
        self, leagues: str | list[str] = "mls", **kwargs
    ) -> DataFrame:
        """Retrieves a DataFrame containing player salary data meeting the specified conditions

        Args:
            leagues (str | list[str]): Leagues on which to filter. Accepts a string or list of strings. Defaults to 'mls'.

        Keyword Args:
            player_ids (str | list[str]): Player IDs on which to filter. Cannot be combined with player_names. Accepts a string or list of strings.
            player_names (str | list[str]): Player names on which to filter. Partial matches are accepted. Cannot be combined with player_ids. Accepts a string or list of strings.
            team_ids (str | list[str]): Team IDs on which to filter. Cannot be combined with team_names. Accepts a string or list of strings.
            team_names (str | list[str]): Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with team_ids. Accepts a string or list of strings.
            position (str | list[str]): Describes the general position, as reported by the players' association. Valid keywords include: 'GK', 'D', 'M', and 'F'. Accepts a string or list of strings.
            season_name (str | list[str]): Name(s)/year(s) of seasons. Cannot be combined with a date range. Accepts a string or list of strings.
            start_date (str): Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            end_date (str): End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.

        Returns:
            DataFrame
        """
        player_salaries = self._get_stats(
            leagues, stat_type="salaries", entity="players", **kwargs
        )
        return player_salaries

    def get_goalkeeper_xgoals(
        self, leagues: str | list[str] = LEAGUES, **kwargs
    ) -> DataFrame:
        """Retrieves a DataFrame containing goalkeeper xG data meeting the specified conditions.

        Args:
         leagues (str | list[str]): League(s) on which to filter. Accepts a string or list of strings. Defaults to LEAGUES.

        Keyword Args:
            minimum_minutes (int): Minimum threshold for sum of minutes played.
            minimum_shots_faced (int): Minimum threshold for sum of shots faced.
            player_ids (str | list[str]): Player IDs on which to filter. Cannot be combined with player_names. Accepts a string or list of strings.
            player_names (str | list[str]): Player names on which to filter. Partial matches are accepted. Cannot be combined with player_ids. Accepts a string or list of strings.
            team_ids (str | list[str]): Team IDs on which to filter. Cannot be combined with team_names. Accepts a string or list of strings.
            team_names (str | list[str]): Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with team_ids. Accepts a string or list of strings.
            season_name (str | list[str]): Name(s)/year(s) of seasons. Cannot be combined with a date range. Accepts a string or list of strings.
            start_date (str): Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            end_date (str): End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            shot_pattern (str | list[str]): Describes the possessing actions leading to the shot. Valid keywords include: 'Set piece', 'Corner', 'Free kick', 'Penalty', 'Fastbreak', and 'Regular'. Accepts a string or list of strings.
            split_by_teams (bool): Logical indicator to group results by team.
            split_by_seasons (bool): Logical indicator to group results by season.
            split_by_games (bool): Logical indicator to group results by game.
            stage_name (str | list[str]): Describes the stage of competition in which a game took place. Accepts a string or list of strings.

        Returns:
            DataFrame
        """
        goalkeeper_xgoals = self._get_stats(
            leagues, stat_type="xgoals", entity="goalkeepers", **kwargs
        )
        return goalkeeper_xgoals

    def get_goalkeeper_goals_added(
        self, leagues: str | list[str] = LEAGUES, **kwargs
    ) -> DataFrame:
        """Retrieves a DataFrame containing goalkeeper g+ data meeting the specified conditions.

        Args:
            leagues (str | list[str]): League(s) on which to filter. Accepts a string or list of strings. Defaults to LEAGUES.

        Keyword Args:
            minimum_minutes (int): Minimum threshold for sum of minutes played.
            player_ids (str | list[str]): Player IDs on which to filter. Cannot be combined with player_names. Accepts a string or list of strings.
            player_names (str | list[str]): Player names on which to filter. Partial matches are accepted. Cannot be combined with player_ids. Accepts a string or list of strings.
            team_ids (str | list[str]): Team IDs on which to filter. Cannot be combined with team_names. Accepts a string or list of strings.
            team_names (str | list[str]): Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with team_ids. Accepts a string or list of strings.
            season_name (str | list[str]): Name(s)/year(s) of seasons. Cannot be combined with a date range. Accepts a string or list of strings.
            start_date (str): Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            end_date (str): End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            split_by_teams (bool): Logical indicator to group results by team.
            split_by_seasons (bool): Logical indicator to group results by season.
            split_by_games (bool): Logical indicator to group results by game.
            stage_name (str | list[str]): Describes the stage of competition in which a game took place. Accepts a string or list of strings.
            action_type (str | list[str]): Describes the goals added (g+) action type. Valid keywords include: 'Dribbling', 'Fouling', 'Interrupting', 'Passing', 'Receiving', and 'Shooting'. Accepts a string or list of strings.
            above_replacement (bool): Logical indicator to compare players against replacement-level values. This will only return aggregated g+ values, rather than disaggregated g+ values by action type.

        Returns:
            DataFrame
        """
        goalkeeper_goals_added = self._get_stats(
            leagues, stat_type="goals-added", entity="goalkeepers", **kwargs
        )
        return goalkeeper_goals_added

    def get_team_xgoals(
        self, leagues: str | list[str] = LEAGUES, **kwargs
    ) -> DataFrame:
        """Retrieves a DataFrame containing team xG data meeting the specified conditions.

        Args:
            leagues (str | list[str]): Leagues on which to filter. Accepts a string or list of strings. Defaults to LEAGUES.

        Keyword Args:
            team_ids (str | list[str]): Team IDs on which to filter. Cannot be combined with team_names. Accepts a string or list of strings.
            team_names (str | list[str]): Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with team_ids. Accepts a string or list of strings.
            season_name (str | list[str]): Name(s)/year(s) of seasons. Cannot be combined with a date range. Accepts a string or list of strings.
            start_date (str): Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            end_date (str): End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            shot_pattern (str | list[str]): Describes the possessing actions leading to the shot. Valid keywords include: 'Set piece', 'Corner', 'Free kick', 'Penalty', 'Fastbreak', and 'Regular'. Accepts a string or list of strings.
            split_by_seasons (bool): Logical indicator to group results by season.
            split_by_games (bool): Logical indicator to group results by game.
            home_only (bool): Logical indicator to only include results from home games.
            away_only (bool): Logical indicator to only include results from away games.
            home_adjusted (bool): Logical indicator to adjust certain values based on the share of home games a team has played during the specified duration.
            even_game_state (bool): Logical indicator to only include shots taken when the score was level.
            stage_name (str | list[str]): Describes the stage of competition in which a game took place. Accepts a string or list of strings.

        Returns:
            DataFrame
        """
        team_xgoals = self._get_stats(leagues, stat_type="xgoals", entity="teams", **kwargs)
        return team_xgoals

    def get_team_xpass(self, leagues: str | list[str] = LEAGUES, **kwargs) -> DataFrame:
        """Retrieves a DataFrame containing team xPass data meeting the specified conditions.

        Args:
            leagues (str | list[str]): Leagues on which to filter. Accepts a string or list of strings. Defaults to LEAGUES.

        Keyword Args:
            team_ids (str | list[str]): Team IDs on which to filter. Cannot be combined with team_names. Accepts a string or list of strings.
            team_names (str | list[str]): Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with team_ids. Accepts a string or list of strings.
            season_name (str | list[str]): Name(s)/year(s) of seasons. Cannot be combined with a date range. Accepts a string or list of strings.
            start_date (str): Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            end_date (str): End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            pass_origin_third (str | list[str]): Describes the third of the field from which the pass originated. Valid keywords include: 'Attacking', 'Middle', and 'Defensive'. Accepts a string or list of strings.
            split_by_seasons (bool): Logical indicator to group results by season.
            split_by_games (bool): Logical indicator to group results by game.
            home_only (bool): Logical indicator to only include results from home games.
            away_only (bool): Logical indicator to only include results from away games.
            stage_name (str | list[str]): Describes the stage of competition in which a game took place. Accepts a string or list of strings.

        Returns:
            DataFrame
        """
        team_xpass = self._get_stats(leagues, stat_type="xpass", entity="teams", **kwargs)
        return team_xpass

    def get_team_goals_added(
        self, leagues: str | list[str] = LEAGUES, **kwargs
    ) -> DataFrame:
        """Retrieves a DataFrame containing team g+ data meeting the specified conditions.

        Args:
            leagues (str | list[str]): Leagues on which to filter. Accepts a string or list of strings. Defaults to LEAGUES.

        Keyword Args:
            team_ids (str | list[str]): Team IDs on which to filter. Cannot be combined with team_names. Accepts a string or list of strings.
            team_names (str | list[str]): Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with team_ids. Accepts a string or list of strings.
            season_name (str | list[str]): Name(s)/year(s) of seasons. Cannot be combined with a date range. Accepts a string or list of strings.
            split_by_seasons (bool): Logical indicator to group results by season.
            stage_name (str | list[str]): Describes the stage of competition in which a game took place. Accepts a string or list of strings.
            action_type (str | list[str]): Describes the goals added (g+) action type. Valid keywords include: 'Dribbling', 'Fouling', 'Interrupting', 'Passing', 'Receiving', and 'Shooting'. Accepts a string or list of strings.
            zone (int | list[int]): Zone number on pitch. Zones 1-5 are the defensive-most zones, and zones 26-30 are the attacking-most zones. Accepts a number or list of numbers.
            gamestate_trunc (int | list[int]): Integer (score differential) value between -2 and 2, inclusive. Gamestates more extreme than -2 and 2 have been included with -2 and 2, respectively. Accepts a number or list of numbers.

        Returns:
            DataFrame
        """
        team_goals_added = self._get_stats(
            leagues, stat_type="goals-added", entity="teams", **kwargs
        )
        return team_goals_added

    def get_team_salaries(
        self, leagues: str | list[str] = "mls", **kwargs
    ) -> DataFrame:
        """Retrieves a DataFrame containing team salary data meeting the specified conditions.

        Args:
            leagues (str | list[str]): Leagues on which to filter. Accepts a string or list of strings. Defaults to 'mls'.

        Keyword Args:
            team_ids (str | list[str]): Team IDs on which to filter. Cannot be combined with team_names. Accepts a string or list of strings.
            team_names (str | list[str]): Team names on which to filter. Partial matches and abbreviations are accepted. Cannot be combined with team_ids. Accepts a string or list of strings.
            season_name (str | list[str]): Name(s)/year(s) of seasons. Cannot be combined with a date range. Accepts a string or list of strings.
            split_by_teams (bool): Logical indicator to group results by team. Results must be grouped by at least one of teams, positions, or seasons. Value is True by default.
            split_by_seasons (bool): Logical indicator to group results by season. Results must be grouped by at least one of teams, positions, or seasons.
            split_by_positions (bool): Logical indicator to group results by positions. Results must be grouped by at least one of teams, positions, or seasons.

        Returns:
            DataFrame
        """
        team_salaries = self._get_stats(
            leagues, stat_type="salaries", entity="teams", **kwargs
        )
        return team_salaries

    def get_game_xgoals(
        self, leagues: str | list[str] = LEAGUES, **kwargs
    ) -> DataFrame:
        """Retrieves a DataFrame containing game xG data meeting the specified conditions.

        Args:
            leagues (str | list[str]): Leagues on which to filter. Accepts a string or list of strings. Defaults to LEAGUES.

        Keyword Args:
            game_ids (str | list[str]): Game IDs on which to filter. Accepts a string or list of strings.
            season_name (str | list[str]): Name(s)/year(s) of seasons. Cannot be combined with a date range. Accepts a string or list of strings.
            start_date (str): Start of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            end_date (str): End of a date range. Must be a string in YYYY-MM-DD format. Cannot be combined with season_name.
            stage_name (str | list[str]): Describes the stage of competition in which a game took place. Accepts a string or list of strings.

        Returns:
            DataFrame
        """
        game_xgoals = self._get_stats(leagues, stat_type="xgoals", entity="games", **kwargs)
        return game_xgoals
