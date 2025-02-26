# Fish Feeder Project Notes

Shared project specification to support ai coding sessions.

## Components

### Hardware
- Raspberry Pi (any model with GPIO)
- Stepper Motor (28BYJ-48 with ULN2003 driver)
- 3D Printed Food Dispenser Disk (14 compartments)
- Power Supply
- Fish Food Container

### Software Components
1. **GPIO Control**
   - Servo motor control
   - PWM signal generation
   - Stepper motor control
   - Step sequence handling
   - Pin initialization and cleanup

2. **Scheduling System**
   - Daily feeding timer
   - Schedule configuration
   - Time management

3. **Configuration Management**
   - Servo parameters
   - Timing settings
   - GPIO pin mappings

4. **Logging System**
   - Operation logging
   - Error tracking
   - Debug information

5. **Testing Interface**
   - Test mode for calibration
   - Hardware verification
   - Feed cycle testing

## Development Plan

### Phase 1: Basic Setup ✅
- [x] Project structure
- [x] Python environment setup
    - [x] Create virtual environment
    - [x] Install dependencies
    - [x] Configure .bashrc for auto-activation
- [x] Basic GPIO configuration
- [x] Initial logging setup
- [x] Stepper motor control
- [x] Basic CLI arguments
- [x] Test mode implementation
- [x] Calibration mode

### Phase 2: Core Functions ✅
- [x] Implement feed_fish() method
- [x] Motor step calculations
- [x] Test rotation accuracy
- [x] Calibrate timing
- [x] Basic error handling
- [x] Adjust feed amount
    - [x] Add FEEDS_PER_DAY to config
    - [x] Update feed_fish() to handle multiple rotations
    - [x] Test with actual food amounts

### Phase 3: Scheduling ✅
- [x] Test schedule functionality
    - [x] Test with shorter intervals for verification (--test-schedule)
    - [x] Verify timing accuracy
    - [x] Test schedule.every().day behavior
- [x] Enhance schedule logging
    - [x] Log next scheduled feed time on startup
    - [x] Log schedule changes/interruptions
    - [x] Add state file tracking
        - [x] Track feed success/failure
        - [x] Track feed counts
        - [x] Add test mode for state verification
- [x] Implement recovery handling
    - [x] Use state file to detect missed feeds
    - [x] Define recovery behavior (skip vs feed)
    - [x] Test recovery scenarios

### Phase 4: Production Ready ✅
- [x] Create systemd service file
    - [x] Configure with venv path
    - [x] Set up auto-restart
    - [x] Configure logging
    - [x] Test service operation
- [x] Implement log rotation
    - [x] Add max log size
    - [x] Configure backup count
    - [x] Test log cleanup
- [x] Add status monitoring
    - [x] Basic status (last feed, active state)
    - [x] Next scheduled feed time
    - [x] Feed success/failure stats
- [x] Complete documentation
    - [x] Usage instructions
    - [x] Configuration guide
    - [x] Troubleshooting steps

## Testing Checklist
- [x] Motor rotation accuracy
- [x] Food dispensing reliability
- [x] Schedule accuracy
- [x] Error recovery
- [x] Power cycle behavior

## Configuration Notes
- Virtual environment: .venv in project directory
- Auto-activation via .bashrc
- Steps per feed: 37 (1/14th of 512)
- Feed schedule: Once daily at 10:00
- Test mode: 5 iterations, 5s apart
- Logging: Both file and console
