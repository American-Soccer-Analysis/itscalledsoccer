from behave import *
from pandas import DataFrame

def split_args(args: str) -> dict:
    kwargs = {}
    split = args.split("  ")
    if len(split) > 1:
        for s in split:
            captured_args = s.split('=')
            if "[" in captured_args[1]:
                kwargs[captured_args[0]] = captured_args[1].strip("][").strip().split(",")
            else:
                kwargs[captured_args[0]] = captured_args[1]
    else:
        captured_args = split[0].split('=')
        if "[" in captured_args[1]:
            kwargs[captured_args[0]] = captured_args[1].strip("][").strip().split(",")
        else:
            kwargs[captured_args[0]] = captured_args[1]
    return kwargs

@given("there is an ASA client")
def step_impl(context):
    pass

@then("there is data")
def step_impl(context):
    assert context.response is not None
    assert isinstance(context.response, DataFrame)
    assert len(context.response) >= 1

@when('the "{function}" function is called with arguments "{args}"')
def step_impl(context, function, args):
    kwargs = split_args(args)
    print(kwargs)
    if "get_player_xgoals" == function:
        context.response = context.soccer.get_player_xgoals(**kwargs)
    elif "get_player_xpass" == function:
        context.response = context.soccer.get_player_xpass(**kwargs)
    elif "get_player_goals_added" == function:
        context.response = context.soccer.get_player_goals_added(**kwargs)
    elif "get_player_salaries" == function:
        context.response = context.soccer.get_player_salaries(**kwargs)
    elif "get_goalkeeper_xgoals" == function:
        context.response = context.soccer.get_goalkeeper_xgoals(**kwargs)
    elif "get_goalkeeper_goals_added" == function:
        context.response = context.soccer.get_goalkeeper_goals_added(**kwargs)
    elif "get_team_xgoals" == function:
        context.response = context.soccer.get_team_xgoals(**kwargs)
    elif "get_team_xpass" == function:
        context.response = context.soccer.get_team_xpass(**kwargs)
    elif "get_team_goals_added" == function:
        context.response = context.soccer.get_team_goals_added(**kwargs)
    elif "get_team_salaries" == function:
        context.response = context.soccer.get_team_salaries(**kwargs)
    elif "get_game_xgoals" == function:
        context.response = context.soccer.get_game_xgoals(**kwargs)
    elif "get_stadia" == function:
        context.response = context.soccer.get_stadia(**kwargs)
    elif "get_referees" == function:
        context.response = context.soccer.get_referees(**kwargs)
    elif "get_managers" == function:
        context.response = context.soccer.get_managers(**kwargs)
    elif "get_teams" == function:
        context.response = context.soccer.get_teams(**kwargs)
    elif "get_players" == function:
        context.response = context.soccer.get_players(**kwargs)
    elif "get_games" == function:
        context.response = context.soccer.get_games(**kwargs)
    else:
        print("Function not recognized")
        raise NameError