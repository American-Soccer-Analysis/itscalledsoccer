Feature: g+ functions

	Tests that all g+ functions work correctly

	Scenario: Querying player-level g+ values
		Given there is an ASA client
		When the get_player_goals_added function is called
		Then there is data
