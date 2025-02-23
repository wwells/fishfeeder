import RPi.GPIO as GPIO
import time
import schedule
import logging
import argparse
import os
import sys
import json
from datetime import datetime
from config import *

class FishFeeder:
    def __init__(self):
        self.setup_logging()
        self.setup_gpio()
        # Full step sequence (might provide more torque)
        self.step_sequence = [
            [1,1,0,0],
            [0,1,1,0],
            [0,0,1,1],
            [1,0,0,1]
        ] if CLOCKWISE else [
            [1,0,0,1],
            [0,0,1,1],
            [0,1,1,0],
            [1,1,0,0]
        ]
        logging.info("Fish feeder initialized")

    def setup_logging(self):
        # Create log directory if it doesn't exist
        log_dir = os.path.dirname(LOG_FILE)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Set up logging to file
        logging.basicConfig(
            level=getattr(logging, LOG_LEVEL),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                # File handler
                logging.FileHandler(LOG_FILE),
                # Console handler
                logging.StreamHandler()
            ]
        )

        # Optionally increase verbosity for test mode
        if '--test' in sys.argv:
            logging.getLogger().setLevel(logging.DEBUG)
            logging.debug("Debug logging enabled for test mode")

    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        # Setup all pins as outputs
        for pin in STEPPER_PINS:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
        logging.info("GPIO setup completed")

    def cleanup(self):
        for pin in STEPPER_PINS:
            GPIO.output(pin, GPIO.LOW)
        GPIO.cleanup()
        logging.info("GPIO cleanup completed")

    def stepper_step(self, steps):
        """Rotate stepper motor by given number of steps"""
        logging.debug(f"Moving stepper motor {steps} steps")
        try:
            for step_count in range(1, abs(steps) + 1):
                for step in self.step_sequence:
                    for i in range(len(STEPPER_PINS)):
                        GPIO.output(STEPPER_PINS[i], step[i])
                    time.sleep(STEP_DELAY)

                # Optional: log progress for long rotations
                if step_count % 50 == 0:
                    logging.debug(f"Completed {step_count} of {steps} steps")

            # Turn off all pins after moving
            for pin in STEPPER_PINS:
                GPIO.output(pin, GPIO.LOW)
        except Exception as e:
            logging.error(f"Error during step: {str(e)}")
            raise

    def feed_fish(self):
        try:
            logging.info("Starting feed cycle")
            logging.debug(f"Rotating {STEPS_PER_FEED} steps")
            self.stepper_step(STEPS_PER_FEED)
            self.save_state()  # Record successful feed
            logging.info("Feed cycle completed")
        except Exception as e:
            logging.error(f"Error during feeding: {str(e)}")

    def test_mode(self):
        logging.info(f"Starting test mode: {TEST_ITERATIONS} iterations")
        try:
            for i in range(TEST_ITERATIONS):
                logging.info(f"Test iteration {i+1}")
                self.feed_fish()
                self.feed_fish()
                time.sleep(TEST_INTERVAL)
        except KeyboardInterrupt:
            logging.info("Test mode interrupted by user")

    def calibrate_mode(self):
        """Perform one full revolution to verify steps calculation"""
        try:
            logging.info("Starting calibration - one full revolution")
            logging.info("Using 511 steps for full revolution")
            self.stepper_step(511)
            logging.info("Calibration complete - verify the motor made exactly one full turn")
        except Exception as e:
            logging.error(f"Error during calibration: {str(e)}")

    def save_state(self):
        state = {
            'last_feed': datetime.now().isoformat(),
            'active': True
        }
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f)

    def load_state(self):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {'last_feed': None, 'active': False}

def main():
    parser = argparse.ArgumentParser(description='Automatic Fish Feeder')
    parser.add_argument('--test', action='store_true', help='Run in test mode')
    parser.add_argument('--calibrate', action='store_true', help='Run calibration mode')
    parser.add_argument('--status', action='store_true', help='Show feeder status and exit')
    args = parser.parse_args()

    feeder = FishFeeder()

    try:
        if args.status:
            state = feeder.load_state()
            if state['last_feed']:
                logging.info(f"Status: Last feed: {state['last_feed']}, Active: {state['active']}")
            else:
                logging.info("Status: No previous feeds recorded")
            return

        if args.calibrate:
            feeder.calibrate_mode()
        elif args.test:
            feeder.test_mode()
        else:
            # Load last state
            state = feeder.load_state()
            if state['last_feed']:
                last_feed = datetime.fromisoformat(state['last_feed'])
                logging.info(f"Last feed occurred at: {last_feed}")

            schedule.every().day.at(FEED_TIME).do(feeder.feed_fish)
            logging.info(f"Scheduled daily feeding at {FEED_TIME}")

            while True:
                schedule.run_pending()
                time.sleep(60)
    except KeyboardInterrupt:
        logging.info("Program interrupted by user")
    finally:
        feeder.cleanup()

if __name__ == "__main__":
    main()
