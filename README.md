# itscalledsoccer

<div align="center">
    <img src="https://raw.githubusercontent.com/American-Soccer-Analysis/itscalledsoccer-r/main/man/figures/logo.png" align="center" height="175"/>
</div>

<br>

<!-- badges: start -->
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)
![PyPI Version](https://img.shields.io/pypi/v/itscalledsoccer.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/itscalledsoccer)
![Python tests](https://github.com/American-Soccer-Analysis/itscalledsoccer/actions/workflows/python-tests.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI download month](https://img.shields.io/pypi/dm/itscalledsoccer.svg)](https://pypi.python.org/pypi/itscalledsoccer/)
[![OpenSSF Baseline](https://www.bestpractices.dev/projects/9759/baseline)](https://www.bestpractices.dev/projects/9759)
[![codecov](https://codecov.io/gh/American-Soccer-Analysis/itscalledsoccer/graph/badge.svg?token=RUWMM7ZLQ2)](https://codecov.io/gh/American-Soccer-Analysis/itscalledsoccer)
<!-- badges: end -->

## Table of Contents

- [Background](#background)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
  - [Entities](#entities)
  - [Games](#games)
  - [Player Statistics](#player-statistics)
  - [Team Statistics](#team-statistics)
- [Advanced Usage](#advanced-usage)
- [API Reference](#api-reference)
- [Other Versions](#other-versions)
- [Contributing](#contributing)
- [License](#license)

---

## Background

`itscalledsoccer` is a Python wrapper around the [American Soccer Analysis API](https://app.americansocceranalysis.com/api/v1/), providing programmatic access to advanced soccer analytics across North American leagues.

**What you can measure:**
- **Expected Goals (xG)** — Shot quality and finishing efficiency
- **Expected Passes (xPass)** — Pass difficulty and creative play
- **Goals Added (g+)** — Total value contribution of players
- **Salaries** — MLS salary and spend data

The API is **free and public** — no authentication required.

**Supported leagues:**

| Code | League |
|------|--------|
| `mls` | Major League Soccer |
| `nwsl` | National Women's Soccer League |
| `uslc` | USL Championship |
| `usl1` | USL League One |
| `usls` | USL Super League |
| `nasl` | North American Soccer League (historical) |
| `mlsnp` | MLS Next Pro |

**Useful links:**
- Full API documentation: [american-soccer-analysis.github.io/itscalledsoccer/reference](https://american-soccer-analysis.github.io/itscalledsoccer/reference)
- Web app: [app.americansocceranalysis.com](https://app.americansocceranalysis.com/)

---

## Features

- **15 API methods** covering players, teams, games, and advanced statistics
- **Fuzzy name matching** — search by partial names or abbreviations ("LA", "Vela")
- **Type hints** — full type annotations on all public methods
- **Consistent interface** — same patterns across all 7 leagues

---

## Installation

### Stable Release

```bash
pip install itscalledsoccer
```

### Development Version

```bash
git clone https://github.com/American-Soccer-Analysis/itscalledsoccer.git
cd itscalledsoccer
pip install -e ".[dev]"
```

**Requirements:** Python 3.10+, `requests`, `pandas`, `cachecontrol`, `rapidfuzz`

---

## Quick Start

```python
from itscalledsoccer.client import AmericanSoccerAnalysis

# Initialize client (no authentication required)
asa = AmericanSoccerAnalysis()

# Get all USLC players
uslc_players = asa.get_players(leagues="uslc")

# Get Expected Goals (xG) data for 2023
xg_data = asa.get_player_xgoals(
    leagues="uslc",
    season_name="2023"
)
```

For the complete method reference, see **[Usage Examples](#usage-examples)** below.

---

## Usage Examples

### Entities

Retrieve core soccer entities with optional filtering:

```python
# Same interface for all entity types
uslc_players = asa.get_players(leagues="uslc")
teams = asa.get_teams(leagues=["uslc", "nwsl"])
stadia = asa.get_stadia()
managers = asa.get_managers(leagues="uslc")
referees = asa.get_referees(leagues=["uslc", "mls"])

# Filter games by team
usl_2024_games = asa.get_games(leagues="uslc", team_names="Louisville City", seasons="2024")
```

**Available entities:** players, teams, stadia, managers, referees

---

### Games

```python
# Get games for a specific league and season
uslc_2024_games = asa.get_games(leagues="uslc", seasons="2024")
```

---

### Player Statistics

#### Expected Goals (xG)

Expected Goals measures the quality of shot chances a player creates or faces.

```python
xg = asa.get_player_xgoals(
    leagues="uslc",
    season_name="2025",
    minimum_minutes=900
)
```

**Available filters:** `minimum_minutes`, `minimum_shots`, `minimum_key_passes`, `shot_pattern`, `split_by_teams`, `split_by_seasons`, `split_by_games`, `general_position`

#### Expected Pass (xPass)

Expected Pass measures pass difficulty and creative play value.

```python
xpass = asa.get_player_xpass(
    leagues="uslc",
    minimum_minutes=900
)
```

#### Goals Added (g+)

Goals Added measures total value contribution across all actions.

```python
gplus = asa.get_player_goals_added(
    leagues="uslc",
    above_replacement=True
)
```

**Note:** Goalkeeper statistics use the same interface — `get_goalkeeper_xgoals()` and `get_goalkeeper_goals_added()`.

---

### Team Statistics

```python
# Team Expected Goals
team_xg = asa.get_team_xgoals(
    leagues="uslc",
    split_by_seasons=True
)

# Team Expected Pass
team_xpass = asa.get_team_xpass(
    leagues=["uslc", "nwsl"],
    split_by_seasons=True
)

# Team Salaries (MLS only)
team_salaries = asa.get_team_salaries(
    leagues="mls",
    split_by_teams=True
)
```

**Team-specific filters:** `home_only`, `away_only`, `home_adjusted`, `even_game_state`, `zone` (1-30), `gamestate_trunc` (-2 to 2)

---

## Advanced Usage

### Fuzzy Name Matching

Search by partial names, initials, or abbreviations. Returns only the best match:

```python
# All of these match "Carlos Vela"
asa.get_players(names="Carlos Vela")

# Team names
asa.get_teams(names="LA")
```

---

## API Reference

**Complete documentation:** [american-soccer-analysis.github.io/itscalledsoccer/reference](https://american-soccer-analysis.github.io/itscalledsoccer/reference)

The reference includes:
- All 15 methods and their parameters
- Complete field descriptions for each endpoint
- Type signatures and defaults

**Common questions:**

- **No API key needed?** Correct — the API is public and free.
- **Why is my query slow?** Large queries may take a moment. Subsequent identical queries are cached.
- **What do the metrics mean?** 
  - **xG:** Shot quality (0-1 per shot)
  - **xPass:** Pass completion probability (0-1)
  - **g+:** Measures a player's total on-ball contribution in attack and defense

For detailed methodology, see [American Soccer Analysis](https://app.americansocceranalysis.com/).

---

## Other Versions

- **R:** [itscalledsoccer-r](https://github.com/American-Soccer-Analysis/itscalledsoccer-r)
- **JavaScript:** [itscalledsoccer-js](https://github.com/American-Soccer-Analysis/itscalledsoccer-js)

---

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for code of conduct, development setup, pull request process, and issue reporting.

---

## License

MIT © itscalledsoccer authors
