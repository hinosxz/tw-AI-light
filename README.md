# tw-AI-light
AI aiming at winning a game of Vampires vs Werewolves.
See a non-official implementation of the game server here:
https://github.com/Succo/twilight

![Game board](images/board.png)

## Implementation details
A detailed explanation of our strategies and algorithms is available (in French) [here](DETAILS.md)

## How to play

### Requirements
You need python 3.7+ to run this AI.

### Installation
Clone this repo to your local machine using
```shell script
git clone https://github.com/hinosxz/tw-AI-light.git
```

### Usage
Once the server is started and waiting for players, navigate to the root
of this repository and run:
```shell script
python main.py --name player_name --host host_ip --port host_port
```

List of optional parameters
- `name` the in-game name of your player. Default: `Group 3`
- `host` IP address of the game server. Default: `127.0.0.1`
- `port` port on which to access the game server. Default: `5555`
- `heuristic` for debugging purposes. Default: `heuristic2`

## Development setup

We suggest using a virtual environment with python 3.7+
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

To enable pre-commit hooks and benefit from black auto-formatting
```
pre-commit install
```

## Authors
*Quentin Churet, Gauthier Hénon, Alexandre Lainé, Barthélémy Lancelot and Hortense Masurel*
