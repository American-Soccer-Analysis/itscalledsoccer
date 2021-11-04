Feature: Client

	Scenario Outline: When I create a client, it has metadata
		Given I have an ASA client
		Then the API_VERSION should be "v1"
		And the BASE_URL should be "https://app.americansocceranalysis.com/api/v1/"
		And "<league>" should be in LEAGUES

		Examples: Leagues
			| league |
			| nwsl   |
			| mls    |
			| uslc   |
			| usl1   |
			| nasl   |
