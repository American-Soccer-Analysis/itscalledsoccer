from behave import *
from pandas import DataFrame

@when("the get_player_xgoals function is called")
def step_impl(context):
    context.player_xgoals = context.soccer.get_player_xgoals(leagues="mls")

@then("there is data")
def step_impl(context):
    assert context.player_xgoals is not None
    assert isinstance(context.player_xgoals, DataFrame)