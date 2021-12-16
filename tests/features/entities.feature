Feature: Entities functions

	Tests that all entities functions work correctly

	Scenario Outline: Filtering <entity>-level
		Given there is an ASA client
		When the "get_<entity>" function is called with arguments "<args>"
		Then there is data

		@players
		Examples:
			| entity  | args                                     |
			| players | leagues=mls                              |
			| players | leagues=[mls,uslc]                       |
			| players | ids=eV5DL18a5K                           |
			| players | ids=[vzqo8xZQap,9vQ22BR7QK]              |
			| players | names=Jakob Glesnes                      |
			| players | names=[Jakob Glesnes,Alejandro Bedoya]   |
			| players | leagues=mls  ids=[p6qbedyp50,9z5kagOjQA] |
			| players | leagues=mls  names=Andre Blake           |

		@teams
		Examples:
			| entity | args                                        |
			| teams  | leagues=mls                                 |
			| teams  | leagues=[mls,uslc]                          |
			| teams  | ids=NWMWlBK5lz                              |
			| teams  | ids=[a2lqRX2Mr0,9Yqdwg85vJ]                 |
			| teams  | names=Philadelphia Union                    |
			| teams  | names=[Philadelphia Union,Portland Timbers] |
			| teams  | leagues=mls  ids=[a2lqRX2Mr0,9Yqdwg85vJ]    |
			| teams  | leagues=mls  names=Philadelphia Union       |

		@stadia
		Examples:
			| entity | args                                     |
			| stadia | leagues=mls                              |
			| stadia | leagues=[mls,uslc]                       |
			| stadia | ids=Vj58BPwQ8n                           |
			| stadia | ids=[Vj58BPwQ8n,4JMALEDQKg]              |
			| stadia | names=Subaru                             |
			| stadia | names=[Subaru,Providence]                |
			| stadia | leagues=mls  ids=[Vj58BPwQ8n,4JMALEDQKg] |
			| stadia | leagues=mls  names=Subaru                |

		@managers
		Examples:
			| entity   | args                                     |
			| managers | leagues=mls                              |
			| managers | leagues=[mls,uslc]                       |
			| managers | ids=LeVq3j5WOJ                           |
			| managers | ids=[LeVq3j5WOJ,0Oq6zkzq6D]              |
			| managers | names=Curtin                             |
			# Something going on with fuzzing library
			# | managers | names=[Curtin,Arena]                    |
			| managers | leagues=mls  ids=[LeVq3j5WOJ,0Oq6zkzq6D] |
			| managers | leagues=mls  names=Jim Curtin            |

		@referees
		Examples:
			| entity   | args                                     |
			| referees | leagues=mls                              |
			| referees | leagues=[mls,uslc]                       |
			| referees | ids=a35r6KG5L6                           |
			| referees | ids=[a35r6KG5L6,0Oq6037M6D]              |
			| referees | names=Geiger                             |
			| referees | names=[Geiger,Kelly]                     |
			| referees | leagues=mls  ids=[a35r6KG5L6,0Oq6037M6D] |
			| referees | leagues=mls  names=Geiger                |

		@games
		Examples:
			| entity | args                                          |
			| games  | leagues=mls  seasons=2020                     |
			| games  | leagues=[mls,uslc]  seasons=2020              |
			| games  | game_ids=9z5kdxgKqA                           |
			| games  | game_ids=[9z5kdxgKqA,9z5kAnbPQA]              |
			| games  | team_ids=Vj58weDM8n                           |
			| games  | team_ids=[Vj58weDM8n,9Yqdwg85vJ]              |
			| games  | team_names=Union                              |
			| games  | team_names=[Philadelphia,Portland]            |
			| games  | leagues=mls  game_ids=[9z5kdxgKqA,9z5kAnbPQA] |
			| games  | leagues=mls  team_names=Philadelphia Union    |
			| games  | seasons=2020                                  |
			| games  | seasons=[2020,2021]                           |
			| games  | stages=Playoffs                               |
			| games  | stages=[Playoffs,Regular Season]              |

# TODO: Add expected failure scenarios
