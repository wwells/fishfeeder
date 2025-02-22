import RPi.GPIO as GPIO
import time
import schedule
import logging
import argparse
from config import *

class FishFeeder:
    def __init__(self):
        self.setup_logging()
        self.setup_gpio()
        logging.info("Fish feeder initialized")

    def setup_logging(self):
        logging.basicConfig(
            filename=LOG_FILE,
            level=getattr(logging, LOG_LEVEL),
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SERVO_PIN, GPIO.OUT)
        self.servo = GPIO.PWM(SERVO_PIN, SERVO_FREQ)
        self.servo.start(0)
        logging.info("GPIO setup completed")

    def cleanup(self):
        self.servo.stop()
        GPIO.cleanup()
        logging.info("GPIO cleanup completed")

    def feed_fish(self):
        try:
            logging.info("Starting feed cycle")
            # TODO: Implement servo rotation logic
            logging.info("Feed cycle completed")
        except Exception as e:
            logging.error(f"Error during feeding: {str(e)}")

    def test_mode(self):
        logging.info(f"Starting test mode: {TEST_ITERATIONS} iterations")
        try:
            for i in range(TEST_ITERATIONS):
                logging.info(f"Test iteration {i+1}")
                self.feed_fish()
                time.sleep(TEST_INTERVAL)
        except KeyboardInterrupt:
            logging.info("Test mode interrupted by user")
        finally:
            self.cleanup()

def main():
    parser = argparse.ArgumentParser(description='Automatic Fish Feeder')
    parser.add_argument('--test', action='store_true', help='Run in test mode')
    args = parser.parse_args()

    feeder = FishFeeder()

    try:
        if args.test:
            feeder.test_mode()
        else:
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
