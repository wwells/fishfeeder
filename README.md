# Automatic Fish Feeder

Raspberry Pi-powered automatic fish feeder that dispenses food on a daily schedule.

## Setup

1. Clone this repository
2. Set up Python environment:
    ```bash
    # Install required system package
    sudo apt-get update
    sudo apt-get install python3-venv

    # Create and activate virtual environment
    python3.11 -m venv .venv
    source .venv/bin/activate

    # Install dependencies
    pip install -r requirements.txt

    # For easier use, when sshing into the pi,
    # can add this to .bashrc in the pi
    if [ -d "$HOME/fishfeeder" ]; then
        cd "$HOME/fishfeeder"
        if [ -f ".venv/bin/activate" ]; then
            source .venv/bin/activate
        fi
    fi
    ```
3. Configure your settings in `config.py`
4. Run the feeder: `python feeder.py`

## Usage

- Normal mode: `python feeder.py`
- Test mode: `python feeder.py --test`
- Calibration mode: `python feeder.py --calibrate`

## Hardware Requirements

- Raspberry Pi
- Stepper Motor (28BYJ-48 with ULN2003 driver)
  - Step Angle: 5.625° × 1/64
  - Steps per Revolution: 512 (using half-stepping)
- 3d Print base disk / compartment disk

## 3d Printing assets

Inspired by https://www.the-diy-life.com/make-an-arduino-based-automatic-fish-feeder/.   Assets for printing are in the assets dir.

## Timezones

Remain super fun ;)   Be sure your PI is set to the desired timezone to ensure the schedule meets your expectations (`sudo raspi-config` and select `Localisation`)
