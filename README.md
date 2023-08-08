# itscalledsoccer

<img src="https://raw.githubusercontent.com/American-Soccer-Analysis/itscalledsoccer-r/main/man/figures/logo.png" align="right" height="175"/>

<!-- badges: start -->
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)
![PyPi Version](https://img.shields.io/pypi/v/itscalledsoccer.svg)
![Python tests](https://github.com/American-Soccer-Analysis/itscalledsoccer/actions/workflows/python-tests.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI download month](https://img.shields.io/pypi/dm/itscalledsoccer.svg)](https://pypi.python.org/pypi/itscalledsoccer/)
<!-- badges: end -->

---

:warning: **`itscalledsoccer` has been split up into multiple repositories. If you're looking for the R or JavaScript version, check out the links below** :warning::

- [itscalledsoccer-r](https://github.com/American-Soccer-Analysis/itscalledsoccer-r)
- [itscalledsoccer-js](https://github.com/American-Soccer-Analysis/itscalledsoccer-js)

---

## Table of Contents

- [itscalledsoccer](#itscalledsoccer)
  - [Table of Contents](#table-of-contents)
  - [Background](#background)
  - [Install](#install)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [License](#license)

## Background

`itscalledsoccer` is a wrapper around the same API that powers the [American Soccer Analysis app](https://app.americansocceranalysis.com/). It enables Python users to programmatically retrieve advanced analytics for their favorite [MLS](https://en.wikipedia.org/wiki/Major_League_Soccer), [NWSL](https://en.wikipedia.org/wiki/National_Women%27s_Soccer_League), and [USL](https://en.wikipedia.org/wiki/United_Soccer_League) players and teams.

## Install

```sh
pip install itscalledsoccer
```

To install a development version, clone this repo and run the following command.

```sh
pip install --editable itscalledsoccer/python-package
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

## Contributing

Feel free to open an issue or submit a pull request.

## License

MIT © itscalledsoccer authors
