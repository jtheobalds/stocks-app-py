# Stock Recommendation App

This is a Python application that will determine whether an investor should purchase stocks based on the stock market data of an input from the user. Data comes from [AlphaVantage API](https://www.alphavantage.co).

## Installing the program

In order to use the program, it must be installed. One must "fork" this repository and download the forked version using the GitHub.com online interface or the Git command-line interface. From the command-line, the repository can be downloaded by "cloning" it using:
```sh
git clone https://github.com/YOUR_USERNAME/stocks-app-py.git
```

After downloading your forked repository, navigate to the root directory:

```sh
cd stocks-app-py
```

Next, you will need to install the packages needed for the application. Depending on how your system requirements, use one of the commands for installation:

```sh
# Pipenv on Mac or Windows:
pipenv install -r requirements.txt

# Homebrew-installed Python 3.x on Mac OS:
pip3 install -r requirements.txt

# All others:
pip install -r requirements.txt
```

If you are using Pipenv, enter a new virtual environment (`pipenv shell`) before running any of the commands below.

All commands below assume you are running them from this repository's root directory.

## Setup

###Environment Variables
You will need to obtain an [AlphaVantage API Key](https://www.alphavantage.co/support/#api-key). This key will be used to access data from the website.

This key should be kept private. In order to keep it from being tracked in the main application, you will need to set up an environment variable named `ALPHAVANTAGE_API_KEY`. You may use the "dotenv" or ".env" method. However, this program runs under the assumption that the environment variable has been set up from the command line.

Mac users should be able to manage global environment variables using a hidden file called
`~/.bash_profile`. Open the file with your text editor (e.g. `atom ~/.bash_profile`), and place inside the following contents:

```sh
# ~/.bash_profile
export ALPHAVANTAGE_API_KEY="SecretPassword123"
```

Then exit and re-open your Terminal for the changes to take effect.

Windows users can set local environment variables from the command-line using the `set` keyword:

```sh
# Windows Command Prompt:
set ALPHAVANTAGE_API_KEY="SecretPassword123"
```

> NOTE: if you close your command prompt and re-open it, you will need to re-set the environment variable.

### CSV File

In order to store the historical trade price data, a CSV file will need to be set up. This can also be done in the command line by running the prepare.py file:
```sh
# Homebrew-installed Python 3.x on Mac OS:
python3 app/prepare.py

# All others:
python app/prepare.py
```

## Run the app

After all of the preparation steps have been take, the recommendation app can be run:
```sh
# Homebrew-installed Python 3.x on Mac OS:
python3 app/robo_adviser.py

# All others:
python app/robo_adviser.py
```
