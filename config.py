# Stepper Motor configuration
STEPPER_PINS = [17, 18, 27, 22]  # GPIO pins in BCM mode
STEPS_PER_REVOLUTION = 2048      # From motor datasheet
STEPS_PER_FEED = (2048 // 14) // 2  # Half of 1/14th rotation (about 73 steps)
CLOCKWISE = True                 # Direction of rotation
STEP_DELAY = 0.01               # Delay between steps (controls speed)

# Schedule settings
FEED_TIME = "10:00"  # 24-hour format
FEED_DURATION = 1    # seconds to hold position

# Test mode settings
TEST_INTERVAL = 10   # seconds between feeds in test mode
TEST_ITERATIONS = 5  # number of test feeds to perform

# Logging
LOG_FILE = "fishfeeder.log"
LOG_LEVEL = "INFO"
