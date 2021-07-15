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

    def get_stadia(self, league: str, ids: List[str] = None) -> List[Dict[str, Any]]:
        """Get information associated with stadia

        :param league: league abbreviation
        :param ids: list of stadium ids (optional)
        :returns: list of dictionaries
        """
        if ids:
            stadia_url = f"{self.base_url}{league}/stadia?stadium_id={','.join(ids)}"
        else:
            stadia_url = f"{self.base_url}{league}/stadia"
        response = self.session.get(stadia_url)
        return response.json()

    def get_referees(self, league: str, ids: List[str] = None) -> List[Dict[str, Any]]:
        """Get information associated with referees

        :param league: league abbreviation
        :param ids: list of referee ids (optional)
        :returns: list of dictionaries
        """
        if ids:
            referees_url = (
                f"{self.base_url}{league}/referees?referee_id={','.join(ids)}"
            )
        else:
            referees_url = f"{self.base_url}{league}/referees"
        response = self.session.get(referees_url)
        return response.json()

    def get_managers(self, league: str, ids: List[str] = None) -> List[Dict[str, Any]]:
        """Get information associated with managers

        :param league: league abbreviation
        :param ids: list of manager ids (optional)
        :returns: list of dictionaries
        """
        if ids:
            managers_url = (
                f"{self.base_url}{league}/managers?manager_id={','.join(ids)}"
            )
        else:
            managers_url = f"{self.base_url}{league}/managers"
        response = self.session.get(managers_url)
        return response.json()

    def get_teams(self, league: str, ids: List[str]) -> List[Dict[str, Any]]:
        """Get information associated with teams

        :param league: league abbreviation
        :param ids: team id (optional)
        :returns: list of dictionaries
        """
        if ids:
            teams_url = f"{self.base_url}{league}/teams?team_id={','.join(ids)}"
        else:
            teams_url = f"{self.base_url}{league}/teams"
        response = self.session.get(teams_url)
        return response.json()

    def get_players(self, league: str, ids: List[str]) -> List[Dict[str, Any]]:
        """Get information associated with players

        :param league: league abbreviation
        :param ids: list of player ids (optional)
        :returns: list of dictionaries
        """
        if ids:
            players_url = f"{self.base_url}{league}/players?player_id={','.join(ids)}"
        else:
            players_url = f"{self.base_url}{league}/players"
        response = self.session.get(players_url)
        return response.json()
