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
FEED_TIME = "08:00"  # 24-hour format
FEED_DURATION = 1  # seconds to hold position
FEEDS_PER_DAY = 2  # Number of feed compartments to dispense daily
SCHEDULER_HEARTBEAT = 300  # How often to check schedule in production (seconds)

# Recovery settings
RECOVERY_MODE = "feed"  # Options: "feed" or "skip"
MAX_RECOVERY_DELAY = 3600  # Maximum seconds after missed feed to attempt recovery (1 hour)
RECOVERY_ENABLED = True  # Enable/disable recovery handling

# Test mode settings
TEST_INTERVAL = 5    # seconds between feeds in test mode
TEST_ITERATIONS = 2  # number of test feeds to perform
TEST_SCHEDULE_ITERATIONS = 3  # number of schedule test feeds to perform
TEST_SCHEDULE_INTERVAL = 10  # Seconds between feeds when testing schedule
TEST_SCHEDULER_HEARTBEAT = 5 # How often to check schedule in test mode (seconds)

# Logging
LOG_FILE = "fishfeeder.log"
LOG_LEVEL = "INFO"
# Log rotation settings
LOG_MAX_SIZE = 1024 * 1024  # 1MB
LOG_BACKUP_COUNT = 5        # Keep 5 backup files

# Add to config.py
STATE_FILE = "feeder_state.json"  # Track last feed time and active status
