Feature: Stats functions

	Tests that all stats functions work correctly

	Scenario Outline: Querying <type>-level <stat> values
		Given there is an ASA client
		When the "get_<type>_<stat>" function is called with arguments "<args>"
		Then there is data

		Examples:
			| type       | args                                                 | stat        |
			| player     | leagues=mls                                          | xgoals      |
			| team       | leagues=mls                                          | xgoals      |
			| game       | leagues=mls  season_name=2020                        | xgoals      |
			| goalkeeper | leagues=mls                                          | xgoals      |
			| player     | leagues=mls  season_name=2021                        | goals_added |
			| team       | leagues=mls                                          | goals_added |
			| goalkeeper | leagues=mls                                          | goals_added |
			| player     | leagues=mls  season_name=2021                        | xpass       |
			| team       | leagues=mls                                          | xpass       |
			| player     | leagues=mls  season_name=2020                        | salaries    |
			| team       | leagues=mls  season_name=2020  split_by_seasons=true | salaries    |



	Scenario Outline: Expecting multiple rows of data
		Given there is an ASA client
		When the "get_<type>_<stat>" function is called with arguments "<args>"
		Then there is multiple rows of data

		Examples:
			| type | args                                         | stat   |
			| game | leagues=mls  game_id=[aDQ037dpqE,NPqxr10gM9] | xgoals |
