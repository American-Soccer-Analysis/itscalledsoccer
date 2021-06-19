import requests
from typing import Dict, List, Any
from cachecontrol import CacheControl


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
        self.referess = self._get_all_ids("referee")

    def _get_all_ids(self, type: str) -> Dict[str, str]:
        """Creates a dictionary where keys are ids and values
        are corresponding names.

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
                all_ids.update({resp[f"{type}_id"]: resp[f"{type}_name"]})
        return all_ids

    def get_stadia(self, league: str, id: str = None) -> List[Dict[str, Any]]:
        """Get information associated with stadia

        :param league: league abbreviation
        :param id: stadium id (optional)
        :returns: list of dictionaries
        """
        if id:
            stadia_url = f"{self.base_url}{league}/stadia?stadium_id={id}"
        else:
            stadia_url = f"{self.base_url}{league}/stadia"
        response = self.session.get(stadia_url)
        return response.json()

    def get_referees(self, league: str, id: str = None) -> List[Dict[str, Any]]:
        """Get information associated with referees

        :param league: league abbreviation
        :param id: referee id (optional)
        :returns: list of dictionaries
        """
        if id:
            referees_url = f"{self.base_url}{league}/referees?referee_id={id}"
        else:
            referees_url = f"{self.base_url}{league}/referees"
        response = self.session.get(referees_url)
        return response.json()

    def get_managers(self, league: str, id: str = None) -> List[Dict[str, Any]]:
        """Get information associated with managers

        :param league: league abbreviation
        :param id: manager id (optional)
        :returns: list of dictionaries
        """
        if id:
            managers_url = f"{self.base_url}{league}/managers?manager_id={id}"
        else:
            managers_url = f"{self.base_url}{league}/managers"
        response = self.session.get(managers_url)
        return response.json()

    def get_teams(self, league: str) -> List[Dict[str, Any]]:
        """Get information associated with teams

        :param league: league abbreviation
        :param id: team id (optional)
        :returns: list of dictionaries
        """
        teams_url = f"{self.base_url}{league}/teams"
        response = self.session.get(teams_url)
        return response.json()

    def get_players(self, league: str) -> List[Dict[str, Any]]:
        """Get information associated with players

        :param league: league abbreviation
        :param id: player id (optional)
        :returns: list of dictionaries
        """
        players_url = f"{self.base_url}{league}/players"
        response = self.session.get(players_url)
        return response.json()
