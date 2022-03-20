import fetch from "isomorphic-fetch";
import "core-js/stable";
import "regenerator-runtime/runtime";
import Fuse from "fuse.js";
import { snakeCase } from "change-case";

import pluralize from "./pluralize";
import { BASE_URL, ENTITY_TYPES, LEAGUES, MIN_FUSE_SCORE } from "./constants";
import {
  validateLeagues,
  validateStringArray,
  validateUrlParameters,
} from "./validators";
import {
  playersXgoalsParameters,
  playersXpassParameters,
  playersGoalsAddedParameters,
  playersSalariesParameters,
  goalkeepersXgoalsParameters,
  goalkeepersGoalsAddedParameters,
  teamsXgoalsParameters,
  teamsXpassParameters,
  teamsGoalsAddedParameters,
  teamsSalariesParameters,
  gamesXgoalsParameters,
} from "./parameters.js";

export default class Client {
  #fuses = new Map();
  #minimumFuseScore;

  constructor({ minimumFuseScore } = {}) {
    this.#minimumFuseScore = minimumFuseScore || MIN_FUSE_SCORE;
  }

  /* utils */
  async #convertNameToId({ name, entityType, league }) {
    const fuseKey = `${league}|${entityType}`;

    let fuse;
    if (!this.#fuses.has(entityType)) {
      const pluralEntityType = pluralize(entityType);
      const url = `${BASE_URL}${league}/${pluralEntityType}`;
      const response = await fetch(url);

      if (response.status >= 400) {
        throw new Error(
          `Got a bad response from the server: ${response.status}`
        );
      }

      const entities = await response.json();
      fuse = new Fuse(entities, {
        includeScore: true,
        keys: [`${entityType}_name`],
      });
      this.#fuses.set(fuseKey, fuse);
    } else {
      fuse = this.#fuses.get(fuseKey);
    }

    const result = fuse.search(name);

    if (!result[0] || result[0].score > this.#minimumFuseScore) {
      throw new Error(`Name ${name} does not match any known name`);
    }

    return result[0].item;
  }

  async #getEntityIdsByName({ names = [], entityType, leagues }) {
    if (!names.length) {
      const entities = new Map();

      leagues.forEach((league) => {
        entities.set(league, []);
      });

      return entities;
    }

    return Promise.all(
      leagues.map(async (league) => {
        const entities = await Promise.all(
          names.map((name) =>
            this.#convertNameToId({ name, entityType, league })
          )
        );

        const entityIds = entities.map((entity) => entity[`${entityType}_id`]);

        return { league, [`${pluralize(entityType)}`]: entityIds };
      })
    );
  }

  async #fetchEntity({ leagues, entityType, ids }) {
    const results = await Promise.all(
      leagues.map(async (league) => {
        const url = `${BASE_URL}${league}/${pluralize(entityType)}${
          ids.length ? `?${entityType}_id=${ids.join(",")}` : ""
        }`;

        const response = await fetch(url);

        if (response.status >= 400) {
          throw new Error(
            `Got a bad response from the server: ${response.status}`
          );
        }

        return response.json();
      })
    );

    return results.reduce((acc, curr) => acc.concat(curr), []);
  }

  async #getStats({ leagues, urlFragment, urlParams }) {
    const urls = leagues.map((league) => {
      const url = new URL(`${BASE_URL}${league}${urlFragment}`);
      if (Object.keys(urlParams).length > 0) {
        Object.entries(urlParams).forEach(([key, val]) => {
          url.searchParams.set(snakeCase(key), val);
        });
      }
      return url;
    });
    const results = await Promise.all(
      urls.map(async (url) => {
        const response = await fetch(url.href);

        if (response.status >= 400) {
          throw new Error(
            `Got a bad response from the server: ${response.status}`
          );
        }

        return response.json();
      })
    );
    return results.reduce(
      (accumulator, result) => accumulator.concat(result),
      []
    );
  }

  /* public-facing api */
  async getPlayersByName({
    leagues = Object.values(LEAGUES),
    names = [],
  } = {}) {
    validateStringArray({
      strings: names,
      message: `names must be an array of strings, got ${names}`,
    });
    validateLeagues({ leagues });

    return this.#getEntityIdsByName({
      names,
      entityType: ENTITY_TYPES.PLAYER,
      leagues,
    });
  }

  async getPlayers({ leagues = Object.values(LEAGUES), ids = [] } = {}) {
    validateStringArray({
      strings: ids,
      message: `ids must be an array of strings, got ${ids}`,
    });
    validateLeagues({ leagues });

    return this.#fetchEntity({
      ids,
      entityType: ENTITY_TYPES.PLAYER,
      leagues,
    });
  }

  async getManagersByName({
    leagues = Object.values(LEAGUES),
    names = [],
  } = {}) {
    validateStringArray({
      strings: names,
      message: `names must be an array of strings, got ${names}`,
    });
    validateLeagues({ leagues });

    return this.#getEntityIdsByName({
      names,
      entityType: ENTITY_TYPES.MANAGER,
      leagues,
    });
  }

  async getManagers({ leagues = Object.values(LEAGUES), ids = [] } = {}) {
    validateStringArray({
      strings: ids,
      message: `ids must be an array of strings, got ${ids}`,
    });
    validateLeagues({ leagues });

    return this.#fetchEntity({
      ids,
      entityType: ENTITY_TYPES.MANAGER,
      leagues,
    });
  }

  async getStadiaByName({ leagues = Object.values(LEAGUES), names = [] } = {}) {
    validateStringArray({
      strings: names,
      message: `names must be an array of strings, got ${names}`,
    });
    validateLeagues({ leagues });

    return this.#getEntityIdsByName({
      names,
      entityType: ENTITY_TYPES.STADIUM,
      leagues,
    });
  }

  async getStadia({ leagues = Object.values(LEAGUES), ids = [] } = {}) {
    validateStringArray({
      strings: ids,
      message: `ids must be an array of strings, got ${ids}`,
    });
    validateLeagues({ leagues });

    return this.#fetchEntity({
      ids,
      entityType: ENTITY_TYPES.STADIUM,
      leagues,
    });
  }

  async getRefereesByName({
    leagues = Object.values(LEAGUES),
    names = [],
  } = {}) {
    validateStringArray({
      strings: names,
      message: `names must be an array of strings, got ${names}`,
    });
    validateLeagues({ leagues });

    return this.#getEntityIdsByName({
      names,
      entityType: ENTITY_TYPES.REFEREE,
      leagues,
    });
  }

  async getReferees({ leagues = Object.values(LEAGUES), ids = [] } = {}) {
    validateStringArray({
      strings: ids,
      message: `ids must be an array of strings, got ${ids}`,
    });
    validateLeagues({ leagues });

    return this.#fetchEntity({
      ids,
      entityType: ENTITY_TYPES.REFEREE,
      leagues,
    });
  }

  async getTeamsByName({ leagues = Object.values(LEAGUES), names = [] } = {}) {
    validateStringArray({
      strings: names,
      message: `names must be an array of strings, got ${names}`,
    });
    validateLeagues({ leagues });

    return this.#getEntityIdsByName({
      names,
      entityType: ENTITY_TYPES.TEAM,
      leagues,
    });
  }

  async getTeams({ leagues = Object.values(LEAGUES), ids = [] } = {}) {
    validateStringArray({
      strings: ids,
      message: `ids must be an array of strings, got ${ids}`,
    });
    validateLeagues({ leagues });

    return this.#fetchEntity({
      ids,
      entityType: ENTITY_TYPES.TEAM,
      leagues,
    });
  }

  async getPlayersXgoals({ leagues = Object.values(LEAGUES), ...args } = {}) {
    validateLeagues({ leagues });
    validateUrlParameters({
      validParameters: playersXgoalsParameters,
      providedArguments: args,
    });

    return this.#getStats({
      leagues,
      urlFragment: "/players/xgoals",
      urlParams: args,
    });
  }

  async getPlayersXpass({ leagues = Object.values(LEAGUES), ...args } = {}) {
    validateLeagues({ leagues });
    validateUrlParameters({
      validParameters: playersXpassParameters,
      providedArguments: args,
    });

    return this.#getStats({
      leagues,
      urlFragment: "/players/xpass",
      urlParams: args,
    });
  }

  async getPlayersGoalsAdded({
    leagues = Object.values(LEAGUES),
    ...args
  } = {}) {
    validateLeagues({ leagues });
    validateUrlParameters({
      validParameters: playersGoalsAddedParameters,
      providedArguments: args,
    });

    return this.#getStats({
      leagues,
      urlFragment: "/players/goals-added",
      urlParams: args,
    });
  }

  async getPlayersSalaries({ leagues = Object.values(LEAGUES), ...args } = {}) {
    validateLeagues({ leagues });
    validateUrlParameters({
      validParameters: playersSalariesParameters,
      providedArguments: args,
    });

    return this.#getStats({
      leagues,
      urlFragment: "/players/salaries",
      urlParams: args,
    });
  }

  async getGoalkeepersXgoals({
    leagues = Object.values(LEAGUES),
    ...args
  } = {}) {
    validateLeagues({ leagues });
    validateUrlParameters({
      validParameters: goalkeepersXgoalsParameters,
      providedArguments: args,
    });

    return this.#getStats({
      leagues,
      urlFragment: "/goalkeepers/xgoals",
      urlParams: args,
    });
  }

  async getGoalkeepersGoalsAdded({
    leagues = Object.values(LEAGUES),
    ...args
  } = {}) {
    validateLeagues({ leagues });
    validateUrlParameters({
      validParameters: goalkeepersGoalsAddedParameters,
      providedArguments: args,
    });

    return this.#getStats({
      leagues,
      urlFragment: "/goalkeepers/goals-added",
      urlParams: args,
    });
  }

  async getTeamsXgoals({ leagues = Object.values(LEAGUES), ...args } = {}) {
    validateLeagues({ leagues });
    validateUrlParameters({
      validParameters: teamsXgoalsParameters,
      providedArguments: args,
    });

    return this.#getStats({
      leagues,
      urlFragment: "/teams/xgoals",
      urlParams: args,
    });
  }

  async getTeamsXpass({ leagues = Object.values(LEAGUES), ...args } = {}) {
    validateLeagues({ leagues });
    validateUrlParameters({
      validParameters: teamsXpassParameters,
      providedArguments: args,
    });

    return this.#getStats({
      leagues,
      urlFragment: "/teams/xpass",
      urlParams: args,
    });
  }

  async getTeamsGoalsAdded({ leagues = Object.values(LEAGUES), ...args } = {}) {
    validateLeagues({ leagues });
    validateUrlParameters({
      validParameters: teamsGoalsAddedParameters,
      providedArguments: args,
    });

    return this.#getStats({
      leagues,
      urlFragment: "/teams/goals-added",
      urlParams: args,
    });
  }

  async getTeamsSalaries({ leagues = Object.values(LEAGUES), ...args } = {}) {
    validateLeagues({ leagues });
    validateUrlParameters({
      validParameters: teamsSalariesParameters,
      providedArguments: args,
    });

    return this.#getStats({
      leagues,
      urlFragment: "/teams/salaries",
      urlParams: args,
    });
  }

  async getGamesXgoals({ leagues = Object.values(LEAGUES), ...args } = {}) {
    validateLeagues({ leagues });
    validateUrlParameters({
      validParameters: gamesXgoalsParameters,
      providedArguments: args,
    });

    return this.#getStats({
      leagues,
      urlFragment: "/games/xgoals",
      urlParams: args,
    });
  }
}
