Feature: Client initialization

	Scenario: An ASA client has metadata
		Given there is an ASA client
		Then the API_VERSION should be "v1"
		And the BASE_URL should be "https://app.americansocceranalysis.com/api/v1/"
		And the MAX_API_LIMIT should be "1000"

	Scenario Outline: An ASA client has the correct leagues
		Given there is an ASA client
		Then "<league>" should be in LEAGUES

		Examples: Leagues
			| league |
			| nwsl   |
			| mls    |
			| uslc   |
			| usl1   |
			| nasl   |
