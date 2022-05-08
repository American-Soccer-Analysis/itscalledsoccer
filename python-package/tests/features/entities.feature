Feature: Entities functions

	Tests that all entities functions work correctly

	Scenario Outline: Filtering <entity>-level
		Given there is an ASA client
		When the "get_<entity>" function is called with arguments "<args>"
		Then there is data

		Examples:
			| entity   | args                      |
			| players  | leagues=mls               |
			| teams    | leagues=mls               |
			| stadia   | leagues=mls               |
			| managers | leagues=mls               |
			| referees | leagues=mls               |
			| games    | leagues=mls  seasons=2020 |

# TODO: Add expected failure scenarios
