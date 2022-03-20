import fetch from "isomorphic-fetch";
import pluralize from "../src/pluralize";

import Client from "../src";
import { BASE_URL, ENTITY_TYPES, LEAGUES } from "../src/constants";

import { playersXgoalsParameters } from "../src/parameters.js";

// fetch payload mocks
import mockPlayersPayload from "./mocks/players-payload";
import mockManagersPayload from "./mocks/managers-payload";
import mockRefereesPayload from "./mocks/referees-payload";
import mockStadiaPayload from "./mocks/stadia-payload";
import mockTeamsPayload from "./mocks/teams-payload";

import mockPlayersXgoalsPayload from "./mocks/players-xgoals-payload";
import mockPlayersXpassPayload from "./mocks/players-xpass-payload";
import mockPlayersGoalsAddedPayload from "./mocks/players-goals-added-payload";
import mockPlayersSalariesPayload from "./mocks/players-salaries-payload";
import mockGoalkeepersXgoalsPayload from "./mocks/goalkeepers-xgoals-payload";
import mockGoalkeepersGoalsAddedPayload from "./mocks/goalkeepers-goals-added-payload";
import mockTeamsXgoalsPayload from "./mocks/teams-xgoals-payload";
import mockTeamsXpassPayload from "./mocks/teams-xpass-payload";
import mockTeamsGoalsAddedPayload from "./mocks/teams-goals-added-payload";
import mockTeamsSalariesPayload from "./mocks/teams-salaries-payload";
import mockGamesXgoalsPayload from "./mocks/games-xgoals-payload";

jest.mock("isomorphic-fetch");

describe("client", () => {
  describe("constructor", () => {
    it("instantiates with no arguments", () => {
      expect(() => {
        new Client();
      }).not.toThrow();
    });

    it("instantiates with the minimumFuseScore argument", () => {
      expect(() => {
        new Client({ minimumFuseScore: 0.75 });
      }).not.toThrow();
    });
  });

  describe("parameter validation", () => {
    it("logs to the console when an invalid league is provided", async () => {
      const mockLeague = "la liga";
      jest.spyOn(console, "assert").mockImplementation();
      fetch.mockImplementation(() =>
        Promise.resolve({
          async json() {
            return [];
          },
        })
      );

      const client = new Client();
      await client.getPlayersXgoals({
        leagues: [mockLeague],
      });

      expect(console.assert).toHaveBeenCalledWith(
        false,
        `leagues must be an array of nwsl, mls, uslc, usl1, nasl, fetchEntity got ${mockLeague}`
      );
    });

    it("logs to the console when an invalid url parameter is provided", async () => {
      const mockKey = "cristianRoldan";
      jest.spyOn(console, "assert").mockImplementation();
      fetch.mockImplementation(() =>
        Promise.resolve({
          async json() {
            return [];
          },
        })
      );

      const client = new Client();
      await client.getPlayersXgoals({
        [mockKey]: "mock value",
      });

      expect(console.assert).toHaveBeenCalledWith(
        false,
        `Url parameters must be one of ${Array.from(
          playersXgoalsParameters.values()
        ).join(", ")}, got ${mockKey}`
      );
    });
  });

  describe("getStats methods", () => {
    const testParameters = [
      {
        method: "getPlayersXpass",
        payload: mockPlayersXpassPayload,
        urlFragment: "/players/xpass",
      },
      {
        method: "getPlayersXgoals",
        payload: mockPlayersXgoalsPayload,
        urlFragment: "/players/xgoals",
      },
      {
        method: "getPlayersGoalsAdded",
        payload: mockPlayersGoalsAddedPayload,
        urlFragment: "/players/goals-added",
      },
      {
        method: "getPlayersSalaries",
        payload: mockPlayersSalariesPayload,
        urlFragment: "/players/salaries",
      },
      {
        method: "getGoalkeepersXgoals",
        payload: mockGoalkeepersXgoalsPayload,
        urlFragment: "/goalkeepers/xgoals",
      },
      {
        method: "getGoalkeepersGoalsAdded",
        payload: mockGoalkeepersGoalsAddedPayload,
        urlFragment: "/goalkeepers/goals-added",
      },
      {
        method: "getTeamsXgoals",
        payload: mockTeamsXgoalsPayload,
        urlFragment: "/teams/xgoals",
      },
      {
        method: "getTeamsXpass",
        payload: mockTeamsXpassPayload,
        urlFragment: "/teams/xpass",
      },
      {
        method: "getTeamsGoalsAdded",
        payload: mockTeamsGoalsAddedPayload,
        urlFragment: "/teams/goals-added",
      },
      {
        method: "getTeamsSalaries",
        payload: mockTeamsSalariesPayload,
        urlFragment: "/teams/salaries",
      },
      {
        method: "getGamesXgoals",
        payload: mockGamesXgoalsPayload,
        urlFragment: "/games/xgoals",
      },
    ];

    beforeEach(() => {
      jest.resetAllMocks();
    });

    it.each(testParameters)(
      "gets with no arguments",
      async ({ method, payload, urlFragment }) => {
        fetch.mockImplementation(() =>
          Promise.resolve({
            async json() {
              return payload;
            },
          })
        );
        const client = new Client();
        const results = await client[method]();

        expect(fetch).toHaveBeenCalledTimes(Object.keys(LEAGUES).length);
        Object.values(LEAGUES).forEach((league) => {
          expect(fetch).toHaveBeenCalledWith(
            `${BASE_URL}${league}${urlFragment}`
          );
        });
        expect(results.length).toBe(
          payload.length * Object.keys(LEAGUES).length
        );
      }
    );

    it.each(testParameters)(
      "gets with leagues argument",
      async ({ method, payload, urlFragment }) => {
        fetch.mockImplementation(() =>
          Promise.resolve({
            async json() {
              return payload;
            },
          })
        );
        const leaguesArgument = [LEAGUES.MLS, LEAGUES.NWSL];

        const client = new Client();
        const results = await client[method]({
          leagues: leaguesArgument,
        });

        expect(fetch).toHaveBeenCalledTimes(leaguesArgument.length);
        leaguesArgument.forEach((leagueArgument) => {
          expect(fetch).toHaveBeenCalledWith(
            `${BASE_URL}${leagueArgument}${urlFragment}`
          );
        });
        expect(results.length).toBe(payload.length * leaguesArgument.length);
      }
    );

    it.each(testParameters)(
      "gets with other arguments",
      async ({ method, payload, urlFragment }) => {
        fetch.mockImplementation(() =>
          Promise.resolve({
            async json() {
              return payload;
            },
          })
        );
        const mockLeague = LEAGUES.USLC;
        const mockMinimumPasses = 42;
        const mockMinimumMinutes = 1000;
        const mockSeasonName = "2021";
        const mockGeneralPosition = "W";

        const client = new Client();
        await client[method]({
          leagues: [mockLeague],
          minimumPasses: mockMinimumPasses,
          minimumMinutes: mockMinimumMinutes,
          seasonName: mockSeasonName,
          generalPosition: mockGeneralPosition,
        });

        expect(fetch).toHaveBeenCalledWith(
          `${BASE_URL}${mockLeague}${urlFragment}?minimum_passes=${mockMinimumPasses}&minimum_minutes=${mockMinimumMinutes}&season_name=${mockSeasonName}&general_position=${mockGeneralPosition}`
        );
      }
    );
  });

  describe("getEntity methods", () => {
    const testParameters = [
      {
        method: "getPlayers",
        entityType: ENTITY_TYPES.PLAYER,
        payload: mockPlayersPayload,
      },
      {
        method: "getManagers",
        entityType: ENTITY_TYPES.MANAGER,
        payload: mockManagersPayload,
      },
      {
        method: "getStadia",
        entityType: ENTITY_TYPES.STADIUM,
        payload: mockStadiaPayload,
      },
      {
        method: "getReferees",
        entityType: ENTITY_TYPES.REFEREE,
        payload: mockRefereesPayload,
      },
      {
        method: "getTeams",
        entityType: ENTITY_TYPES.TEAM,
        payload: mockTeamsPayload,
      },
    ];

    beforeEach(() => {
      jest.resetAllMocks();
    });

    it.each(testParameters)(
      "gets with no arguments",
      async ({ method, entityType, payload }) => {
        fetch.mockImplementation(() =>
          Promise.resolve({
            async json() {
              return payload;
            },
          })
        );
        const client = new Client();
        const results = await client[method]();

        expect(fetch).toHaveBeenCalledTimes(Object.keys(LEAGUES).length);
        Object.values(LEAGUES).forEach((league) => {
          expect(fetch).toHaveBeenCalledWith(
            `${BASE_URL}${league}/${pluralize(entityType)}`
          );
        });
        expect(results.length).toBe(
          payload.length * Object.values(LEAGUES).length
        );
      }
    );

    it.each(testParameters)(
      "gets with ids",
      async ({ method, entityType, payload }) => {
        const mockIds = ["abc", "123"];
        fetch.mockImplementation(() =>
          Promise.resolve({
            async json() {
              return payload;
            },
          })
        );

        const client = new Client();
        await client[method]({ ids: mockIds });

        Object.values(LEAGUES).forEach((league) => {
          expect(fetch).toHaveBeenCalledWith(
            `${BASE_URL}${league}/${pluralize(
              entityType
            )}?${entityType}_id=${mockIds.join(",")}`
          );
        });
      }
    );
  });

  describe("getEntityByName methods", () => {
    const testParameters = [
      {
        method: "getPlayersByName",
        entityType: ENTITY_TYPES.PLAYER,
        payload: mockPlayersPayload,
        mockName: "Ugo Ihemelu",
      },
      {
        method: "getManagersByName",
        entityType: ENTITY_TYPES.MANAGER,
        payload: mockManagersPayload,
        mockName: "Josh Wolff",
      },
      {
        method: "getStadiaByName",
        entityType: ENTITY_TYPES.STADIUM,
        payload: mockStadiaPayload,
        mockName: "PNC Stadium",
      },
      {
        method: "getRefereesByName",
        entityType: ENTITY_TYPES.REFEREE,
        payload: mockRefereesPayload,
        mockName: "Alan Kelly",
      },
      {
        method: "getTeamsByName",
        entityType: ENTITY_TYPES.TEAM,
        payload: mockTeamsPayload,
        mockName: "New England Revolution",
      },
    ];

    beforeEach(() => {
      jest.resetAllMocks();
    });

    it.each(testParameters)(
      "gets names",
      async ({ method, entityType, payload, mockName }) => {
        fetch.mockImplementation(() =>
          Promise.resolve({
            async json() {
              return payload;
            },
          })
        );

        const client = new Client({ minimumFuseScore: 0.1 });
        const result = await client[method]({
          names: [mockName],
          leagues: ["mls"],
        });

        expect(fetch).toHaveBeenCalledWith(
          `${BASE_URL}mls/${pluralize(entityType)}`
        );
        expect(result[0][`${pluralize(entityType)}`]).toHaveLength(1);
      }
    );

    it.each(testParameters)(
      "gets no results with no names",
      async ({ method }) => {
        const client = new Client();
        const result = await client[method]();

        expect(fetch).not.toHaveBeenCalled();
        result.forEach((entry) => {
          expect(entry).toHaveLength(0);
        });
      }
    );
  });
});
