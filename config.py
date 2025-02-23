# Stepper Motor configuration
STEPPER_PINS = [17, 18, 27, 22]  # GPIO pins in BCM mode
STEPS_PER_FEED = 37             # 1/14th rotation (512 steps per revolution / 14 ≈ 36.57)
CLOCKWISE = True                # Direction of rotation
STEP_DELAY = 0.01              # Delay between steps (controls speed)

# Motor specs (28BYJ-48):
# - Step angle: 5.625° × 1/64
# - Using half-stepping (8 step sequence)
# - Full revolution = 512 steps (360° / (5.625° × 1/64) × 8)

# Schedule settings
FEED_TIME = "10:00"  # 24-hour format
FEED_DURATION = 1    # seconds to hold position

# Test mode settings
TEST_INTERVAL = 5    # seconds between feeds in test mode
TEST_ITERATIONS = 2  # number of test feeds to perform

# Logging
LOG_FILE = "fishfeeder.log"
LOG_LEVEL = "INFO"

# Add to config.py
STATE_FILE = "feeder_state.json"  # Track last feed time and active status
