# GPIO configuration
SERVO_PIN = 18  # GPIO pin number for servo control

# Servo settings
SERVO_FREQ = 50  # Standard frequency for most servos (50Hz)
SERVO_MIN_DUTY = 2.5  # Duty cycle for 0 degrees (adjust based on your servo)
SERVO_MAX_DUTY = 12.5  # Duty cycle for 180 degrees (adjust based on your servo)
SERVO_STEP_ANGLE = 30  # Degrees to rotate for each feed

# Schedule settings
FEED_TIME = "10:00"  # 24-hour format
FEED_DURATION = 1  # seconds to hold position

# Test mode settings
TEST_INTERVAL = 10  # seconds between feeds in test mode
TEST_ITERATIONS = 5  # number of test feeds to perform

# Logging
LOG_FILE = "fishfeeder.log"
LOG_LEVEL = "INFO"
