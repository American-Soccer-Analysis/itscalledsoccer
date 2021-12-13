from behave import *

def split_args(args: str) -> dict:
    kwargs = {}
    split = args.split(" ")
    if len(split) > 1:
        for s in split:
            captured_args = s.split('=')
            if "[" in captured_args[1]:
                kwargs[captured_args[0]] = captured_args[1].strip("][").split(",")
            else:
                kwargs[captured_args[0]] = captured_args[1]
    else:
        captured_args = split[0].split('=')
        if "[" in captured_args[1]:
            kwargs[captured_args[0]] = captured_args[1].strip("][").split(",")
        else:
            kwargs[captured_args[0]] = captured_args[1]
    return kwargs

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
    elif "get_game_xgoals" == function:
        context.response = context.soccer.get_game_xgoals(**kwargs)
    else:
        print("Function not recognized")
        raise KeyError
