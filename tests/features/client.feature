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

	Scenario: An ASA client has a default logger
		Given there is an ASA client
		Then there is a logger
		And the logging level is WARNING

	Scenario: An ASA client's logging level is configurable
		Given there is an ASA client
		When the logging level is set to "DEBUG"
		Then there is a logger
		And the logging level is DEBUG

# TODO: this scenario stalls
# Scenario: An ASA client's proxy settings are configurable
# 	Given there is an ASA client
# 	When the proxy is set to "10.10.1.10"
# 	Then the session is using a proxy
