import requests
from typing import Dict, List, Any, Union
from cachecontrol import CacheControl
from fuzzywuzzy import fuzz, process
import pandas as pd
import json


class AmericanSoccerAnalysis:
    """Wrapper around the ASA Shiny API"""

    API_VERSION = "v1"
    BASE_URL = f"https://app.americansocceranalysis.com/api/{API_VERSION}/"
    LEAGUES = ["nwsl", "mls", "uslc", "usl1", "nasl"]

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

    def _check_leagues(self, leagues: Union[str, List[str]]):
        """Validates the leagues parameter

        :param leagues: league abbreviation or list of league abbreviations
        """
        if isinstance(leagues, list):
            if not all(l in leagues for l in self.LEAGUES):
                print(
                    f"Leagues are limited only to the following options: {self.LEAGUES.join(',')}."
                )
                exit()
        else:
            if leagues not in self.LEAGUES:
                print(
                    f"Leagues are limited only to the following options: {self.LEAGUES.join(',')}."
                )
                exit()

    def _check_ids_names(
        self, ids: Union[str, List[str]], names: Union[str, List[str]]
    ):
        """Makes sure only ids or names are passed to a function and verifies
        they are the right data type.

        :param ids: a single id or list of ids
        :param names: a single name or list of names
        """
        if ids and names:
            print("Please specify only IDs or names, not both.")
            exit()

        if ids:
            if not isinstance(ids, str) and not isinstance(ids, list):
                print("IDs must be passed as a string or list of strings.")
                exit()

        if names:
            if not isinstance(names, str) and not isinstance(names, list):
                print("Names must be passed as a string or list of names.")
                exit()

    def _filter_entity(
        self,
        entity_all: pd.DataFrame,
        entity_type: str,
        leagues: Union[str, List[str]],
        ids: Union[str, List[str]] = None,
        names: Union[str, List[str]] = None,
    ) -> List[Dict[str, Any]]:
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

        return entity.to_json(orient="records")

    def get_stadia(
        self,
        leagues: Union[str, List[str]],
        ids: Union[str, List[str]] = None,
        names: Union[str, List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Get information associated with stadia

        :param leagues: league abbreviation or a list of league abbreviations
        :param ids: a single stadium id or a list of stadia ids (optional)
        :param names: a single stadium name or a list of stadia names (optional)
        :returns: list of dictionaries
        """
        stadia = self._filter_entity(self.stadia, "stadium", leagues, ids, names)
        return stadia

    def get_referees(
        self,
        leagues: Union[str, List[str]],
        ids: Union[str, List[str]] = None,
        names: Union[str, List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Get information associated with referees

        :param leagues: league abbreviation or a list of league abbreviations
        :param ids: a single referee id or a list of referee ids (optional)
        :param names: a single referee name or a list of referee names (optional)
        :returns: list of dictionaries
        """
        referees = self._filter_entity(self.referees, "referee", leagues, ids, names)
        return referees

    def get_managers(
        self,
        leagues: Union[str, List[str]],
        ids: Union[str, List[str]] = None,
        names: Union[str, List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Get information associated with managers

        :param leagues: league abbreviation or a list of league abbreviations
        :param ids: a single referee id or a list of referee ids (optional)
        :param names: a single referee name or a list of referee names (optional)
        :returns: list of dictionaries
        """
        managers = self._filter_entity(self.managers, "manager", leagues, ids, names)
        return managers

    def get_teams(
        self,
        leagues: Union[str, List[str]],
        ids: Union[str, List[str]] = None,
        names: Union[str, List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Get information associated with teams

        :param leagues: league abbreviation or a list of league abbreviations
        :param ids: a single team id or a list of team ids (optional)
        :param names: a single team name or a list of team names (optional)
        :returns: list of dictionaries
        """
        teams = self._filter_entity(self.teams, "team", leagues, ids, names)
        return teams

    def get_players(
        self,
        leagues: Union[str, List[str]],
        ids: Union[str, List[str]] = None,
        names: Union[str, List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Get information associated with players

        :param league: league abbreviation or a list of league abbreviations
        :param ids: a single player id or a list of player ids (optional)
        :param names: a single player name or a list of player names (optional)
        :returns: list of dictionaries
        """
        players = self._filter_entity(self.players, "player", leagues, ids, names)
        return players
