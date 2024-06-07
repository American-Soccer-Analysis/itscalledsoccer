from behave import given, when, then
from pandas import DataFrame, read_json
from pathlib import Path
from itscalledsoccer.client import AmericanSoccerAnalysis
from unittest.mock import patch

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
    with patch('itscalledsoccer.client.AmericanSoccerAnalysis._get_entity'):
        context.soccer = AmericanSoccerAnalysis()

@then("there is data")
def step_impl(context):
    assert context.response is not None
    assert isinstance(context.response, DataFrame)
    assert len(context.response) >= 1

@then("there is multiple rows of data")
def step_impl(context):
    assert context.response is not None
    assert isinstance(context.response, DataFrame)
    assert len(context.response) >= 2

@when('the "{function}" function is called with arguments "{args}"')
def step_impl(context, function, args):
    kwargs = split_args(args)
    cwd = Path.cwd()
    print(kwargs)
    if "get_player_xgoals" == function:
        f = Path(cwd, "./mocks/players_xgoals_payload.json")
    elif "get_player_xpass" == function:
        f = Path(cwd, "./mocks/players_xpass_payload.json")
    elif "get_player_goals_added" == function:
        f = Path(cwd,"./mocks/players_goals_added_payload.json")
    elif "get_player_salaries" == function:
        f = Path(cwd,"./mocks/players_salaries_payload.json")
    elif "get_goalkeeper_xgoals" == function:
        f = Path("./mocks/goalkeepers_xgoals_payload.json")
    elif "get_goalkeeper_goals_added" == function:
        f = Path(cwd,"./mocks/goalkeepers_goals_added_payload.json")
    elif "get_team_xgoals" == function:
        f = Path(cwd,"./mocks/teams_xgoals_payload.json")
    elif "get_team_xpass" == function:
        f = Path("./mocks/teams_xpass_payload.json")
    elif "get_team_goals_added" == function:
        f = Path(cwd,"./mocks/teams_goals_added_payload.json")
    elif "get_team_salaries" == function:
        f = Path(cwd,"./mocks/teams_salaries_payload.json")
    elif "get_game_xgoals" == function:
        f = Path(cwd,"./mocks/games_xgoals_payload.json")
    elif "get_stadia" == function:
        f = Path(cwd,"./mocks/stadia_payload.json")
    elif "get_referees" == function:
        f = Path(cwd,"./mocks/referees_payload.json")
    elif "get_managers" == function:
        f = Path(cwd,"./mocks/managers_payload.json")
    elif "get_teams" == function:
        f = Path(cwd,"./mocks/teams_payload.json")
    elif "get_players" == function:
        f = Path(cwd,"./mocks/players_payload.json")
    elif "get_games" == function:
        f = Path(cwd,"./mocks/games_payload.json")
    else:
        print("Function not recognized")
        raise NameError
    context.response = read_json(f.open())