# CPU Fan Monitoring and Control Tools

This directory contains tools to monitor and control CPU temperature and fan operation for the Living Truth Engine system.

## Current System Status

Based on the latest monitoring:

- **CPU Package Temperature**: 73.0°C (elevated but not critical)
- **Core Temperatures**: 48-73°C (normal to elevated range)
- **Fan Status**: Currently disabled (PWM control available)
- **System Load**: Moderate (1.61, 1.26, 1.49)

## Available Tools

### 1. `monitor_fans.py` - Temperature and Fan Monitoring

**Usage:**
```bash
# Monitor once and exit
python scripts/monitor_fans.py --once

# Monitor continuously (default 30s interval)
python scripts/monitor_fans.py

# Monitor with custom interval
python scripts/monitor_fans.py --interval 60

# Monitor for specific number of cycles
python scripts/monitor_fans.py --cycles 10

# Output in JSON format
python scripts/monitor_fans.py --once --json
```

**Features:**
- Real-time CPU temperature monitoring
- Fan PWM status and speed percentage
- System load monitoring
- Docker container resource usage
- High temperature warnings (>70°C)

### 2. `fan_control.py` - Fan Speed Control

**Usage:**
```bash
# Check current fan status
python scripts/fan_control.py --status

# Enable fan
python scripts/fan_control.py --enable

# Disable fan
python scripts/fan_control.py --disable

# Set specific fan speed (0-100%)
python scripts/fan_control.py --speed 50

# Enable automatic fan control
python scripts/fan_control.py --auto

# Auto control with custom threshold
python scripts/fan_control.py --auto --threshold 75

# Auto control with custom check interval
python scripts/fan_control.py --auto --interval 60
```

**Features:**
- Manual fan speed control (0-100%)
- Automatic temperature-based control
- Configurable temperature thresholds
- Real-time monitoring with automatic adjustments

### 3. `sensors` - System-wide Sensor Information

**Usage:**
```bash
# Display all sensor information
sensors

# Monitor specific sensors
watch -n 2 sensors
```

**Features:**
- CPU core temperatures
- Package temperature
- NVMe drive temperatures
- Network interface temperatures
- Memory module temperatures

### 4. `psensor` - Graphical Monitoring Tool

**Usage:**
```bash
# Launch graphical sensor monitor
psensor
```

**Features:**
- Real-time temperature graphs
- Fan speed monitoring
- System resource usage
- Configurable alerts

## Temperature Guidelines

| Temperature | Status | Action |
|-------------|--------|--------|
| < 60°C | Normal | No action needed |
| 60-70°C | Elevated | Monitor closely |
| 70-80°C | High | Consider increasing fan speed |
| 80-90°C | Very High | Increase fan speed immediately |
| > 90°C | Critical | Emergency cooling required |

## Recommended Usage

### For Normal Operation:
```bash
# Monitor temperatures every 30 seconds
python scripts/monitor_fans.py --interval 30
```

### For High Load Situations:
```bash
# Enable automatic fan control with 70°C threshold
python scripts/fan_control.py --auto --threshold 70 --interval 30
```

### For Troubleshooting:
```bash
# Get detailed system information
sensors
python scripts/monitor_fans.py --once --json
python scripts/fan_control.py --status
```

## System Information

- **CPU**: Intel Core i9-13900K
- **Motherboard**: MSI MEG Z790 GODLIKE
- **Fan Control**: PWM via `/sys/devices/platform/INTC1085:00/pwm/pwmchip0/pwm0`
- **Thermal Zones**: 3 zones monitored
- **Critical Temperature**: 100°C (CPU package)

## Troubleshooting

### Fan Not Responding:
1. Check if PWM control is available: `ls /sys/devices/platform/INTC1085:00/pwm/pwmchip0/`
2. Verify fan is enabled: `cat /sys/devices/platform/INTC1085:00/pwm/pwmchip0/pwm0/enable`
3. Check fan speed: `cat /sys/devices/platform/INTC1085:00/pwm/pwmchip0/pwm0/duty_cycle`

### High Temperatures:
1. Check system load: `top` or `htop`
2. Monitor Docker containers: `docker stats`
3. Verify airflow and cooling
4. Consider reducing system load

### Tools Not Working:
1. Ensure `lm-sensors` is installed: `sudo apt install lm-sensors`
2. Run sensor detection: `sudo sensors-detect --auto`
3. Check permissions for PWM access (may need sudo)

## Integration with Living Truth Engine

These tools are designed to work alongside the Living Truth Engine's Docker containers. The monitoring scripts include Docker container resource usage to help identify which services might be contributing to high temperatures.

For automated integration, consider:
- Running `monitor_fans.py` as a background service
- Using `fan_control.py --auto` during heavy workloads
- Setting up alerts for temperature thresholds
- Monitoring Docker container resource usage patterns
