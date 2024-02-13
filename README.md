# Serif Health Challenge

## DELIVERABLE

### Deliverable Table

| Name         | File Path                 | Description                                                                                                                                |
| ------------ | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Script       | main.py                   | The script or code used to parse the file and produce output.                                                                              |
| Package File | pyproject.toml            | The setup or packaging file(s) required to bootstrap and execute your solution code.                                                       |
| URL List     | list_of_anthem_ny_ppo.csv | The output URL list.                                                                                                                       |
| README       | README.md                 | A README file, explaining your solution, how long it took you to write, how long it took to run, and the tradeoffs you made along the way. |

### Instructions - Running The Code

1. [Set up Environment](#set-up-development-environment)
2. Create the `data` folder at the root of the directory
3. Download and move the [input file](https://antm-pt-prod-dataz-nogbd-nophi-us-east1.s3.amazonaws.com/anthem/2024-02-01_anthem_index.json.gz) to data folder in this repository (local)
4. Run the script, whether in terminal or using your IDE

### Write-Up

#### Assumptions

- URLs
  - URLs of interest are in the location field in the Reporting Structure Object
  - Location field does not have missing values or empty strings
- Anthem and Highmark - which are separate providers under the same network - can use the same in_network_files, as long as the plan_name field in the Reporting Plans Object contains the provider name
- Filtering for Anthem's PPO in New York state
  - If Anthem, then it should be found in the plan_name field in the Reporting Plans Object
  - If NY, then it should be found in the description field in the in_network_files array
  - If PPO, then it should be found in the description field in the in_network_files array
  - All three conditions above must be satisfied for it to be Anthem's PPO in New York state

#### Performance & Time to Complete

Time To Complete

- Coding took ~1.5 hours
- Research took ~.5 hours

Performance

- Decompressing File - 60.33 Seconds
- Getting URLs - 117.38 Seconds
- Outputting to File - 0.002 Seconds

#### Tradeoffs

- Streaming URL vs Downloading File to Local
  - Chose to download file for simplicity and speed
  - However, streaming data via URL saves local storage space
- Streaming vs Batch Unzip
  - Chose to batch unzip (i.e., all at once) for simplicity. Did not find a way to stream unzip
  - However, streaming the unzip saves local storage space and can combine with the getting url process
- Unzipping manually vs programmatically
  - Chose to unzip programmatically for automation purposes
  - However, unzipping manually would have been simpler
- Parametrizing vs Hard-Coding Filtering
  - Chose to add parameters, so you can filter to different provider, state, and plan type
  - However, this takes more time to add
- Adding more regex vs keeping it simple
  - Chose to use less regex and not account for more edge cases for simplicity and speed
  - However, I may not have captured cases where the state is abbreviated (e.g., NY, OH) or if there are typos (e.g., New York <= two spaces)
- Using sets vs lists to store the URLs
  - I believed that duplicate information is not valuable, so I went with adding to a set instead of a list
  - However, I lose information on how many times the URL appears
- Writing in Functions vs Single File
  - Creating the steps with functions for reusability and clear steps
  - However, this takes more time to add
- Multiprocessing vs Not for Getting URLs
  - Attempted but ended up not doing so for the sake of time. You could use the multiprocessing package and the task would be going through an object
  - However, this is possible to do given that adding URLs to a set can be done async

#### Answering the Hints & Pointers

- How do you handle the file size and format efficiently, when the uncompressed file will exceed memory limitations on most systems?
  - Streaming is useful in this case
- When you look at your output URL list, which segments of the URL are changing, which segments are repeating, and what might that mean?
  - Changing
    - e.g., "01_of_02" => the data was split and there may be more relevant data files
    - e.g., Expires="INTEGER" => can mean the expiration date based on when the data was published
    - domain name => different rates across states for Anthem NY PPO?
  - Repeating
    - Key-Pair="ALPHANUMERIC" => could be an identifier based on locality, plan type, provider... but not sure
    - Date "2024-02" => valid rates for the month
- Is the description field helpful? Complete? Is Highmark the same as Anthem?
  - Helpful, but not complete. Description did not contain "Anthem", however the Anthem rates can be the same as Highmark.
- Anthem has an interactive MRF lookup system. This lookup can be used to gather additional information - but it requires you to input the EIN or name of an employer who offers an Anthem health plan: Anthem EIN lookup. How can you find a business likely to be in the Anthem NY PPO? How can you use this tool to confirm which underlying file(s) represent the Anthem NY PPO?
  - You could use the state as a prefix (e.g., "New York") to find companies in New York that may offer the Anthem health plan. You could then confirm which underlying files represent the Anthem NY PPO by looking at the URL and seeing if it contains "NY" and "PPO".

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

4. Activate the virtual environment

```shell
eval $(pdm venv activate)
```

> :information_source: Virtual environment will use the same python version as the system

(Optional) Deactivate the virtual environment

```shell
deactivate
```
