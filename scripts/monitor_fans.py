#!/usr/bin/env python3
"""
CPU Temperature and Fan Monitoring Script
Monitors CPU temperature and fan status for the Living Truth Engine system.
"""

import os
import time
import subprocess
import json
from datetime import datetime

class FanMonitor:
    def __init__(self):
        self.pwm_path = "/sys/devices/platform/INTC1085:00/pwm/pwmchip0/pwm0"
        self.temp_paths = [
            "/sys/class/thermal/thermal_zone0/temp",
            "/sys/class/thermal/thermal_zone1/temp", 
            "/sys/class/thermal/thermal_zone2/temp"
        ]
        
    def get_cpu_temps(self):
        """Get CPU temperatures from thermal zones"""
        temps = {}
        for i, path in enumerate(self.temp_paths):
            try:
                with open(path, 'r') as f:
                    temp_c = int(f.read().strip()) / 1000.0
                    temps[f"thermal_zone_{i}"] = temp_c
            except Exception as e:
                temps[f"thermal_zone_{i}"] = f"Error: {e}"
        return temps
    
    def get_fan_status(self):
        """Get current fan PWM status"""
        try:
            with open(f"{self.pwm_path}/enable", 'r') as f:
                enabled = int(f.read().strip()) == 1
            with open(f"{self.pwm_path}/duty_cycle", 'r') as f:
                duty_cycle = int(f.read().strip())
            with open(f"{self.pwm_path}/period", 'r') as f:
                period = int(f.read().strip())
            
            # Calculate percentage
            percentage = (duty_cycle / period) * 100 if period > 0 else 0
            
            return {
                "enabled": enabled,
                "duty_cycle": duty_cycle,
                "period": period,
                "percentage": round(percentage, 1)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_detailed_sensors(self):
        """Get detailed sensor information using sensors command"""
        try:
            result = subprocess.run(['sensors'], capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return f"Error running sensors: {e}"
    
    def get_system_load(self):
        """Get system load information"""
        try:
            with open('/proc/loadavg', 'r') as f:
                load = f.read().strip().split()
            return {
                "1min": float(load[0]),
                "5min": float(load[1]), 
                "15min": float(load[2])
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_docker_stats(self):
        """Get Docker container resource usage"""
        try:
            result = subprocess.run(['docker', 'stats', '--no-stream', '--format', 'json'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                containers = []
                for line in result.stdout.strip().split('\n'):
                    if line:
                        containers.append(json.loads(line))
                return containers
            else:
                return {"error": "Docker not running or no containers"}
        except Exception as e:
            return {"error": str(e)}
    
    def monitor_once(self):
        """Perform one monitoring cycle"""
        timestamp = datetime.now().isoformat()
        
        data = {
            "timestamp": timestamp,
            "cpu_temperatures": self.get_cpu_temps(),
            "fan_status": self.get_fan_status(),
            "system_load": self.get_system_load(),
            "docker_stats": self.get_docker_stats()
        }
        
        return data
    
    def monitor_continuous(self, interval=30, max_cycles=None):
        """Monitor continuously with specified interval"""
        cycle = 0
        
        print(f"Starting CPU and Fan Monitoring (interval: {interval}s)")
        print("=" * 60)
        
        while max_cycles is None or cycle < max_cycles:
            data = self.monitor_once()
            
            # Print summary
            print(f"\n[{data['timestamp']}]")
            print(f"CPU Temps: {data['cpu_temperatures']}")
            print(f"Fan: {'ON' if data['fan_status'].get('enabled', False) else 'OFF'} "
                  f"({data['fan_status'].get('percentage', 0)}%)")
            print(f"Load: {data['system_load']}")
            
            # Check for high temperatures
            for zone, temp in data['cpu_temperatures'].items():
                if isinstance(temp, (int, float)) and temp > 70:
                    print(f"⚠️  WARNING: {zone} at {temp}°C (high temperature)")
            
            cycle += 1
            if max_cycles is None or cycle < max_cycles:
                time.sleep(interval)

def main():
    monitor = FanMonitor()
    
    import argparse
    parser = argparse.ArgumentParser(description="Monitor CPU temperature and fan status")
    parser.add_argument("--once", action="store_true", help="Monitor once and exit")
    parser.add_argument("--interval", type=int, default=30, help="Monitoring interval in seconds")
    parser.add_argument("--cycles", type=int, help="Number of monitoring cycles (default: continuous)")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    
    args = parser.parse_args()
    
    if args.once:
        data = monitor.monitor_once()
        if args.json:
            print(json.dumps(data, indent=2))
        else:
            print(f"CPU Temps: {data['cpu_temperatures']}")
            print(f"Fan Status: {data['fan_status']}")
            print(f"System Load: {data['system_load']}")
    else:
        monitor.monitor_continuous(args.interval, args.cycles)

if __name__ == "__main__":
    main()
