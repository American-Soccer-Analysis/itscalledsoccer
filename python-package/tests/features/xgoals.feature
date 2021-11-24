Feature: xG functions

	Tests that all xG function work correctly

	Scenario: Querying player-level xG values
		Given there is an ASA client
		When the get_player_xgoals function is called
		Then there is data
