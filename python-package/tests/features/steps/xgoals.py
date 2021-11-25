from behave import *

@when("the get_player_xgoals function is called")
def step_impl(context):
    context.response = context.soccer.get_player_xgoals(leagues="mls")