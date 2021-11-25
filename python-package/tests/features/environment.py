from itscalledsoccer.client import AmericanSoccerAnalysis
from unittest.mock import patch, Mock


@patch.object(AmericanSoccerAnalysis, "_get_entity", return_value={})
def before_all(context, mock_all_ids: Mock):
    context.soccer = AmericanSoccerAnalysis()