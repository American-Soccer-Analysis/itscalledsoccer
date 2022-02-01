Feature: Stats functions

	Tests that all stats functions work correctly

	Scenario Outline: Querying <type>-level <stat> values
		Given there is an ASA client
		When the "get_<type>_<stat>" function is called with arguments "<args>"
		Then there is data

		@player_xgoals
		Examples:
			| type   | args                                                       | stat   |
			| player | leagues=mls                                                | xgoals |
			| player | leagues=[mls,uslc]  season_name=2020                       | xgoals |
			| player | leagues=mls  minimum_minutes=1000                          | xgoals |
			| player | leagues=mls  minimum_shots=200                             | xgoals |
			| player | leagues=mls  minimum_key_passes=20                         | xgoals |
			| player | player_ids=eV5DL18a5K                                      | xgoals |
			| player | player_ids=[vzqo8xZQap,9vQ22BR7QK]                         | xgoals |
			| player | player_names=Glesnes                                       | xgoals |
			| player | player_names=[Glesnes,Bedoya]                              | xgoals |
			| player | team_ids=NWMWlBK5lz                                        | xgoals |
			| player | team_ids=[NWMWlBK5lz,9Yqdwg85vJ]                           | xgoals |
			| player | team_names=Union                                           | xgoals |
			| player | team_names=[Philadelphia,Portland]                         | xgoals |
			| player | start_date=2021-07-01  end_date=2021-07-08                 | xgoals |
			| player | general_position=AM                                        | xgoals |
			| player | general_position=[AM,DM]                                   | xgoals |
			| player | season_name=[2019,2020]                                    | xgoals |
			| player | shot_pattern=Corner  season_name=2018                      | xgoals |
			| player | shot_pattern=[Corner,Penalty]  season_name=2018            | xgoals |
			| player | split_by_teams=true  season_name=2014                      | xgoals |
			| player | split_by_seasons=true  season_name=[2015,2016]             | xgoals |
			| player | split_by_games=true  season_name=2020  general_position=CB | xgoals |
			| player | stage_name=Playoffs  leagues=nwsl                          | xgoals |
			| player | stage_name=[Playoffs,Regular Season]  leagues=mls          | xgoals |


		@team_xgoals
		Examples:
			| type | args                                                   | stat   |
			| team | leagues=mls                                            | xgoals |
			| team | leagues=[mls,uslc]                                     | xgoals |
			| team | team_ids=NWMWlBK5lz                                    | xgoals |
			| team | team_ids=[NWMWlBK5lz,9Yqdwg85vJ]                       | xgoals |
			| team | team_names=Union                                       | xgoals |
			| team | team_names=[Philadelphia,Portland]                     | xgoals |
			| team | season_name=2018                                       | xgoals |
			| team | season_name=[2019,2020]                                | xgoals |
			| team | start_date=2021-07-01  end_date=2021-07-08             | xgoals |
			| team | shot_pattern=Corner                                    | xgoals |
			| team | shot_pattern=[Corner,Penalty]                          | xgoals |
			| team | split_by_seasons=true  season_name=[2015,2016]         | xgoals |
			# TODO: investigate failure here, API related
			# | team | split_by_games=true  season_name=2020                  | xgoals |
			| team | home_only=true  season_name=2013                       | xgoals |
			| team | away_only=true  season_name=2013                       | xgoals |
			| team | home_adjusted=true  season_name=2020                   | xgoals |
			| team | even_game_state=true  season_name=2020                 | xgoals |
			| team | stage_name=Playoffs  season_name=2021                  | xgoals |
			| team | stage_name=[Playoffs,Regular Season]  season_name=2021 | xgoals |


		@game_xgoals
		Examples:
			| type | args                                                               | stat   |
			| game | leagues=mls  season_name=2020                                      | xgoals |
			| game | leagues=[mls,uslc]  season_name=2020                               | xgoals |
			| game | start_date=2021-07-01  end_date=2021-07-08                         | xgoals |
			| game | stage_name=Playoffs  season_name=2021                              | xgoals |
			| game | stage_name=[Playoffs,MLS is Back Knockout Round]  season_name=2020 | xgoals |


		@gk_xgoals
		Examples:
			| type       | args                                           | stat   |
			| goalkeeper | leagues=mls                                    | xgoals |
			| goalkeeper | leagues=[mls,uslc]  season_name=2020           | xgoals |
			| goalkeeper | leagues=mls  minimum_minutes=1000              | xgoals |
			| goalkeeper | leagues=mls  minimum_shots_faced=200           | xgoals |
			| goalkeeper | player_ids=vzqoWbkqap                          | xgoals |
			| goalkeeper | player_ids=[vzqoWbkqap,gOMn6OlmMw]             | xgoals |
			| goalkeeper | player_names=Blake                             | xgoals |
			| goalkeeper | player_names=[Blake,Turner]                    | xgoals |
			| goalkeeper | team_ids=NWMWlBK5lz                            | xgoals |
			| goalkeeper | team_ids=[NWMWlBK5lz,9Yqdwg85vJ]               | xgoals |
			| goalkeeper | team_names=Union                               | xgoals |
			| goalkeeper | team_names=[Philadelphia,Portland]             | xgoals |
			| goalkeeper | start_date=2021-07-01  end_date=2021-07-08     | xgoals |
			| goalkeeper | season_name=[2019,2020]                        | xgoals |
			| goalkeeper | shot_pattern=Corner                            | xgoals |
			| goalkeeper | shot_pattern=[Corner,Penalty]                  | xgoals |
			| goalkeeper | split_by_teams=true  season_name=2014          | xgoals |
			| goalkeeper | split_by_seasons=true  season_name=[2015,2016] | xgoals |
			| goalkeeper | split_by_games=true  season_name=2020          | xgoals |
			| goalkeeper | stage_name=Playoffs                            | xgoals |
			| goalkeeper | stage_name=[Playoffs,Regular Season]           | xgoals |


		@player_goals_added
		Examples:
			| type   | args                                                       | stat        |
			| player | leagues=mls  season_name=2021                              | goals_added |
			| player | leagues=[mls,uslc]  season_name=2020                       | goals_added |
			| player | leagues=mls  minimum_minutes=1000                          | goals_added |
			| player | player_ids=eV5DL18a5K                                      | goals_added |
			| player | player_ids=[vzqo8xZQap,9vQ22BR7QK]                         | goals_added |
			| player | player_names=Glesnes                                       | goals_added |
			| player | player_names=[Glesnes,Bedoya]                              | goals_added |
			| player | team_ids=NWMWlBK5lz                                        | goals_added |
			| player | team_ids=[NWMWlBK5lz,9Yqdwg85vJ]                           | goals_added |
			| player | team_names=Union                                           | goals_added |
			| player | team_names=[Philadelphia,Portland]                         | goals_added |
			| player | start_date=2021-07-01  end_date=2021-07-08                 | goals_added |
			| player | general_position=AM                                        | goals_added |
			| player | general_position=[AM,DM]                                   | goals_added |
			| player | season_name=[2019,2020]                                    | goals_added |
			| player | split_by_teams=true  season_name=2014                      | goals_added |
			| player | split_by_seasons=true  season_name=[2015,2016]             | goals_added |
			| player | split_by_games=true  season_name=2020  general_position=CB | goals_added |
			| player | stage_name=Playoffs                                        | goals_added |
			| player | stage_name=[Playoffs,Regular Season]                       | goals_added |
			| player | action_type=Passing  leagues=mls                           | goals_added |
			| player | action_type=[Passing,Shooting]  leagues=mls                | goals_added |
			| player | above_replacement=true  leagues=mls                        | goals_added |


		@team_goals_added
		Examples:
			| type | args                                                   | stat        |
			| team | leagues=mls                                            | goals_added |
			| team | leagues=[mls,uslc]                                     | goals_added |
			| team | team_ids=NWMWlBK5lz                                    | goals_added |
			| team | team_ids=[NWMWlBK5lz,9Yqdwg85vJ]                       | goals_added |
			| team | team_names=Union                                       | goals_added |
			| team | team_names=[Philadelphia,Portland]                     | goals_added |
			| team | season_name=2018                                       | goals_added |
			| team | season_name=[2019,2020]                                | goals_added |
			| team | split_by_seasons=true  season_name=[2015,2016]         | goals_added |
			| team | stage_name=Playoffs  season_name=2021                  | goals_added |
			| team | stage_name=[Playoffs,Regular Season]  season_name=2021 | goals_added |
			| team | action_type=Passing                                    | goals_added |
			| team | action_type=[Shooting,Passing]                         | goals_added |
			| team | zone=24                                                | goals_added |
			| team | zone=[24,27]                                           | goals_added |
			| team | gamestate_trunc=2                                      | goals_added |
			| team | gamestate_trunc=[-2,2]                                 | goals_added |


		@gk_goals_added
		Examples:
			| type       | args                                           | stat        |
			| goalkeeper | leagues=mls                                    | goals_added |
			| goalkeeper | leagues=[mls,uslc]  season_name=2020           | goals_added |
			| goalkeeper | leagues=mls  minimum_minutes=1000              | goals_added |
			| goalkeeper | player_ids=vzqoWbkqap                          | goals_added |
			| goalkeeper | player_ids=[vzqoWbkqap,gOMn6OlmMw]             | goals_added |
			| goalkeeper | player_names=Blake                             | goals_added |
			| goalkeeper | player_names=[Blake,Turner]                    | goals_added |
			| goalkeeper | team_ids=NWMWlBK5lz                            | goals_added |
			| goalkeeper | team_ids=[NWMWlBK5lz,9Yqdwg85vJ]               | goals_added |
			| goalkeeper | team_names=Union                               | goals_added |
			| goalkeeper | team_names=[Philadelphia,Portland]             | goals_added |
			| goalkeeper | start_date=2021-07-01  end_date=2021-07-08     | goals_added |
			| goalkeeper | season_name=[2019,2020]                        | goals_added |
			| goalkeeper | split_by_teams=true  season_name=2014          | goals_added |
			| goalkeeper | split_by_seasons=true  season_name=[2015,2016] | goals_added |
			| goalkeeper | split_by_games=true  season_name=2020          | goals_added |
			| goalkeeper | stage_name=Playoffs                            | goals_added |
			| goalkeeper | stage_name=[Playoffs,Regular Season]           | goals_added |
			| goalkeeper | action_type=Shotstopping                       | goals_added |
			| goalkeeper | action_type=[Shotstopping,Sweeping]            | goals_added |
			| goalkeeper | above_replacement=true                         | goals_added |


		@player_xpass
		Examples:
			| type   | args                                                       | stat  |
			| player | leagues=mls  season_name=2021                              | xpass |
			| player | leagues=[mls,uslc]  season_name=2020                       | xpass |
			| player | leagues=mls  minimum_minutes=1000                          | xpass |
			| player | player_ids=eV5DL18a5K                                      | xpass |
			| player | player_ids=[vzqo8xZQap,9vQ22BR7QK]                         | xpass |
			| player | player_names=Glesnes                                       | xpass |
			| player | player_names=[Glesnes,Bedoya]                              | xpass |
			| player | team_ids=NWMWlBK5lz                                        | xpass |
			| player | team_ids=[NWMWlBK5lz,9Yqdwg85vJ]                           | xpass |
			| player | team_names=Union                                           | xpass |
			| player | team_names=[Philadelphia,Portland]                         | xpass |
			| player | start_date=2021-07-01  end_date=2021-07-08                 | xpass |
			| player | general_position=AM                                        | xpass |
			| player | general_position=[AM,DM]                                   | xpass |
			| player | season_name=[2019,2020]                                    | xpass |
			| player | split_by_teams=true  season_name=2014                      | xpass |
			| player | split_by_seasons=true  season_name=[2015,2016]             | xpass |
			| player | split_by_games=true  season_name=2020  general_position=CB | xpass |
			| player | stage_name=Playoffs                                        | xpass |
			| player | stage_name=[Playoffs,Regular Season]                       | xpass |
			| player | pass_origin_third=Defensive  leagues=mls                   | xpass |
			| player | pass_origin_third=[Defensive,Middle]  leagues=mls          | xpass |


		@team_xpass
		Examples:
			| type | args                                                   | stat  |
			| team | leagues=mls                                            | xpass |
			| team | leagues=[mls,uslc]                                     | xpass |
			| team | team_ids=NWMWlBK5lz                                    | xpass |
			| team | team_ids=[NWMWlBK5lz,9Yqdwg85vJ]                       | xpass |
			| team | team_names=Union                                       | xpass |
			| team | team_names=[Philadelphia,Portland]                     | xpass |
			| team | season_name=2018                                       | xpass |
			| team | season_name=[2019,2020]                                | xpass |
			| team | split_by_seasons=true  season_name=[2015,2016]         | xpass |
			| team | stage_name=Playoffs  season_name=2021                  | xpass |
			| team | stage_name=[Playoffs,Regular Season]  season_name=2021 | xpass |
			| team | home_only=true  season_name=2013                       | xpass |
			| team | away_only=true  season_name=2013                       | xpass |
			| team | pass_origin_third=Defensive                            | xpass |
			| team | pass_origin_third=[Defensive,Middle]                   | xpass |


		@player_salaries
		Examples:
			| type   | args                                       | stat     |
			# | player | leagues=mls                                                | salaries |
			| player | leagues=mls  season_name=2020              | salaries |
			| player | player_ids=eV5DL18a5K                      | salaries |
			| player | player_ids=[vzqo8xZQap,9vQ22BR7QK]         | salaries |
			| player | player_names=Glesnes                       | salaries |
			| player | player_names=[Glesnes,Bedoya]              | salaries |
			| player | team_ids=NWMWlBK5lz                        | salaries |
			| player | team_ids=[NWMWlBK5lz,9Yqdwg85vJ]           | salaries |
			| player | team_names=Union                           | salaries |
			| player | team_names=[Philadelphia,Portland]         | salaries |
			| player | start_date=2020-07-01  end_date=2021-07-08 | salaries |
			| player | position=M  season_name=2019               | salaries |
			| player | position=[D,M]  season_name=2018           | salaries |
			| player | season_name=[2019,2020]                    | salaries |


		@team_salaries
		Examples:
			| type | args                                                    | stat     |
			# | team | leagues=mls                                    | salaries |
			| team | leagues=mls  season_name=2020  split_by_seasons=true    | salaries |
			| team | team_ids=NWMWlBK5lz  split_by_teams=true                | salaries |
			| team | team_ids=[NWMWlBK5lz,9Yqdwg85vJ]  split_by_teams=true   | salaries |
			| team | team_names=Union  split_by_teams=true                   | salaries |
			| team | team_names=[Philadelphia,Portland]  split_by_teams=true | salaries |
			| team | season_name=[2019,2020]  split_by_seasons=true          | salaries |
			| team | split_by_teams=true  season_name=2014                   | salaries |
			| team | split_by_seasons=true  season_name=[2015,2016]          | salaries |
			| team | split_by_positions=true  season_name=2020               | salaries |


# TODO: Add expected failure scenarios
