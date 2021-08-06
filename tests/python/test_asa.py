from unittest import TestCase
from unittest.mock import patch, Mock
from itscalledsoccer.client import AmericanSoccerAnalysis


class TestASA(TestCase):
    @patch.object(AmericanSoccerAnalysis, "_get_all_ids", return_value={})
    def setUp(self, mock_all_ids: Mock) -> None:
        self.soccer = AmericanSoccerAnalysis()

    def test_base_url(self):
        with patch.object(AmericanSoccerAnalysis, "_get_all_ids", return_value={}):
            self.assertIn(
                "https://app.americansocceranalysis.com/api", self.soccer.BASE_URL
            )

    def test_version(self):
        self.assertEqual("v1", self.soccer.API_VERSION)

    def test_leagues(self):
        self.assertEqual(len(self.soccer.LEAGUES), 5)
        self.assertEqual(["nwsl", "mls", "uslc", "usl1", "nasl"], self.soccer.LEAGUES)
