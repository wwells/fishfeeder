# Automatic Fish Feeder

Raspberry Pi-powered automatic fish feeder that dispenses food on a daily schedule.

## Setup

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure your settings in `config.py`
4. Run the feeder: `python feeder.py`

## Usage

- Normal mode: `python feeder.py`
- Test mode: `python feeder.py --test`

## Hardware Requirements

- Raspberry Pi
- Servo Motor
- Fish Food Dispenser Disk


## TODO

setup the venv, .bashrc to init the venv at ssh login

if [ -d "$HOME/ServoFishFeeder" ]; then
    cd "$HOME/ServoFishFeeder"
    if [ -f ".venv/bin/activate" ]; then
        source .venv/bin/activate
    fi
fi
