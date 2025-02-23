# Fish Feeder Project Notes

Shared project plan documentation to support ai coding sessions.

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

### Phase 2: Core Functions ⏳
- [x] Implement feed_fish() method
- [x] Motor step calculations
- [x] Test rotation accuracy
- [x] Calibrate timing
- [x] Basic error handling
- [ ] Adjust feed amount
    - [ ] Add FEEDS_PER_DAY to config
    - [ ] Update feed_fish() to handle multiple rotations
    - [ ] Test with actual food amounts

### Phase 3: Scheduling (Next Up)
- [ ] Test schedule functionality
    - [ ] Test with shorter intervals for verification
    - [ ] Verify timing accuracy
    - [ ] Test schedule.every().day behavior
- [ ] Enhance schedule logging
    - [ ] Log next scheduled feed time on startup
    - [ ] Log schedule changes/interruptions
- [ ] Implement recovery handling
    - [ ] Use state file to detect missed feeds
    - [ ] Define recovery behavior (skip vs feed)
    - [ ] Test recovery scenarios

### Phase 4: Production Ready
- [ ] Create systemd service file
    - [ ] Configure with venv path
    - [ ] Set up auto-restart
    - [ ] Configure logging
- [ ] Implement log rotation
    - [ ] Add max log size
    - [ ] Configure backup count
    - [ ] Test log cleanup
- [ ] Add status monitoring
    - [x] Basic status (last feed, active state)
    - [ ] Next scheduled feed time
    - [ ] Feed success/failure stats
    - [ ] GPIO/hardware status
    - [ ] Service status
- [ ] Complete documentation
- [ ] Include 3d printer files and any photo assets

## Testing Checklist
- [x] Motor rotation accuracy
- [ ] Food dispensing reliability
- [ ] Schedule accuracy
- [ ] Error recovery
- [ ] Power cycle behavior

## Configuration Notes
- Virtual environment: .venv in project directory
- Auto-activation via .bashrc
- Steps per feed: 37 (1/14th of 512)
- Feed schedule: Once daily at 10:00
- Test mode: 5 iterations, 5s apart
- Logging: Both file and console
