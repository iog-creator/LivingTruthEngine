#!/usr/bin/env python3
"""
Water Cooling Monitoring and Control Script
Monitors and controls Corsair water cooling systems for the Living Truth Engine.
"""

import os
import time
import subprocess
import json
import argparse
from datetime import datetime
from typing import Dict, Any, Optional

class WaterCoolingMonitor:
    def __init__(self):
        self.device_name = "Corsair Commander ST"
        self.critical_temp = 60.0  # Critical water temperature
        self.warning_temp = 50.0   # Warning water temperature
        self.optimal_temp = 40.0   # Optimal water temperature
        
    def get_device_status(self) -> Dict[str, Any]:
        """Get current status of the water cooling device"""
        try:
            result = subprocess.run(['liquidctl', 'status', '--json'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return {"error": f"Failed to get status: {result.stderr}"}
        except Exception as e:
            return {"error": f"Exception getting status: {e}"}
    
    def get_device_info(self) -> Dict[str, Any]:
        """Get device information"""
        try:
            result = subprocess.run(['liquidctl', 'initialize', '--json'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return {"error": f"Failed to get device info: {result.stderr}"}
        except Exception as e:
            return {"error": f"Exception getting device info: {e}"}
    
    def set_fan_speed(self, fan_port: int, speed_percentage: int) -> bool:
        """Set fan speed for a specific port"""
        if not 0 <= speed_percentage <= 100:
            print(f"❌ Speed must be between 0 and 100, got {speed_percentage}")
            return False
            
        try:
            cmd = ['liquidctl', 'set', f'fan{fan_port}', 'speed', str(speed_percentage)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Fan {fan_port} speed set to {speed_percentage}%")
                return True
            else:
                print(f"❌ Failed to set fan {fan_port} speed: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Exception setting fan speed: {e}")
            return False
    
    def set_pump_speed(self, speed_percentage: int) -> bool:
        """Set pump speed"""
        if not 0 <= speed_percentage <= 100:
            print(f"❌ Speed must be between 0 and 100, got {speed_percentage}")
            return False
            
        try:
            cmd = ['liquidctl', 'set', 'pump', 'speed', str(speed_percentage)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Pump speed set to {speed_percentage}%")
                return True
            else:
                print(f"❌ Failed to set pump speed: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Exception setting pump speed: {e}")
            return False
    
    def set_temperature_based_fan_curve(self, water_temp: float) -> Dict[str, Any]:
        """Set fan speeds based on water temperature"""
        actions = {}
        
        # Fan curve logic
        if water_temp > self.critical_temp:
            # Critical temperature - max fan speed
            for fan in range(1, 7):
                if self.set_fan_speed(fan, 100):
                    actions[f"fan_{fan}"] = 100
            if self.set_pump_speed(100):
                actions["pump"] = 100
            actions["status"] = "CRITICAL"
            
        elif water_temp > self.warning_temp:
            # Warning temperature - high fan speed
            for fan in range(1, 7):
                if self.set_fan_speed(fan, 80):
                    actions[f"fan_{fan}"] = 80
            if self.set_pump_speed(80):
                actions["pump"] = 80
            actions["status"] = "WARNING"
            
        elif water_temp > self.optimal_temp:
            # Elevated temperature - moderate fan speed
            for fan in range(1, 7):
                if self.set_fan_speed(fan, 60):
                    actions[f"fan_{fan}"] = 60
            if self.set_pump_speed(70):
                actions["pump"] = 70
            actions["status"] = "ELEVATED"
            
        else:
            # Normal temperature - low fan speed
            for fan in range(1, 7):
                if self.set_fan_speed(fan, 40):
                    actions[f"fan_{fan}"] = 40
            if self.set_pump_speed(60):
                actions["pump"] = 60
            actions["status"] = "NORMAL"
        
        return actions
    
    def monitor_once(self) -> Dict[str, Any]:
        """Perform one monitoring cycle"""
        timestamp = datetime.now().isoformat()
        
        # Get device status
        status = self.get_device_status()
        device_info = self.get_device_info()
        
        data = {
            "timestamp": timestamp,
            "device_info": device_info,
            "status": status
        }
        
        # Extract key metrics
        if "error" not in status:
            try:
                # Parse status data - liquidctl returns a list
                if isinstance(status, list) and len(status) > 0:
                    device_data = status[0]
                    status_items = device_data.get("status", [])
                    metrics = {}
                    
                    for item in status_items:
                        key = item.get("key", "")
                        value = item.get("value", 0)
                        
                        if "Pump speed" in key:
                            metrics["pump_speed"] = value
                        elif "Water temperature" in key:
                            metrics["water_temp"] = value
                        elif "Fan speed" in key:
                            # Extract fan number from key like "Fan speed 1"
                            fan_num = key.split()[-1]
                            metrics[f"fan_{fan_num}_speed"] = value
                
                data["metrics"] = metrics
                
                # Check for temperature alerts
                if "water_temp" in metrics:
                    water_temp = metrics["water_temp"]
                    if water_temp > self.critical_temp:
                        data["alert"] = f"CRITICAL: Water temperature {water_temp}°C"
                    elif water_temp > self.warning_temp:
                        data["alert"] = f"WARNING: Water temperature {water_temp}°C"
                    elif water_temp > self.optimal_temp:
                        data["alert"] = f"ELEVATED: Water temperature {water_temp}°C"
                    else:
                        data["alert"] = f"Normal: Water temperature {water_temp}°C"
                        
            except Exception as e:
                data["error"] = f"Error parsing status: {e}"
        
        return data
    
    def monitor_continuous(self, interval: int = 30, auto_control: bool = False, 
                          max_cycles: Optional[int] = None):
        """Monitor continuously with optional automatic control"""
        cycle = 0
        
        print(f"🔄 Starting Water Cooling Monitoring (interval: {interval}s)")
        if auto_control:
            print("🤖 Automatic fan control enabled")
        print("=" * 60)
        
        while max_cycles is None or cycle < max_cycles:
            data = self.monitor_once()
            
            # Print summary
            print(f"\n[{data['timestamp']}]")
            
            if "error" in data:
                print(f"❌ Error: {data['error']}")
            else:
                metrics = data.get("metrics", {})
                alert = data.get("alert", "No alert")
                
                print(f"💧 Water Temp: {metrics.get('water_temp', 'N/A')}°C")
                print(f"🔧 Pump Speed: {metrics.get('pump_speed', 'N/A')} RPM")
                print(f"⚠️  Alert: {alert}")
                
                # Show fan speeds
                fan_speeds = []
                for i in range(1, 7):
                    speed = metrics.get(f'fan_{i}_speed', 0)
                    fan_speeds.append(f"F{i}:{speed}")
                print(f"🌪️  Fans: {' '.join(fan_speeds)}")
                
                # Auto control if enabled
                if auto_control and "water_temp" in metrics:
                    water_temp = metrics["water_temp"]
                    actions = self.set_temperature_based_fan_curve(water_temp)
                    print(f"🤖 Auto Control: {actions.get('status', 'Unknown')}")
            
            cycle += 1
            if max_cycles is None or cycle < max_cycles:
                time.sleep(interval)
    
    def test_all_fans(self):
        """Test all connected fans"""
        print("🧪 Testing all fans...")
        
        # Test each fan port
        for fan in range(1, 7):
            print(f"Testing Fan {fan}...")
            
            # Set to 50% for 3 seconds
            if self.set_fan_speed(fan, 50):
                time.sleep(3)
                # Set back to 0%
                self.set_fan_speed(fan, 0)
            else:
                print(f"Fan {fan} not responding")
        
        print("✅ Fan test complete")
    
    def set_quiet_mode(self):
        """Set quiet mode - low speeds"""
        print("🔇 Setting quiet mode...")
        for fan in range(1, 7):
            self.set_fan_speed(fan, 30)
        self.set_pump_speed(50)
        print("✅ Quiet mode activated")
    
    def set_performance_mode(self):
        """Set performance mode - high speeds"""
        print("🏃 Setting performance mode...")
        for fan in range(1, 7):
            self.set_fan_speed(fan, 80)
        self.set_pump_speed(90)
        print("✅ Performance mode activated")

def main():
    monitor = WaterCoolingMonitor()
    
    parser = argparse.ArgumentParser(description="Monitor and control Corsair water cooling")
    parser.add_argument("--once", action="store_true", help="Monitor once and exit")
    parser.add_argument("--interval", type=int, default=30, help="Monitoring interval in seconds")
    parser.add_argument("--cycles", type=int, help="Number of monitoring cycles (default: continuous)")
    parser.add_argument("--auto", action="store_true", help="Enable automatic fan control")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument("--test-fans", action="store_true", help="Test all fans")
    parser.add_argument("--quiet", action="store_true", help="Set quiet mode")
    parser.add_argument("--performance", action="store_true", help="Set performance mode")
    parser.add_argument("--set-fan", nargs=2, metavar=("FAN", "SPEED"), 
                       help="Set specific fan speed (fan_number speed_percentage)")
    parser.add_argument("--set-pump", type=int, help="Set pump speed (percentage)")
    
    args = parser.parse_args()
    
    if args.test_fans:
        monitor.test_all_fans()
    elif args.quiet:
        monitor.set_quiet_mode()
    elif args.performance:
        monitor.set_performance_mode()
    elif args.set_fan:
        fan_num = int(args.set_fan[0])
        speed = int(args.set_fan[1])
        monitor.set_fan_speed(fan_num, speed)
    elif args.set_pump:
        monitor.set_pump_speed(args.set_pump)
    elif args.once:
        data = monitor.monitor_once()
        if args.json:
            print(json.dumps(data, indent=2))
        else:
            if "error" in data:
                print(f"Error: {data['error']}")
            else:
                metrics = data.get("metrics", {})
                print(f"Water Temp: {metrics.get('water_temp', 'N/A')}°C")
                print(f"Pump Speed: {metrics.get('pump_speed', 'N/A')} RPM")
                print(f"Alert: {data.get('alert', 'No alert')}")
    else:
        monitor.monitor_continuous(args.interval, args.auto, args.cycles)

if __name__ == "__main__":
    main()
