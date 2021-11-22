import requests
from typing import Dict, List, Union
from cachecontrol import CacheControl
from fuzzywuzzy import fuzz, process
import pandas as pd
import json


class AmericanSoccerAnalysis:
    """Wrapper around the ASA Shiny API"""

    API_VERSION = "v1"
    BASE_URL = f"https://app.americansocceranalysis.com/api/{API_VERSION}/"
    LEAGUES = ["nwsl", "mls", "uslc", "usl1", "nasl"]
    MAX_API_LIMIT = 1000

    def __init__(self) -> None:
        """Class constructor"""
        SESSION = requests.session()
        CACHE_SESSION = CacheControl(SESSION)

        self.session = CACHE_SESSION
        self.base_url = self.BASE_URL
        self.players = self._get_all("player")
        self.teams = self._get_all("team")
        self.stadia = self._get_all("stadia")
        self.managers = self._get_all("manager")
        self.referees = self._get_all("referee")

    def _get_all(self, type: str) -> pd.DataFrame:
        """Gets all the data for a specific type and
        stores it in a dataframe.

        :param type: type of data to get
        :returns: dataframe
        """
        df = pd.DataFrame([])
        for league in self.LEAGUES:
            if type == "stadia":
                url = f"{self.BASE_URL}{league}/stadia"
            else:
                url = f"{self.BASE_URL}{league}/{type}s"
            response = self.session.get(url).json()
            # Convert list of objects to JSON
            resp_df = pd.read_json(json.dumps(response, default=lambda x: x.__dict__))
            resp_df = resp_df.assign(competition=league)
            df = df.append(resp_df)
        return df

    def _convert_name_to_id(self, type: str, name: str) -> Union[str, int]:
        """Converts the name of a player, manager, stadium, referee or team
        to their corresponding id.

        :param type: type of name to convert
        :param name: name
        :returns: either an int or string, depending on the type
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
                print(f"No match found for {name} due to score")
                return ""
        else:
            print(f"No match found for {name}")
            return ""
        matched_id = lookup.loc[lookup[f"{type}_name"] == name, f"{type}_id"].iloc[0]
        return matched_id

    def _convert_names_to_ids(
        self, type: str, names: Union[str, None]
    ) -> Union[str, List[str]]:
        """Converts a name or list of names to an id or list of ids

        :param type: type of name
        :param names: a name or list of names
        :returns: an id or list of ids
        """
        ids = []
        if names is None:
            return None
        if isinstance(names, str):
            return self._convert_name_to_id(type, names)
        else:
            for n in names:
                ids.append(self._convert_name_to_id(type, n))
            return ids

    def _check_leagues(self, leagues: Union[str, List[str]]) -> None:
        """Validates the leagues parameter

        :param leagues: league abbreviation or list of league abbreviations
        """
        if isinstance(leagues, list):
            for l in leagues:
                if l not in self.LEAGUES:
                    print(
                        f"Leagues are limited only to the following options: {self.LEAGUES}."
                    )
                    raise SystemExit(1)
        else:
            if leagues not in self.LEAGUES:
                print(
                    f"Leagues are limited only to the following options: {self.LEAGUES}."
                )
                raise SystemExit(1)

    def _check_ids_names(
        self, ids: Union[str, List[str]], names: Union[str, List[str]]
    ) -> None:
        """Makes sure only ids or names are passed to a function and verifies
        they are the right data type.

        :param ids: a single id or list of ids
        :param names: a single name or list of names
        """
        if ids and names:
            print("Please specify only IDs or names, not both.")
            raise SystemExit(1)

        if ids:
            if not isinstance(ids, str) and not isinstance(ids, list):
                print("IDs must be passed as a string or list of strings.")
                raise SystemExit(1)

        if names:
            if not isinstance(names, str) and not isinstance(names, list):
                print("Names must be passed as a string or list of names.")
                raise SystemExit(1)

    def _filter_entity(
        self,
        entity_all: pd.DataFrame,
        entity_type: str,
        leagues: Union[str, List[str]],
        ids: Union[str, List[str]] = None,
        names: Union[str, List[str]] = None,
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

        entity = entity[entity["competition"].isin(leagues)]

        if converted_ids:
            entity = entity[entity[f"{entity_type}_id"].isin(converted_ids)]

        return entity

    def _execute_query(self, url: str, params: Dict[str,List[str]]) -> pd.DataFrame:
        """Executes a query while handling the max number of responses from the API

        :param url: the API endpoint to call
        :param params: URL query strings
        :returns: Dataframe
        """
        temp_response = self._single_request(url, params)
        response = temp_response

        if (isinstance(response, pd.DataFrame)):
            offset = self.MAX_API_LIMIT

            while(len(temp_response) == self.MAX_API_LIMIT):
                params["offset"] = offset
                temp_response = self._execute_query(url, params)
                response = response.append(temp_response)
                offset = offset + self.MAX_API_LIMIT
        
        return response

    def _single_request(self, url: str, params: Dict[str, List[str]]) -> pd.DataFrame:
        """Handles single call to the API

        :param url: the API endpoint to call
        :param params: URL query strings
        :returns: Dataframe
        """
        response = self.session.get(url=url, params=params)
        response.raise_for_status()
        resp_df = pd.read_json(json.dumps(response.json()))
        return resp_df

    def get_stadia(
        self,
        leagues: Union[str, List[str]],
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
        leagues: Union[str, List[str]],
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
        leagues: Union[str, List[str]],
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
        leagues: Union[str, List[str]],
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
        leagues: Union[str, List[str]],
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
        leagues: Union[str, List[str]],
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

        query = {}

        if game_ids:
            query["game_id"] = game_ids
        if team_names:
            query["team_id"] = self._convert_names_to_ids("team",team_names)
        if team_ids:
            query["team_id"] = team_ids
        if seasons:
            query["season_name"] = seasons
        if stages:
            query["stage_name"] = stages

        games = pd.DataFrame([])
        if isinstance(leagues, str):
            games_url = f"{self.base_url}{leagues}/games"
            response = self._execute_query(games_url, query)

            games = games.append(response)
        elif isinstance(leagues, list):
            for league in leagues:
                games_url = f"{self.base_url}{league}/games"
                response = self._execute_query(games_url, query)

                games = games.append(response)

        return games.sort_values(by=["date_time_utc"], ascending=False)