from os import name
import re
import requests
from typing import Dict, List, Any, Union
from cachecontrol import CacheControl
from fuzzywuzzy import fuzz, process


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
        self.players = self._get_all_ids("player")
        self.teams = self._get_all_ids("team")
        self.stadia = self._get_all_ids("stadia")
        self.managers = self._get_all_ids("manager")
        self.referees = self._get_all_ids("referee")

    def _get_all_ids(self, type: str) -> Dict[str, str]:
        """Creates a dictionary where keys are names and values
        are corresponding ids.

        :param type: type of ids to get
        :returns: dictionary
        """
        all_ids = {}
        for league in self.LEAGUES:
            if type == "stadia":
                url = f"{self.BASE_URL}{league}/{type}"
                type = "stadium"
            else:
                url = f"{self.BASE_URL}{league}/{type}s"
            response = self.session.get(url).json()
            for resp in response:
                name = resp.get(f"{type}_name", "None")
                name_id = resp.get(f"{type}_id", "None")
                all_ids.update({name: name_id})
            if type == "stadium":
                type = "stadia"
        return all_ids

    def _convert_name_to_id(self, type: str, name: str) -> Union[str, int]:
        """Converts the name of a player, manager, stadium, referee or team
        to their corresponding id.

        :param type: type of name to convert
        :param name: name
        :returns: either an int or string, depending on the type
        """
        if type == "player":
            lookup = self.players
            names = self.players.keys()
        elif type == "manager":
            lookup = self.managers
            names = self.managers.keys()
        elif type == "stadium":
            lookup = self.stadia
            names = self.stadia.keys()
        elif type == "referee":
            lookup = self.referees
            names = self.referees.keys()
        elif type == "team":
            lookup = self.teams
            names = self.teams.keys()

        matches = process.extractOne(name, names, scorer=fuzz.partial_ratio)
        lookup_id = matches[0]
        matched_id = lookup.get(lookup_id)
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

    def get_stadia(
        self, league: str, names: Union[str, List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Get information associated with stadia

        :param league: league abbreviation
        :param names: a single stadium name or a list of stadia names (optional)
        :returns: list of dictionaries
        """
        ids = self._convert_names_to_ids("stadium", names)
        if isinstance(ids, str):
            stadia_url = f"{self.base_url}{league}/stadia?stadium_id={ids}"
        elif isinstance(ids, list):
            stadia_url = f"{self.base_url}{league}/stadia?stadium_id={','.join(ids)}"
        else:
            stadia_url = f"{self.base_url}{league}/stadia"
        response = self.session.get(stadia_url)
        return response.json()

    def get_referees(
        self, league: str, names: Union[str, List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Get information associated with referees

        :param league: league abbreviation
        :param names: a single referee name or a list of referee names (optional)
        :returns: list of dictionaries
        """
        ids = self._convert_names_to_ids("referee", names)
        if isinstance(ids, str):
            referees_url = f"{self.base_url}{league}/referees?referee_id={ids}"
        elif isinstance(ids, list):
            referees_url = (
                f"{self.base_url}{league}/referees?referee_id={','.join(ids)}"
            )
        else:
            referees_url = f"{self.base_url}{league}/referees"
        response = self.session.get(referees_url)
        return response.json()

    def get_managers(
        self, league: str, names: Union[str, List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Get information associated with managers

        :param league: league abbreviation
        :param names: a single manager name or list of manager names (optional)
        :returns: list of dictionaries
        """
        ids = self._convert_names_to_ids("manager", names)
        if isinstance(ids, str):
            managers_url = f"{self.base_url}{league}/managers?manager_id={ids}"
        elif isinstance(ids, list):
            managers_url = (
                f"{self.base_url}{league}/managers?manager_id={','.join(ids)}"
            )
        else:
            managers_url = f"{self.base_url}{league}/managers"
        response = self.session.get(managers_url)
        return response.json()

    def get_teams(
        self, league: str, names: Union[str, List[str]]
    ) -> List[Dict[str, Any]]:
        """Get information associated with teams

        :param league: league abbreviation
        :param names: a single team name or list of team names (optional)
        :returns: list of dictionaries
        """
        ids = self._convert_names_to_ids("team", names)
        if isinstance(ids, str):
            teams_url = f"{self.base_url}{league}/teams?team_id={ids}"
        if isinstance(ids, list):
            teams_url = f"{self.base_url}{league}/teams?team_id={','.join(ids)}"
        else:
            teams_url = f"{self.base_url}{league}/teams"
        response = self.session.get(teams_url)
        return response.json()

    def get_players(
        self, league: str, names: Union[str, List[str]]
    ) -> List[Dict[str, Any]]:
        """Get information associated with players

        :param league: league abbreviation
        :param names: a single player name or list of player names (optional)
        :returns: list of dictionaries
        """
        ids = self._convert_names_to_ids("player", names)
        if isinstance(ids, str):
            players_url = f"{self.base_url}{league}/players?player_id={ids}"
        if isinstance(ids, list):
            players_url = f"{self.base_url}{league}/players?player_id={','.join(ids)}"
        else:
            players_url = f"{self.base_url}{league}/players"
        response = self.session.get(players_url)
        return response.json()
