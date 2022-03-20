# itscalledsoccer

American Soccer Analysis [released a library](https://www.americansocceranalysis.com/home/2022/2/9/introducing-itscalledsoccer) for interacting with their API for R and Python. This is a Javascript implementation of the same library.

## Getting Started

Install the library

```shell
$ npm i -S itscalledsoccer
```

import the library

```javascript
import Client from "itscalledsoccer";
```

instantiate the client

```javascript
const client = new Client();
```

## Usage

Any of the `get*` methods can be used to retrieve the same data made available in the [American Soccer Analysis app](https://app.americansocceranalysis.com/). Partial matches or abbreviations are accepted for any player or team names. For most methods, arguments _must be named_. A few examples are below.

### getPlayers

```javascript
// Get all players named "Roldan"
const asaPlayers = await client.getPlayers({ names: "Roldan" });
```

### getManagers

```javascript
// Get manager Brian Schmetzer
const asaManager = await client.getManagers({ ids: ["odMXxreMYL"] });
```

### getTeams

```javascript
// Get all MLS stadia
const asaTeam = await client.getTeams({ leagues: ["mls"] });
```

### getReferees

```javascript
// Get all referees
const asaReferees = await client.getReferees();
```

### getStadia

```javascript
// Get all stadia
const asaStadia = await client.getStadia();
```

### getPlayersXgoals

```javascript
// Get Xgoals for all MLS wingers in 2021
const asaXgoals = await client.getPlayersXgoals({
  leagues: ["mls"],
  seasonName: "2021",
  generalPosition: "W",
});
```

### getPlayersXpass

```javascript
// Get Xpass for players aDQ0PKPRQE and aDQ0PkRRQE
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
