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
from config import (RECOVERY_ENABLED, RECOVERY_MODE, MAX_RECOVERY_DELAY,
                   FEED_TIME, SCHEDULER_HEARTBEAT, TEST_SCHEDULER_HEARTBEAT,
                   TEST_SCHEDULE_INTERVAL, TEST_SCHEDULE_ITERATIONS)
from logging.handlers import RotatingFileHandler

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
                # Rotating file handler
                RotatingFileHandler(
                    LOG_FILE,
                    maxBytes=LOG_MAX_SIZE,
                    backupCount=LOG_BACKUP_COUNT
                ),
                # Console handler
                logging.StreamHandler()
            ]
        )

        # Optionally increase verbosity for test modes
        if '--test-hardware' in sys.argv or '--test-schedule' in sys.argv:
            logging.getLogger().setLevel(logging.DEBUG)
            logging.debug("Debug logging enabled for testing")

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

    def feed_fish(self, rotations=None):
        """Feed fish with specified number of rotations (defaults to FEEDS_PER_DAY)"""
        try:
            rotations = rotations or FEEDS_PER_DAY
            logging.info("Starting feed cycle")
            for i in range(rotations):
                logging.debug(f"Rotation {i+1}/{rotations}: {STEPS_PER_FEED} steps")
                self.stepper_step(STEPS_PER_FEED)
            self.save_state()  # Record successful feed
            logging.info("Feed cycle completed")
        except Exception as e:
            # Save failed state
            state = {
                'last_feed': datetime.now().isoformat(),
                'active': True,
                'feed_count': self.load_state().get('feed_count', {'total': 0, 'successful': 0, 'failed': 0}),
                'last_feed_status': 'failed',
                'next_scheduled_feed': self.get_next_feed_time()
            }
            state['feed_count']['total'] += 1
            state['feed_count']['failed'] += 1
            with open(STATE_FILE, 'w') as f:
                json.dump(state, f)
            logging.error(f"Error during feeding: {str(e)}")
            raise

    def test_mode(self):
        logging.info(f"Starting test mode: {TEST_ITERATIONS} iterations")
        try:
            for i in range(TEST_ITERATIONS):
                logging.info(f"Test iteration {i+1}")
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
            'active': True,
            'feed_count': {
                'total': 0,
                'successful': 0,
                'failed': 0
            },
            'last_feed_status': 'success',
            'next_scheduled_feed': self.get_next_feed_time()
        }
        # Load existing state to preserve counts
        try:
            old_state = self.load_state()
            if old_state.get('feed_count'):
                state['feed_count'] = old_state['feed_count']
                state['feed_count']['total'] += 1
                state['feed_count']['successful'] += 1
        except Exception as e:
            logging.warning(f"Could not load previous state: {e}")

        with open(STATE_FILE, 'w') as f:
            json.dump(state, f)

    def load_state(self):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {'last_feed': None, 'active': False}

    def get_next_feed_time(self):
        """Calculate and return the next scheduled feed time"""
        next_run = schedule.next_run()
        if next_run:
            return next_run.strftime("%Y-%m-%d %H:%M:%S")
        return None

    def check_missed_feeds(self):
        """Check for and handle any missed feeds"""
        if not RECOVERY_ENABLED:
            return

        state = self.load_state()
        if not state['last_feed']:
            return

        last_feed = datetime.fromisoformat(state['last_feed'])
        scheduled_feed = datetime.strptime(f"{datetime.now():%Y-%m-%d} {FEED_TIME}", "%Y-%m-%d %H:%M")

        # If we're past feed time and haven't fed today
        if datetime.now() > scheduled_feed and last_feed.date() < datetime.now().date():
            delay = (datetime.now() - scheduled_feed).total_seconds()

            if delay <= MAX_RECOVERY_DELAY:
                if RECOVERY_MODE == "feed":
                    logging.warning(f"Missed feed detected. Last feed: {last_feed}. Recovering...")
                    self.feed_fish()
                else:
                    logging.warning(f"Missed feed detected. Last feed: {last_feed}. Skipping...")
            else:
                logging.warning(f"Missed feed detected but outside recovery window ({delay}s > {MAX_RECOVERY_DELAY}s)")

def main():
    parser = argparse.ArgumentParser(description='Automatic Fish Feeder')
    parser.add_argument('--test-hardware', action='store_true', help='Run hardware test - feed cycles with short delay')
    parser.add_argument('--calibrate', action='store_true', help='Run calibration mode')
    parser.add_argument('--status', action='store_true', help='Show feeder status and exit')
    parser.add_argument('--test-schedule', action='store_true',
                       help='Test schedule with shorter intervals (every few minutes)')
    parser.add_argument('--test-state', action='store_true',
                       help='Test state file handling with success/failure scenarios')
    parser.add_argument('--test-recovery', action='store_true',
                       help='Test recovery handling with simulated missed feeds')
    parser.add_argument('--test-service', action='store_true',
                       help='Test service behavior (signal handling, cleanup)')
    parser.add_argument('--test-logs', action='store_true',
                       help='Test log rotation by generating log entries')
    args = parser.parse_args()

    feeder = FishFeeder()

    try:
        if args.status:
            state = feeder.load_state()
            if state['last_feed']:
                feed_count = state.get('feed_count', {'total': 0, 'successful': 0, 'failed': 0})
                status_msg = [
                    f"Last feed: {state['last_feed']}",
                    f"Status: {state.get('last_feed_status', 'unknown')}",
                    f"Active: {state['active']}",
                    f"Total feeds: {feed_count['total']}",
                    f"Successful: {feed_count['successful']}",
                    f"Failed: {feed_count['failed']}",
                    f"Next scheduled: {state.get('next_scheduled_feed', 'unknown')}"
                ]
                logging.info("Status:\n - " + "\n - ".join(status_msg))
            else:
                logging.info("Status: No previous feeds recorded")
            return

        if args.calibrate:
            feeder.calibrate_mode()
        elif args.test_hardware:
            feeder.test_mode()
        elif args.test_schedule:
            feeds_completed = 0

            def feed_with_counter():
                nonlocal feeds_completed
                feeder.feed_fish()
                feeds_completed += 1
                logging.info(f"Feed {feeds_completed}/{TEST_SCHEDULE_ITERATIONS} completed")
                if feeds_completed >= TEST_SCHEDULE_ITERATIONS:
                    return schedule.CancelJob

            schedule.every(TEST_SCHEDULE_INTERVAL).seconds.do(feed_with_counter)
            next_feed = feeder.get_next_feed_time()
            logging.info(f"Testing schedule every {TEST_SCHEDULE_INTERVAL} seconds")
            logging.info(f"Next feed scheduled for: {next_feed}")
            logging.info(f"Will run {TEST_SCHEDULE_ITERATIONS} times")

            while feeds_completed < TEST_SCHEDULE_ITERATIONS:
                time.sleep(TEST_SCHEDULER_HEARTBEAT)
                schedule.run_pending()
            logging.info("Schedule test completed")
        elif args.test_state:
            logging.info("Testing state file handling...")

            # Test successful feed
            logging.info("Testing successful feed...")
            feeder.feed_fish()
            logging.info("Checking state after success:")
            os.system(f"{sys.executable} {sys.argv[0]} --status")

            # Test failed feed by forcing an error
            logging.info("\nTesting failed feed...")
            try:
                # Temporarily modify STEPS_PER_FEED to force an error
                old_steps = STEPS_PER_FEED
                globals()['STEPS_PER_FEED'] = -1  # Invalid value
                feeder.feed_fish()
            except:
                globals()['STEPS_PER_FEED'] = old_steps
                logging.info("Expected error occurred")

            logging.info("Checking state after failure:")
            os.system(f"{sys.executable} {sys.argv[0]} --status")
        elif args.test_recovery:
            logging.info("Testing recovery handling...")

            # Simulate a missed feed by setting last feed to yesterday
            yesterday = datetime.now().replace(day=datetime.now().day-1)
            state = {
                'last_feed': yesterday.isoformat(),
                'active': True,
                'feed_count': {'total': 10, 'successful': 10, 'failed': 0},
                'last_feed_status': 'success'
            }
            with open(STATE_FILE, 'w') as f:
                json.dump(state, f)

            logging.info("Simulated missed feed. Checking recovery...")
            feeder.check_missed_feeds()
        elif args.test_service:
            logging.info("Testing service behavior...")

            def handle_sigterm(signum, frame):
                logging.info("Received SIGTERM signal")
                raise KeyboardInterrupt

            import signal
            signal.signal(signal.SIGTERM, handle_sigterm)

            logging.info("Service test started - will run for 30 seconds")
            logging.info("Test commands:")
            logging.info("  sudo systemctl status fishfeeder")
            logging.info("  sudo systemctl stop fishfeeder")

            # Schedule a few test feeds
            schedule.every(10).seconds.do(feeder.feed_fish)

            end_time = time.time() + 30
            while time.time() < end_time:
                schedule.run_pending()
                time.sleep(1)

            logging.info("Service test completed")
        elif args.test_logs:
            logging.info("Testing log rotation...")
            logging.info(f"Will generate logs until we exceed {LOG_MAX_SIZE/1024:.0f}KB")

            # Create a longer message to fill logs faster
            test_msg = "This is a longer test message with lots of text " * 10

            # Generate enough logs to trigger rotation
            for i in range(10000):
                logging.info(f"Test log entry {i}: {test_msg}")
                if i % 1000 == 0:
                    log_size = os.path.getsize(LOG_FILE)
                    logging.info(f"Generated {i} log entries. Log size: {log_size/1024:.1f}KB")
                    if log_size > LOG_MAX_SIZE * 2:
                        break

            # Check for rotated files
            import glob
            log_files = glob.glob(f"{LOG_FILE}.*")
            logging.info(f"Found {len(log_files)} rotated log files:")
            for log_file in log_files:
                size = os.path.getsize(log_file)
                logging.info(f"  - {log_file} ({size/1024:.1f}KB)")
        else:
            state = feeder.load_state()
            if state['last_feed']:
                last_feed = datetime.fromisoformat(state['last_feed'])
                logging.info(f"Last feed occurred at: {last_feed}")

            # Check for missed feeds on startup
            feeder.check_missed_feeds()

            schedule.every().day.at(FEED_TIME).do(feeder.feed_fish)
            next_feed = feeder.get_next_feed_time()
            logging.info(f"Scheduled daily feeding at {FEED_TIME}")
            logging.info(f"Next feed scheduled for: {next_feed}")

            while True:
                try:
                    schedule.run_pending()
                except Exception as e:
                    logging.error(f"Schedule interrupted: {str(e)}")
                time.sleep(SCHEDULER_HEARTBEAT)
    except KeyboardInterrupt:
        logging.warning("Program manually interrupted - schedule stopped")
        logging.info("Program interrupted by user")
    finally:
        feeder.cleanup()

if __name__ == "__main__":
    main()
