from pathlib import Path
from unittest.mock import patch

import pytest
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
        assert self.client.LEAGUES == ["nwsl", "mls", "uslc", "usl1", "usls", "nasl", "mlsnp"]
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
            self.client = AmericanSoccerAnalysis(lazy_load=False)
            stadia = self.client.get_stadia()
            assert stadia is not None
            assert isinstance(stadia, DataFrame)
            assert len(stadia) >= 2

    def test_get_referees(self):
        with patch(
            "itscalledsoccer.client.AmericanSoccerAnalysis._get_entity"
        ) as mock_entity:
            mock_entity.return_value = self.load_mock_data("referees")
            self.client = AmericanSoccerAnalysis(lazy_load=False)
            referees = self.client.get_referees()
            assert referees is not None
            assert isinstance(referees, DataFrame)
            assert len(referees) >= 2

    def test_get_managers(self):
        with patch(
            "itscalledsoccer.client.AmericanSoccerAnalysis._get_entity"
        ) as mock_entity:
            mock_entity.return_value = self.load_mock_data("managers")
            self.client = AmericanSoccerAnalysis(lazy_load=False)
            managers = self.client.get_managers()
            assert managers is not None
            assert isinstance(managers, DataFrame)
            assert len(managers) >= 2

    def test_get_teams(self):
        with patch(
            "itscalledsoccer.client.AmericanSoccerAnalysis._get_entity"
        ) as mock_entity:
            mock_entity.return_value = self.load_mock_data("teams")
            self.client = AmericanSoccerAnalysis(lazy_load=False)
            teams = self.client.get_teams()
            assert teams is not None
            assert isinstance(teams, DataFrame)
            assert len(teams) >= 2

    def test_get_players(self):
        with patch(
            "itscalledsoccer.client.AmericanSoccerAnalysis._get_entity"
        ) as mock_entity:
            mock_entity.return_value = self.load_mock_data("players")
            self.client = AmericanSoccerAnalysis(lazy_load=False)
            players = self.client.get_players()
            assert players is not None
            assert isinstance(players, DataFrame)
            assert len(players) >= 2

    def test_get_games(self):
        with patch(
            "itscalledsoccer.client.AmericanSoccerAnalysis._execute_query"
        ) as mock_query:
            mock_query.return_value = self.load_mock_data("games")
            self.client = AmericanSoccerAnalysis(lazy_load=False)
            games = self.client.get_games()
            assert games is not None
            assert isinstance(games, DataFrame)
            assert len(games) >= 2

    def test_convert_names_to_ids_with_string(self):
        self.client = AmericanSoccerAnalysis()
        self.client.players = DataFrame(
            [
                {"player_id": "p1", "player_name": "Alex Morgan", "competition": "mls"},
                {"player_id": "p2", "player_name": "Megan Rapinoe", "competition": "nwsl"},
            ]
        )

        player_id = self.client._convert_names_to_ids("player", "Alex Morgan")

        assert player_id == "p1"

    def test_convert_names_to_ids_with_list(self):
        self.client = AmericanSoccerAnalysis()
        self.client.teams = DataFrame(
            [
                {"team_id": "t1", "team_name": "LAFC", "competition": "mls"},
                {"team_id": "t2", "team_name": "NYCFC", "competition": "mls"},
            ]
        )

        team_ids = self.client._convert_names_to_ids("team", ["LAFC", "NYCFC"])

        assert team_ids == ["t1", "t2"]

    def test_check_leagues_invalid(self, init_client):
        self.client = init_client

        with pytest.raises(ValueError, match="is not valid"):
            self.client._check_leagues("invalid_league")

    def test_check_leagues_salaries_invalid(self, init_client):
        self.client = init_client

        with pytest.raises(ValueError, match="Only MLS salary data is publicly available"):
            self.client._check_leagues_salaries("nwsl")

    def test_check_ids_names_both_values(self, init_client):
        self.client = init_client

        with pytest.raises(ValueError, match="only IDs or names"):
            self.client._check_ids_names("123", "Jane Doe")

    def test_filter_entity_by_names_and_leagues(self, init_client):
        self.client = init_client
        self.client.teams = DataFrame(
            [
                {"team_id": "t1", "team_name": "LAFC", "competition": "mls"},
                {"team_id": "t2", "team_name": "Portland Timbers", "competition": "mls"},
                {"team_id": "t3", "team_name": "Angel City", "competition": "nwsl"},
            ]
        )

        filtered = self.client._filter_entity(
            self.client.teams, "team", "mls", names="LAFC"
        )

        assert len(filtered) == 1
        assert filtered.iloc[0]["team_id"] == "t1"

    def test_execute_query_handles_list_params_and_pagination(self):
        self.client = AmericanSoccerAnalysis()
        self.client.MAX_API_LIMIT = 2

        first = DataFrame([{"value": 1}, {"value": 2}])
        second = DataFrame([{"value": 3}])

        def side_effect(url, params):
            return first if "offset" not in params else second

        with patch.object(self.client, "_single_request", side_effect=side_effect) as mock_single:
            result = self.client._execute_query("http://example.com/api", {"ids": ["a", "b"]})

        assert result.shape[0] == 3
        assert list(result["value"]) == [1, 2, 3]
        assert mock_single.call_count == 2
        assert mock_single.call_args_list[0].args[1]["ids"] == "a,b"

    def test_get_team_salaries_sets_split_by_teams_by_default(self):
        self.client = AmericanSoccerAnalysis()
        with patch(
            "itscalledsoccer.client.AmericanSoccerAnalysis._execute_query"
        ) as mock_execute:
            mock_execute.return_value = DataFrame([{"team_id": "t1"}])
            self.client.get_team_salaries()

        assert mock_execute.call_count == 1
        args, _ = mock_execute.call_args
        assert args[1]["split_by_teams"] is True

    def test_get_games_converts_team_names_to_ids(self):
        self.client = AmericanSoccerAnalysis()
        with patch.object(
            self.client, "_convert_names_to_ids", return_value=["t1"]
        ) as mock_convert, patch(
            "itscalledsoccer.client.AmericanSoccerAnalysis._execute_query"
        ) as mock_execute:
            mock_execute.return_value = DataFrame(
                [
                    {"game_id": "g1", "date_time_utc": "2026-01-01T00:00:00Z"}
                ]
            )
            self.client.get_games(leagues="mls", team_names="LAFC")

        mock_convert.assert_called_once_with("team", "LAFC")
        args, _ = mock_execute.call_args
        assert args[1]["team_id"] == ["t1"]
