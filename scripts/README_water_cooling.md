# Water Cooling System Setup and Monitoring

This directory contains tools to monitor and control your Corsair water cooling system for the Living Truth Engine.

## System Overview

**Detected Hardware:**
- **Device**: Corsair Commander ST
- **Firmware**: 2.0.19
- **AIO Connected**: Yes
- **Water Temperature Sensor**: Yes
- **Fan Ports**: 6 (currently no fans connected)
- **Pump**: Active (2263 RPM)

## Current Status

- **Water Temperature**: 43.3°C (elevated)
- **Pump Speed**: 2263 RPM
- **Fan Status**: All fans disconnected
- **System Health**: Good (pump working, temperature monitoring active)

## Installed Software

### 1. `liquidctl` - Core Water Cooling Control
**Version**: 1.15.0
**Purpose**: Direct communication with Corsair water cooling devices

**Usage:**
```bash
# List devices
liquidctl list

# Initialize device
liquidctl initialize

# Get status
liquidctl status

# Set pump speed
liquidctl set pump speed 80

# Set fan speed
liquidctl set fan1 speed 60
```

### 2. `water_cooling_monitor.py` - Advanced Monitoring Script
**Purpose**: Comprehensive monitoring and automatic control

**Usage:**
```bash
# Monitor once
python scripts/water_cooling_monitor.py --once

# Monitor continuously
python scripts/water_cooling_monitor.py --interval 30

# Monitor with automatic control
python scripts/water_cooling_monitor.py --auto --interval 30

# Test all fans
python scripts/water_cooling_monitor.py --test-fans

# Set modes
python scripts/water_cooling_monitor.py --quiet
python scripts/water_cooling_monitor.py --performance

# Set specific speeds
python scripts/water_cooling_monitor.py --set-fan 1 80
python scripts/water_cooling_monitor.py --set-pump 90
```

## Temperature Guidelines

| Water Temperature | Status | Action | Fan Speed | Pump Speed |
|-------------------|--------|--------|-----------|------------|
| < 40°C | Normal | No action | 40% | 60% |
| 40-50°C | Elevated | Monitor | 60% | 70% |
| 50-60°C | Warning | Increase cooling | 80% | 80% |
| > 60°C | Critical | Emergency cooling | 100% | 100% |

## System Configuration

### Udev Rules
Created `/etc/udev/rules.d/99-corsair-liquidctl.rules` for proper device access:
- Allows non-root access to Corsair devices
- Supports all Corsair Commander variants
- Includes HID device access

### Device Permissions
- **Vendor ID**: 1b1c (Corsair)
- **Product IDs**: 0c32, 0c33 (Commander Core/Pro)
- **Access Mode**: 0666 (read/write for all users)
- **Group**: plugdev

## Troubleshooting

### Device Not Detected
1. Check USB connection
2. Verify udev rules: `ls /etc/udev/rules.d/99-corsair-liquidctl.rules`
3. Reload rules: `sudo udevadm control --reload-rules`
4. Check device: `lsusb | grep Corsair`

### Permission Errors
1. Add user to plugdev group: `sudo usermod -a -G plugdev $USER`
2. Log out and back in
3. Check group membership: `groups`

### High Water Temperature
1. Check pump operation: `liquidctl status`
2. Verify radiator airflow
3. Check for air bubbles in loop
4. Monitor CPU load and ambient temperature

### Fan Issues
1. Test individual fans: `python scripts/water_cooling_monitor.py --test-fans`
2. Check fan connections to Commander
3. Verify fan power supply
4. Test fan speeds manually

## Integration with Living Truth Engine

### Automatic Monitoring
The water cooling system integrates with the Living Truth Engine's monitoring infrastructure:

1. **Temperature Correlation**: Water temperature correlates with CPU load
2. **Docker Container Impact**: Heavy workloads increase water temperature
3. **Automatic Response**: System can automatically adjust cooling based on workload

### Recommended Setup
```bash
# Start automatic monitoring with 30-second intervals
python scripts/water_cooling_monitor.py --auto --interval 30

# Monitor alongside CPU temperatures
python scripts/monitor_fans.py --interval 30 &
python scripts/water_cooling_monitor.py --auto --interval 30 &
```

### Performance Profiles

#### Quiet Mode
- **Use Case**: Light workloads, quiet operation
- **Fan Speed**: 30%
- **Pump Speed**: 50%
- **Command**: `python scripts/water_cooling_monitor.py --quiet`

#### Balanced Mode
- **Use Case**: Normal operation
- **Fan Speed**: 40-60% (temperature dependent)
- **Pump Speed**: 60-70%
- **Command**: `python scripts/water_cooling_monitor.py --auto`

#### Performance Mode
- **Use Case**: Heavy workloads, maximum cooling
- **Fan Speed**: 80%
- **Pump Speed**: 90%
- **Command**: `python scripts/water_cooling_monitor.py --performance`

## Maintenance

### Regular Checks
1. **Weekly**: Check water temperature trends
2. **Monthly**: Test all fans and pump
3. **Quarterly**: Clean radiator and check for dust
4. **Annually**: Consider coolant replacement

### Monitoring Alerts
- **Water Temp > 50°C**: Warning threshold
- **Water Temp > 60°C**: Critical threshold
- **Pump Speed = 0**: Pump failure
- **Fan Speed = 0**: Fan failure

### Logging
The monitoring scripts can be configured to log to:
- System logs: `/var/log/syslog`
- Application logs: `logs/water_cooling.log`
- JSON output for external monitoring

## Hardware Specifications

### Corsair Commander ST
- **Firmware**: 2.0.19
- **USB Interface**: HID
- **Fan Ports**: 6x PWM
- **RGB Ports**: 6x ARGB
- **Temperature Sensors**: 2x
- **Power**: USB powered

### Supported Devices
- Corsair H100i Elite Capellix
- Corsair H115i Elite Capellix
- Corsair H150i Elite Capellix
- Corsair Commander Core
- Corsair Commander Pro
- Corsair Commander XT

## Future Enhancements

### Planned Features
1. **Web Dashboard**: Real-time monitoring interface
2. **Alert System**: Email/SMS notifications
3. **Historical Data**: Temperature and performance logging
4. **Integration**: Direct integration with Living Truth Engine dashboard
5. **Predictive Cooling**: AI-based temperature prediction

### Customization Options
1. **Custom Fan Curves**: User-defined temperature/speed relationships
2. **Profile Switching**: Automatic profile selection based on workload
3. **External Sensors**: Integration with additional temperature sensors
4. **Network Control**: Remote monitoring and control capabilities
