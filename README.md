# Serif Health Challenge

## Deliverable

- Script =>
- Set Up, also how to execute your solution code =>
- output URL list, prob in json form =>

- Assumptions
- How long did it take to write
- How long it took to run
- Tradeoffs

## Contributing

### General Guidelines

Please take a look at the following guides on writing code:

- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/) for Python

### Set Up Development Environment

1. Clone and navigate to the repository

```shell
cd ~/GitHub/issaloo
git clone git@github.com:issaloo/serif-health-challenge.git
```

2. Install pdm globally

```shell
pip install pdm
```

3. Install general & development packages with pdm

```shell
pdm install --dev
```

> :information_source: This will install packages [pre-commit](https://pre-commit.com/), [commitizen](https://commitizen-tools.github.io/commitizen/), and [gitlint](https://jorisroovers.com/gitlint/latest/)

(Optional) Install only the general packages

```shell
pdm install
```

3. Activate the virtual environment

```shell
eval $(pdm venv activate)
```

> :information_source: Virtual environment will use the same python version as the system

(Optional) Deactivate the virtual environment

```shell
deactivate
```
