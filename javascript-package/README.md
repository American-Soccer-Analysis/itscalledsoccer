# itscalledsoccer

`itscalledsoccer` is a wrapper around the same API that powers the [American Soccer Analysis app](https://app.americansocceranalysis.com/). It enables Node users to programmatically retrieve advanced analytics for their favorite [MLS](https://en.wikipedia.org/wiki/Major_League_Soccer), [NWSL](https://en.wikipedia.org/wiki/National_Women%27s_Soccer_League), and [USL](https://en.wikipedia.org/wiki/United_Soccer_League) players and teams.

## Installation Getting Started

Install the library

```shell
$ npm i -S itscalledsoccer
```

## Getting Started

import the library

```javascript
import Client from "itscalledsoccer";
```

instantiate the client

```javascript
const client = new Client();
```

## Usage

Any of the `get*` methods can be used to retrieve the same data made available in the [American Soccer Analysis app](https://app.americansocceranalysis.com/). Partial matches or abbreviations are accepted for any player or team names. For most methods, arguments _must be named_. There is an example for each of the methods below, but not all options are shown. You can find the list of all of the parameters in [the Swagger docs](https://app.americansocceranalysis.com/api/v1/__docs__/), with the notable different that the parameters are `snake_case` for the url parameters, but `camelCase` for the client, so `split_by_games` becomes `splitByGames`.

To see a full example of using the library, see [here](https://github.com/doug-wade/itscalledsoccerclient).

### getPlayers

```javascript
const asaPlayers = await client.getPlayers({ names: "Roldan" });
```

### getManagers

```javascript
const asaManager = await client.getManagers({ ids: ["odMXxreMYL"] });
```

### getTeams

```javascript
const asaTeam = await client.getTeams({ leagues: ["mls"] });
```

### getReferees

```javascript
const asaReferees = await client.getReferees();
```

### getStadia

```javascript
const asaStadia = await client.getStadia();
```

### getPlayersXgoals

```javascript
const asaXgoals = await client.getPlayersXgoals({
  leagues: ["mls"],
  seasonName: "2021",
  generalPosition: "W",
});
```

### getPlayersXpass

```javascript
const asaXpass = await client.getPlayersXpass({
  playerId: ["aDQ0PKPRQE", "aDQ0PkRRQE"],
});
```

### getPlayersGoalsAdded

```javascript
const asaGoalsAdded = await client.getPlayersGoalsAdded({
  minimumMinutes: 1000,
  splitByTeams: true,
});
```

### getGoalkeepersXgoals

```javascript
const asaXgoals = await client.getGoalkeepersXgoals({ leagues: ["mls"] });
```

### getGoalkeepersXgoals

```javascript
const asaXgoals = await client.getGoalkeepersGoalsAdded({ leagues: ["mls"] });
```

### getGoalkeepersGoalsAdded

```javascript
const asaGoalsAdded = await client.getGoalkeepersGoalsAdded({
  actionType: "Sweeping",
  splitByTeams: true,
});
```

### getTeamsXgoals

```javascript
const asaGoalsAdded = await client.getTeamsXgoals({
  homeAdjusted: true,
  shotPattern: "Fastbreak",
});
```

### getTeamsXpass

```javascript
const asaXpass = await client.getTeamsXpass({
  stageName: "MLS is Back Group Stage",
  awayOnly: true,
});
```

### getTeamsGoalsAdded

```javascript
const asaGoalsAdded = await client.getTeamsGoalsAdded({
  zone: 27,
});
```

### getTeamsSalaries

```javascript
const asaSalaries = await client.getTeamsSalaries({
  seasonName: "2015",
});
```

### getGamesXgoals

```javascript
const asaXgoals = await client.getGamesXgoals({
  stageName: "Playoffs",
});
```
