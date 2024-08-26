from pathlib import Path
from unittest.mock import patch

from pandas import DataFrame, read_json
from pytest import fixture

from itscalledsoccer.client import AmericanSoccerAnalysis


@fixture(scope="session")
@patch("itscalledsoccer.client.AmericanSoccerAnalysis._get_entity")
def init_client(self):
    return AmericanSoccerAnalysis()


class TestClient:
    def test_init(self, init_client):
        self.client = init_client
        assert self.client.API_VERSION == "v1"
        assert self.client.BASE_URL == "https://app.americansocceranalysis.com/api/v1/"
        assert self.client.MAX_API_LIMIT == 1000
        assert self.client.LEAGUES == ["nwsl", "mls", "uslc", "usl1", "nasl", "mlsnp"]
        assert self.client.LOGGER is not None
        assert self.client.LOGGER.getEffectiveLevel() == 30

    @patch("itscalledsoccer.client.AmericanSoccerAnalysis._get_entity")
    def test_proxy(self, mock_entity):
        proxies = {"http": "http://foo", "https": "https://bar"}
        self.client = AmericanSoccerAnalysis(proxies=proxies)
        assert self.client.session.proxies == proxies

    @patch("itscalledsoccer.client.AmericanSoccerAnalysis._get_entity")
    def test_logging_level(self, mock_entity):
        self.client = AmericanSoccerAnalysis(logging_level="DEBUG")
        assert self.client.LOGGER.getEffectiveLevel() == 10

    def load_mock_data(self, func_name: str):
        path = Path(__file__).parent
        file = Path(path, f"./mocks/{func_name}_payload.json")
        return read_json(file)

    def test_get_player_xgoals(self, init_client):
        self.client = init_client
        with patch(
            "itscalledsoccer.client.AmericanSoccerAnalysis._get_stats"
        ) as mock_stats:
            mock_stats.return_value = self.load_mock_data("players_xgoals")
            data = self.client.get_player_xgoals()
            assert data is not None
            assert isinstance(data, DataFrame)
            assert len(data) >= 2

    def test_get_player_xpass(self, init_client):
        self.client = init_client
        with patch(
            "itscalledsoccer.client.AmericanSoccerAnalysis._get_stats"
        ) as mock_stats:
            mock_stats.return_value = self.load_mock_data("players_xpass")
            data = self.client.get_player_xpass()
            assert data is not None
            assert isinstance(data, DataFrame)
            assert len(data) >= 2

    def test_get_player_goals_added(self, init_client):
        self.client = init_client
        with patch(
            "itscalledsoccer.client.AmericanSoccerAnalysis._get_stats"
        ) as mock_stats:
            mock_stats.return_value = self.load_mock_data("players_goals_added")
            data = self.client.get_player_goals_added()
            assert data is not None
            assert isinstance(data, DataFrame)
            assert len(data) >= 2

    def test_get_player_salaries(self, init_client):
        self.client = init_client
        with patch(
            "itscalledsoccer.client.AmericanSoccerAnalysis._get_stats"
        ) as mock_stats:
            mock_stats.return_value = self.load_mock_data("players_salaries")
            data = self.client.get_player_salaries()
            assert data is not None
            assert isinstance(data, DataFrame)
            assert len(data) >= 2

    def test_get_goalkeeper_xgoals(self, init_client):
        self.client = init_client
        with patch(
            "itscalledsoccer.client.AmericanSoccerAnalysis._get_stats"
        ) as mock_stats:
            mock_stats.return_value = self.load_mock_data("goalkeepers_xgoals")
            data = self.client.get_goalkeeper_xgoals()
            assert data is not None
            assert isinstance(data, DataFrame)
            assert len(data) >= 2

    def test_get_goalkeeper_goals_added(self, init_client):
        self.client = init_client
        with patch(
            "itscalledsoccer.client.AmericanSoccerAnalysis._get_stats"
        ) as mock_stats:
            mock_stats.return_value = self.load_mock_data("goalkeepers_goals_added")
            data = self.client.get_goalkeeper_goals_added()
            assert data is not None
            assert isinstance(data, DataFrame)
            assert len(data) >= 2

    def test_get_team_xgoals(self, init_client):
        self.client = init_client
        with patch(
            "itscalledsoccer.client.AmericanSoccerAnalysis._get_stats"
        ) as mock_stats:
            mock_stats.return_value = self.load_mock_data("teams_xgoals")
            data = self.client.get_team_xgoals()
            assert data is not None
            assert isinstance(data, DataFrame)
            assert len(data) >= 2

    def test_get_team_xpass(self, init_client):
        self.client = init_client
        with patch(
            "itscalledsoccer.client.AmericanSoccerAnalysis._get_stats"
        ) as mock_stats:
            mock_stats.return_value = self.load_mock_data("teams_xpass")
            data = self.client.get_team_xpass()
            assert data is not None
            assert isinstance(data, DataFrame)
            assert len(data) >= 2

    def test_get_team_goals_added(self, init_client):
        self.client = init_client
        with patch(
            "itscalledsoccer.client.AmericanSoccerAnalysis._get_stats"
        ) as mock_stats:
            mock_stats.return_value = self.load_mock_data("teams_goals_added")
            data = self.client.get_team_goals_added()
            assert data is not None
            assert isinstance(data, DataFrame)
            assert len(data) >= 2

    def test_get_team_salaries(self, init_client):
        self.client = init_client
        with patch(
            "itscalledsoccer.client.AmericanSoccerAnalysis._get_stats"
        ) as mock_stats:
            mock_stats.return_value = self.load_mock_data("teams_salaries")
            data = self.client.get_team_salaries()
            assert data is not None
            assert isinstance(data, DataFrame)
            assert len(data) >= 2

    def test_get_game_xgoals(self, init_client):
        self.client = init_client
        with patch(
            "itscalledsoccer.client.AmericanSoccerAnalysis._get_stats"
        ) as mock_stats:
            mock_stats.return_value = self.load_mock_data("games_xgoals")
            data = self.client.get_game_xgoals()
            assert data is not None
            assert isinstance(data, DataFrame)
            assert len(data) >= 2

    def test_get_stadia(self):
        with patch(
            "itscalledsoccer.client.AmericanSoccerAnalysis._get_entity"
        ) as mock_entity:
            mock_entity.return_value = self.load_mock_data("stadia")
            self.client = AmericanSoccerAnalysis()
            stadia = self.client.get_stadia()
            assert stadia is not None
            assert isinstance(stadia, DataFrame)
            assert len(stadia) >= 2

    def test_get_referees(self):
        with patch(
            "itscalledsoccer.client.AmericanSoccerAnalysis._get_entity"
        ) as mock_entity:
            mock_entity.return_value = self.load_mock_data("referees")
            self.client = AmericanSoccerAnalysis()
            referees = self.client.get_referees()
            assert referees is not None
            assert isinstance(referees, DataFrame)
            assert len(referees) >= 2

    def test_get_managers(self):
        with patch(
            "itscalledsoccer.client.AmericanSoccerAnalysis._get_entity"
        ) as mock_entity:
            mock_entity.return_value = self.load_mock_data("managers")
            self.client = AmericanSoccerAnalysis()
            managers = self.client.get_managers()
            assert managers is not None
            assert isinstance(managers, DataFrame)
            assert len(managers) >= 2

    def test_get_teams(self):
        with patch(
            "itscalledsoccer.client.AmericanSoccerAnalysis._get_entity"
        ) as mock_entity:
            mock_entity.return_value = self.load_mock_data("teams")
            self.client = AmericanSoccerAnalysis()
            teams = self.client.get_teams()
            assert teams is not None
            assert isinstance(teams, DataFrame)
            assert len(teams) >= 2

    def test_get_players(self):
        with patch(
            "itscalledsoccer.client.AmericanSoccerAnalysis._get_entity"
        ) as mock_entity:
            mock_entity.return_value = self.load_mock_data("players")
            self.client = AmericanSoccerAnalysis()
            players = self.client.get_players()
            assert players is not None
            assert isinstance(players, DataFrame)
            assert len(players) >= 2

    def test_get_games(self):
        with patch(
            "itscalledsoccer.client.AmericanSoccerAnalysis._get_entity"
        ) as mock_entity:
            mock_entity.return_value = self.load_mock_data("games")
            self.client = AmericanSoccerAnalysis()
            games = self.client.get_games()
            assert games is not None
            assert isinstance(games, DataFrame)
            assert len(games) >= 2
