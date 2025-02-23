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
    python3 -m venv .venv
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

## Hardware Requirements

- Raspberry Pi
- Stepper Motor (28BYJ-48 with ULN2003 driver)
  - Step Angle: 5.625° × 1/64
  - Steps per Revolution: 512 (using half-stepping)
- Fish Food Dispenser Disk
