Feature: xPass functions

	Tests that all xPass function work correctly

	Scenario: Querying player-level xPass values
		Given there is an ASA client
		When the get_player_xpass function is called
		Then there is data