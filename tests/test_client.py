from pathlib import Path
from unittest.mock import patch

import pytest
from pandas import DataFrame, read_json
from pytest import fixture

from itscalledsoccer.client import AmericanSoccerAnalysis
from itscalledsoccer import AmericanSoccerAnalysis as ASAFromPackage
from itscalledsoccer.errors import (
    ConflictingParametersError,
    InvalidLeagueError,
    InvalidParameterFormatError,
    InvalidSeasonError,
    SalaryDataError,
)


@fixture(scope="session")
@patch("itscalledsoccer.client.AmericanSoccerAnalysis._get_entity")
def init_client(self):
    return AmericanSoccerAnalysis()


class TestClient:
    def test_import_from_package_init(self):
        assert ASAFromPackage is AmericanSoccerAnalysis
        assert ASAFromPackage.__name__ == "AmericanSoccerAnalysis"

    def test_custom_exceptions_exported_from_package(self):
        import itscalledsoccer
        
        assert hasattr(itscalledsoccer, 'InvalidLeagueError')
        assert hasattr(itscalledsoccer, 'SalaryDataError')
        assert hasattr(itscalledsoccer, 'ConflictingParametersError')
        assert hasattr(itscalledsoccer, 'InvalidParameterFormatError')
        assert hasattr(itscalledsoccer, 'InvalidEntityTypeError')
        assert hasattr(itscalledsoccer, 'ASAError')

    def test_init(self, init_client):
        self.client = init_client
        assert self.client.API_VERSION == "v1"
        assert self.client.BASE_URL == "https://app.americansocceranalysis.com/api/v1/"
        assert self.client.MAX_API_LIMIT == 1000
        assert self.client.LEAGUES == ["nwsl", "mls", "uslc", "usl1", "usls", "nasl", "mlsnp"]
        assert self.client.logger is not None
        assert self.client.logger.getEffectiveLevel() == 30

    @patch("itscalledsoccer.client.AmericanSoccerAnalysis._get_entity")
    def test_proxy(self, mock_entity):
        proxies = {"http": "http://foo", "https": "https://bar"}
        self.client = AmericanSoccerAnalysis(proxies=proxies)
        assert self.client.session.proxies == proxies

    @patch("itscalledsoccer.client.AmericanSoccerAnalysis._get_entity")
    def test_logging_level(self, mock_entity):
        self.client = AmericanSoccerAnalysis(logging_level="DEBUG")
        assert self.client.logger.getEffectiveLevel() == 10

    @patch("itscalledsoccer.client.AmericanSoccerAnalysis._get_entity")
    def test_logger_isolation_different_instances(self, mock_entity):
        client1 = AmericanSoccerAnalysis(logging_level="DEBUG")
        client2 = AmericanSoccerAnalysis(logging_level="WARNING")
        
        assert client1.logger is not client2.logger
        assert client1.logger.getEffectiveLevel() == 10
        assert client2.logger.getEffectiveLevel() == 30

    @patch("itscalledsoccer.client.AmericanSoccerAnalysis._get_entity")
    def test_logger_names_unique_per_instance(self, mock_entity):
        client1 = AmericanSoccerAnalysis()
        client2 = AmericanSoccerAnalysis()
        
        assert client1.logger.name != client2.logger.name
        assert str(id(client1)) in client1.logger.name
        assert str(id(client2)) in client2.logger.name

    @patch("itscalledsoccer.client.AmericanSoccerAnalysis._get_entity")
    def test_logger_isolation_logging_levels_independent(self, mock_entity):
        client1 = AmericanSoccerAnalysis(logging_level="DEBUG")
        client2 = AmericanSoccerAnalysis(logging_level="ERROR")
        client3 = AmericanSoccerAnalysis(logging_level="INFO")
        
        assert client1.logger.getEffectiveLevel() == 10
        assert client2.logger.getEffectiveLevel() == 40
        assert client3.logger.getEffectiveLevel() == 20

    @patch("itscalledsoccer.client.HTTPAdapter")
    @patch("itscalledsoccer.client.AmericanSoccerAnalysis._get_entity")
    def test_retry_strategy_configuration(self, mock_entity, mock_http_adapter_class):
        with patch("itscalledsoccer.client.Retry") as mock_retry_class:
            mock_retry_instance = mock_retry_class.return_value
            
            self.client = AmericanSoccerAnalysis()
            
            # Verify Retry was instantiated with correct parameters
            mock_retry_class.assert_called_once_with(
                total=3,
                backoff_factor=0.5,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=["GET"],
            )
            
            # Verify HTTPAdapter was instantiated with the retry strategy
            mock_http_adapter_class.assert_called_once_with(max_retries=mock_retry_instance)

    @patch("itscalledsoccer.client.AmericanSoccerAnalysis._get_entity")
    def test_retry_strategy_defaults(self, mock_entity):
        # Verify that the retry strategy is set with expected defaults
        self.client = AmericanSoccerAnalysis()
        
        # The session should be a CacheControl instance wrapping a requests session
        assert self.client.session is not None
        assert hasattr(self.client.session, 'get')

    @patch("itscalledsoccer.client.AmericanSoccerAnalysis._get_entity")
    def test_request_timeout_default(self, mock_entity):
        self.client = AmericanSoccerAnalysis()
        assert self.client.request_timeout == 30

    @patch("itscalledsoccer.client.AmericanSoccerAnalysis._get_entity")
    def test_request_timeout_custom(self, mock_entity):
        custom_timeout = 60
        self.client = AmericanSoccerAnalysis(request_timeout=custom_timeout)
        assert self.client.request_timeout == custom_timeout

    def test_request_timeout_applied_to_request(self, init_client):
        self.client = init_client
        with patch.object(self.client.session, 'get') as mock_get:
            mock_get.return_value.json.return_value = [{"value": 1}]
            self.client._single_request("http://example.com/api", {})
            
            # Verify timeout was passed to the get request
            mock_get.assert_called_once()
            args, kwargs = mock_get.call_args
            assert kwargs['timeout'] == 30

    def test_request_timeout_custom_applied_to_request(self):
        with patch("itscalledsoccer.client.AmericanSoccerAnalysis._get_entity"):
            custom_timeout = 45
            self.client = AmericanSoccerAnalysis(request_timeout=custom_timeout)
            
            with patch.object(self.client.session, 'get') as mock_get:
                mock_get.return_value.json.return_value = [{"value": 1}]
                self.client._single_request("http://example.com/api", {})
                
                # Verify custom timeout was passed to the get request
                mock_get.assert_called_once()
                args, kwargs = mock_get.call_args
                assert kwargs['timeout'] == custom_timeout

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

    def test_convert_name_to_id_lazy_loads_missing_entity(self):
        self.client = AmericanSoccerAnalysis()
        teams = DataFrame(
            [
                {"team_id": "t1", "team_name": "LAFC", "competition": "mls"},
                {"team_id": "t2", "team_name": "NYCFC", "competition": "mls"},
            ]
        )

        with patch.object(self.client, "_get_entity", return_value=teams) as mock_get_entity:
            team_id = self.client._convert_name_to_id("team", "LAFC")

        assert team_id == "t1"
        assert self.client.teams is teams
        mock_get_entity.assert_called_once_with("team")

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

        with pytest.raises(InvalidLeagueError, match="is not valid"):
            self.client._check_leagues("invalid_league")

    def test_check_leagues_salaries_invalid(self, init_client):
        self.client = init_client

        with pytest.raises(SalaryDataError, match="Only MLS salary data is publicly available"):
            self.client._check_leagues_salaries("nwsl")

    def test_check_ids_names_both_values(self, init_client):
        self.client = init_client

        with pytest.raises(ConflictingParametersError, match="only IDs or names"):
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

    def test_convert_names_to_ids_with_none(self):
        self.client = AmericanSoccerAnalysis()
        result = self.client._convert_names_to_ids("player", None)
        assert result is None

    def test_convert_names_to_ids_with_list(self):
        self.client = AmericanSoccerAnalysis()
        self.client.players = DataFrame(
            [
                {"player_id": "p1", "player_name": "Alex Morgan", "competition": "mls"},
                {"player_id": "p2", "player_name": "Megan Rapinoe", "competition": "nwsl"},
            ]
        )

        player_ids = self.client._convert_names_to_ids("player", ["Alex Morgan", "Megan Rapinoe"])

        assert player_ids == ["p1", "p2"]

    def test_check_leagues_with_list(self):
        self.client = AmericanSoccerAnalysis()

        # Should not raise
        self.client._check_leagues(["mls", "nwsl"])

    def test_check_leagues_with_list_invalid(self, init_client):
        self.client = init_client

        with pytest.raises(InvalidLeagueError, match="is not a valid league"):
            self.client._check_leagues(["mls", "invalid_league"])

    def test_check_ids_names_with_invalid_ids_type(self, init_client):
        self.client = init_client

        with pytest.raises(InvalidParameterFormatError, match="IDs must be passed as a string or list of strings"):
            self.client._check_ids_names(123, None)

    def test_check_ids_names_with_invalid_names_type(self, init_client):
        self.client = init_client

        with pytest.raises(InvalidParameterFormatError, match="Names must be passed as a string or list of names"):
            self.client._check_ids_names(None, 123)

    def test_check_season_name_none(self, init_client):
        self.client = init_client
        
        # Should not raise
        self.client._check_season_name(None)

    def test_check_season_name_valid_single(self, init_client):
        self.client = init_client
        
        # Should not raise for valid years
        self.client._check_season_name("2023")
        self.client._check_season_name("2013")

    def test_check_season_name_valid_list(self, init_client):
        self.client = init_client
        
        # Should not raise for list of valid years
        self.client._check_season_name(["2020", "2021", "2022"])

    def test_check_season_name_before_2013_single(self, init_client):
        self.client = init_client

        with pytest.raises(InvalidSeasonError, match="Data is only available from 2013 onward"):
            self.client._check_season_name("2012")

    def test_check_season_name_before_2013_list(self, init_client):
        self.client = init_client

        with pytest.raises(InvalidSeasonError, match="Data is only available from 2013 onward"):
            self.client._check_season_name(["2020", "2012"])

    def test_check_season_name_invalid_format(self, init_client):
        self.client = init_client

        with pytest.raises(InvalidParameterFormatError, match="Season must be a valid year"):
            self.client._check_season_name("not_a_year")

    def test_check_season_name_invalid_format_list(self, init_client):
        self.client = init_client

        with pytest.raises(InvalidParameterFormatError, match="Season must be a valid year"):
            self.client._check_season_name(["2020", "invalid"])

    def test_filter_entity_by_ids_and_leagues(self, init_client):
        self.client = init_client
        self.client.teams = DataFrame(
            [
                {"team_id": "t1", "team_name": "LAFC", "competition": "mls"},
                {"team_id": "t2", "team_name": "Portland Timbers", "competition": "mls"},
                {"team_id": "t3", "team_name": "Angel City", "competition": "nwsl"},
            ]
        )

        filtered = self.client._filter_entity(
            self.client.teams, "team", ["mls"], ids="t1"
        )

        assert len(filtered) == 1
        assert filtered.iloc[0]["team_id"] == "t1"

    def test_filter_entity_with_list_ids(self, init_client):
        self.client = init_client
        self.client.teams = DataFrame(
            [
                {"team_id": "t1", "team_name": "LAFC", "competition": "mls"},
                {"team_id": "t2", "team_name": "Portland Timbers", "competition": "mls"},
                {"team_id": "t3", "team_name": "Angel City", "competition": "nwsl"},
            ]
        )

        filtered = self.client._filter_entity(
            self.client.teams, "team", ["mls"], ids=["t1", "t2"]
        )

        assert len(filtered) == 2
        assert list(filtered["team_id"]) == ["t1", "t2"]

    def test_filter_entity_no_filters(self, init_client):
        self.client = init_client
        self.client.teams = DataFrame(
            [
                {"team_id": "t1", "team_name": "LAFC", "competition": "mls"},
                {"team_id": "t2", "team_name": "Portland Timbers", "competition": "mls"},
                {"team_id": "t3", "team_name": "Angel City", "competition": "nwsl"},
            ]
        )

        filtered = self.client._filter_entity(
            self.client.teams, "team", None
        )

        assert len(filtered) == 3

    def test_execute_query_with_string_list_params(self):
        self.client = AmericanSoccerAnalysis()

        first = DataFrame([{"value": 1}, {"value": 2}])

        with patch.object(self.client, "_single_request", return_value=first) as mock_single:
            result = self.client._execute_query("http://example.com/api", {"ids": ["a", "b"]})

        assert mock_single.call_count == 1
        args, _ = mock_single.call_args
        assert args[1]["ids"] == "a,b"

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
