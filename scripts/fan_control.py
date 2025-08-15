#!/usr/bin/env python3
"""
CPU Fan Control Script
Controls CPU fan speed for the Living Truth Engine system.
"""

import os
import sys
import argparse
import time

class FanController:
    def __init__(self):
        self.pwm_path = "/sys/devices/platform/INTC1085:00/pwm/pwmchip0/pwm0"
        
    def enable_fan(self):
        """Enable the fan"""
        try:
            with open(f"{self.pwm_path}/enable", 'w') as f:
                f.write("1")
            print("✅ Fan enabled")
            return True
        except Exception as e:
            print(f"❌ Error enabling fan: {e}")
            return False
    
    def disable_fan(self):
        """Disable the fan"""
        try:
            with open(f"{self.pwm_path}/enable", 'w') as f:
                f.write("0")
            print("✅ Fan disabled")
            return True
        except Exception as e:
            print(f"❌ Error disabling fan: {e}")
            return False
    
    def set_fan_speed(self, percentage):
        """Set fan speed as percentage (0-100)"""
        if not 0 <= percentage <= 100:
            print("❌ Percentage must be between 0 and 100")
            return False
            
        try:
            # Get current period
            with open(f"{self.pwm_path}/period", 'r') as f:
                period = int(f.read().strip())
            
            # Calculate duty cycle
            duty_cycle = int((percentage / 100.0) * period)
            
            # Set duty cycle
            with open(f"{self.pwm_path}/duty_cycle", 'w') as f:
                f.write(str(duty_cycle))
            
            print(f"✅ Fan speed set to {percentage}%")
            return True
        except Exception as e:
            print(f"❌ Error setting fan speed: {e}")
            return False
    
    def get_fan_status(self):
        """Get current fan status"""
        try:
            with open(f"{self.pwm_path}/enable", 'r') as f:
                enabled = int(f.read().strip()) == 1
            with open(f"{self.pwm_path}/duty_cycle", 'r') as f:
                duty_cycle = int(f.read().strip())
            with open(f"{self.pwm_path}/period", 'r') as f:
                period = int(f.read().strip())
            
            percentage = (duty_cycle / period) * 100 if period > 0 else 0
            
            return {
                "enabled": enabled,
                "duty_cycle": duty_cycle,
                "period": period,
                "percentage": round(percentage, 1)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def auto_fan_control(self, temp_threshold=70, check_interval=30):
        """Automatically control fan based on temperature"""
        print(f"🔄 Starting auto fan control (threshold: {temp_threshold}°C, interval: {check_interval}s)")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                # Get temperature
                with open("/sys/class/thermal/thermal_zone1/temp", 'r') as f:
                    temp = int(f.read().strip()) / 1000.0
                
                # Get current fan status
                status = self.get_fan_status()
                
                print(f"\n[{time.strftime('%H:%M:%S')}] Temp: {temp}°C, Fan: {status.get('percentage', 0)}%")
                
                if temp > temp_threshold:
                    if not status.get('enabled', False):
                        self.enable_fan()
                    
                    # Calculate fan speed based on temperature
                    if temp > 80:
                        speed = 100
                    elif temp > 75:
                        speed = 80
                    elif temp > 70:
                        speed = 60
                    else:
                        speed = 40
                    
                    self.set_fan_speed(speed)
                    print(f"🔥 High temperature detected! Setting fan to {speed}%")
                else:
                    if status.get('enabled', False) and status.get('percentage', 0) > 0:
                        self.set_fan_speed(20)  # Low speed for normal temps
                        print("❄️  Normal temperature, reducing fan speed")
                
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Auto fan control stopped")

def main():
    controller = FanController()
    
    parser = argparse.ArgumentParser(description="Control CPU fan speed")
    parser.add_argument("--enable", action="store_true", help="Enable fan")
    parser.add_argument("--disable", action="store_true", help="Disable fan")
    parser.add_argument("--speed", type=int, help="Set fan speed (0-100%)")
    parser.add_argument("--status", action="store_true", help="Show current fan status")
    parser.add_argument("--auto", action="store_true", help="Enable automatic fan control")
    parser.add_argument("--threshold", type=int, default=70, help="Temperature threshold for auto control (°C)")
    parser.add_argument("--interval", type=int, default=30, help="Check interval for auto control (seconds)")
    
    args = parser.parse_args()
    
    if args.status:
        status = controller.get_fan_status()
        print(f"Fan Status: {status}")
        return
    
    if args.enable:
        controller.enable_fan()
    elif args.disable:
        controller.disable_fan()
    elif args.speed is not None:
        controller.set_fan_speed(args.speed)
    elif args.auto:
        controller.auto_fan_control(args.threshold, args.interval)
    else:
        print("No action specified. Use --help for options.")
        status = controller.get_fan_status()
        print(f"Current fan status: {status}")

if __name__ == "__main__":
    main()
