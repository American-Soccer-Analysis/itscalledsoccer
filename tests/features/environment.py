from itscalledsoccer.client import AmericanSoccerAnalysis
from unittest.mock import patch


@patch("itscalledsoccer.client.AmericanSoccerAnalysis._get_entity")
def before_all(context, mock_entity):
    context.soccer = AmericanSoccerAnalysis()
