<!-- omit in toc -->
# itscalledsoccer

<div align="center">
    <img src="https://raw.githubusercontent.com/American-Soccer-Analysis/itscalledsoccer-r/main/man/figures/logo.png" align="center" height="175"/>
</div>

<br>


<!-- badges: start -->
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)
![PyPi Version](https://img.shields.io/pypi/v/itscalledsoccer.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/itscalledsoccer)
![Python tests](https://github.com/American-Soccer-Analysis/itscalledsoccer/actions/workflows/python-tests.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI download month](https://img.shields.io/pypi/dm/itscalledsoccer.svg)](https://pypi.python.org/pypi/itscalledsoccer/)
[![codecov](https://codecov.io/github/American-Soccer-Analysis/itscalledsoccer/graph/badge.svg?token=RUWMM7ZLQ2)](https://codecov.io/github/American-Soccer-Analysis/itscalledsoccer)
<!-- badges: end -->

<!-- omit in toc -->
## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Other versions](#other-versions)
- [Contributing](#contributing)
- [License](#license)

## Background

`itscalledsoccer` is a wrapper around the same API that powers the [American Soccer Analysis app](https://app.americansocceranalysis.com/). It enables Python users to programmatically retrieve advanced analytics for their favorite [MLS](https://en.wikipedia.org/wiki/Major_League_Soccer), [NWSL](https://en.wikipedia.org/wiki/National_Women%27s_Soccer_League), and [USL](https://en.wikipedia.org/wiki/United_Soccer_League) players and teams.

## Install

```sh
pip install itscalledsoccer
```

## Usage

```python
from itscalledsoccer.client import AmericanSoccerAnalysis

asa_client = AmericanSoccerAnalysis()
```

Any of the `get_*` methods can be used to retrieve the same data made available in the [American Soccer Analysis app](https://app.americansocceranalysis.com/). Partial matches or abbreviations are accepted for any player or team names. For most methods, arguments _must be named_. A few examples are below.

```python
# Get all players named "Andre"
asa_players = asa_client.get_players(names="Andre")
```

For more information, check out the [documentation site](https://american-soccer-analysis.github.io/itscalledsoccer/).

## Other versions

- [itscalledsoccer-r](https://github.com/American-Soccer-Analysis/itscalledsoccer-r)
- [itscalledsoccer-js](https://github.com/American-Soccer-Analysis/itscalledsoccer-js)

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md)

## License

MIT © itscalledsoccer authors