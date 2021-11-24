# itscalledsoccer

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

## Table of Contents

- [itscalledsoccer](#itscalledsoccer)
  - [Table of Contents](#table-of-contents)
  - [Install](#install)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [License](#license)

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

```python
# Get all players named "Andre"
asa_players = asa_client.get_players(names="Andre")
```

## Contributing

Feel free to open an issue or submit a pull request.

## License

MIT © itscalledsoccer authors
