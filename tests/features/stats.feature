Feature: Stats functions

	Tests that all stats functions work correctly

	Scenario Outline: Querying <type>-level xG values
		Given there is an ASA client
		When the "get_<type>_<stat>" function is called with arguments "<args>"
		Then there is data

		@player_xgoals
		Examples:
			| type   | args                                      | stat   |
			| player | leagues=mls                               | xgoals |
			| player | leagues=[mls,uslc] season_name=2020       | xgoals |
			| player | leagues=mls minimum_minutes=1000          | xgoals |
			| player | leagues=mls minimum_shots=200             | xgoals |
			| player | leagues=mls minimum_key_passes=1000       | xgoals |
			| player | player_ids=eV5DL18a5K                     | xgoals |
			| player | player_ids=[vzqo8xZQap,9vQ22BR7QK]        | xgoals |
			| player | player_names=Glesnes                      | xgoals |
			| player | player_names=[Glesnes,Bedoya]             | xgoals |
			| player | team_ids=NWMWlBK5lz                       | xgoals |
			| player | team_ids=[NWMWlBK5lz,9Yqdwg85vJ]          | xgoals |
			| player | team_names=Union                          | xgoals |
			| player | team_names=[Philadelphia,Portland]        | xgoals |
			| player | start_date=2021-01-01 end_date=2021-01-02 | xgoals |
			| player | general_position=AM                       | xgoals |
			| player | general_position=[AM,DM]                  | xgoals |

		@team_xgoals
		Examples:
			| type | args               | stat   |
			| team | leagues=mls        | xgoals |
			| team | leagues=[mls,uslc] | xgoals |

		@game_xgoals
		Examples:
			| type | args                                | stat   |
			| game | leagues=mls season_name=2020        | xgoals |
			| game | leagues=[mls,uslc] season_name=2020 | xgoals |

		@gk_xgoals:
		Examples:
			| type       | args               | stat   |
			| goalkeeper | leagues=mls        | xgoals |
			| goalkeeper | leagues=[mls,uslc] | xgoals |
