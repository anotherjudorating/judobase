# Judobase API Wrapper

[![PyPI](https://img.shields.io/pypi/v/judobase)](https://pypi.org/project/judobase/)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Downloads](https://img.shields.io/pypi/dm/judobase)](https://pypistats.org/packages/judobase)
[![License](https://img.shields.io/pypi/l/judobase)](https://opensource.org/licenses/MIT)
[![Docs](https://img.shields.io/badge/docs-stable-brightgreen)](https://anotherjudorating.github.io/judobase/)
[![Codecov](https://img.shields.io/codecov/c/gh/anotherjudorating/judobase)](https://app.codecov.io/gh/anotherjudorating/judobase)
[![Contributors](https://img.shields.io/github/contributors/anotherjudorating/judobase)](https://github.com/anotherjudorating/judobase/graphs/contributors)
[![Ruff](https://img.shields.io/badge/linting-ruff-orange)](https://github.com/astral-sh/ruff)


Judobase API Wrapper is a Python library that provides a async interface to interact with the Judobase API. Developed entirely through reverse engineering, this wrapper allows developers to access and integrate Judobase data effortlessly into their projects.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Features

- **Reverse Engineered:** Reverse engineered base Judobase API methods. Access to data 
on tournaments, athletes, results is available by python classes `JudokaAPI`, `CompetitionAPI`, `ContestAPI`, `CountryAPI`. 
- **Extension:** Implemented additional methods to the API to make it more user-friendly. 
Look at `JudoBase` class.
- **Pydantic Schemas:** All data is returned as Pydantic models, making it easy to work with.
- **Async:** All requests are asynchronous, allowing for faster data retrieval.

---

## Installation

### Requirements

- **Python 3.10+**
- **pip** (Python package installer)

### pip

```bash
pip install judobase
```

---

## Usage

After installing the library, you can easily integrate it into your project. Below is a basic usage example:

```python
import asyncio

from judobase import JudoBase, Competition, Contest


async def main():
    async with JudoBase() as api:
        contests: list[Contest] = await api.all_contests()
        print(len(contests)) # Output: 195161

    api = JudoBase()
    olympic_games_2024: Competition = await api.competition_by_id(2653)
    print(olympic_games_2024.city) # Output: Paris
    await api.close_session()

asyncio.run(main())
```

### Key classes

- `JudoBase`: Main class that provides access to user-friendly methods.
- `JudokaAPI`: Base methods for fetching data about athletes.
- `CompetitionAPI`: Base methods for fetching data about competitions.
- `ContestAPI`: Base methods for fetching data about contests.
- `CountryAPI`: Base methods for fetching data about countries.

---

## Upgrading to 3.0

Version 3.0 returns values with their real types instead of the raw strings of the API:

- Ids are `int`: `id_fight`, `id_competition`, `id_country`, `id_person_blue`, ...
- "Unknown" values (`0`, `"0"`, `""`) are `None`: `id_winner` before a contest is decided,
  fighters before the draw sets them, `dob_year`, `id_weight`, ...
- `Competition.date_from` / `date_to` are `datetime.date` (they were `datetime` at midnight UTC).
- Unknown times are `None` instead of 1970-01-01: `Contest.date_start_ts`,
  `Contest.first_hajime_at_ts`, `Judoka.birth_date`.
- `Contest.bye` and `Competition.is_teams` are `bool`.
- `Competition.has_results` is still `int`: it is the number of results, not a flag.
- Methods taking ids accept both `int` and `str`.
- The request timeout can be set: `JudoBase(timeout=30)` (10 seconds by default).

```python
# 2.x
if contest.id_winner != "0" and contest.id_winner == contest.id_person_blue: ...
# 3.x
if contest.id_winner is not None and contest.id_winner == contest.id_person_blue: ...
```

---

## Documentation

For a detailed description of all available methods and endpoints, please refer to the [Documentation](https://anotherjudorating.github.io/judobase/).

---

## Contributing

Contributions are welcome! Also, if you have any questions or suggestions, please feel free to open an [issue](https://github.com/anotherjudorating/judobase/issues).

> **Note:** See [CONTRIBUTING.md](.github/CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](.github/CODE_OF_CONDUCT.md) for details on how to contribute..


---

## License

This project is licensed under the [MIT License](LICENSE). See the LICENSE file for more details.

---

## Contact

If you have any questions or suggestions, please feel free to reach out:

- **GitHub:** [DavidDzgoev](https://github.com/DavidDzgoev)
- **Email:** ddzgoev@gmail.com

> **Important:** This project is not an official Judobase solution. It is an API wrapper developed through reverse engineering of the Judobase API.
