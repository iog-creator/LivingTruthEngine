#!/usr/bin/env python3
"""
Unified System Cooling Monitor
Combines CPU temperature and water cooling monitoring for the Living Truth Engine.
"""

import os
import time
import subprocess
import json
import argparse
from datetime import datetime
from typing import Dict, Any, Optional

class SystemCoolingMonitor:
    def __init__(self):
        self.cpu_monitor = None
        self.water_monitor = None
        self.critical_cpu_temp = 80.0
        self.critical_water_temp = 60.0
        
    def get_cpu_temps(self) -> Dict[str, Any]:
        """Get CPU temperatures"""
        try:
            temps = {}
            temp_paths = [
                "/sys/class/thermal/thermal_zone0/temp",
                "/sys/class/thermal/thermal_zone1/temp", 
                "/sys/class/thermal/thermal_zone2/temp"
            ]
            
            for i, path in enumerate(temp_paths):
                try:
                    with open(path, 'r') as f:
                        temp_c = int(f.read().strip()) / 1000.0
                        temps[f"thermal_zone_{i}"] = temp_c
                except Exception as e:
                    temps[f"thermal_zone_{i}"] = f"Error: {e}"
            return temps
        except Exception as e:
            return {"error": f"CPU temp error: {e}"}
    
    def get_water_cooling_status(self) -> Dict[str, Any]:
        """Get water cooling status"""
        try:
            result = subprocess.run(['liquidctl', 'status', '--json'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return {"error": f"Water cooling error: {result.stderr}"}
        except Exception as e:
            return {"error": f"Water cooling exception: {e}"}
    
    def get_system_load(self) -> Dict[str, Any]:
        """Get system load"""
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
    
    def get_docker_stats(self) -> Dict[str, Any]:
        """Get Docker container stats"""
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
    
    def analyze_cooling_status(self, cpu_temps: Dict, water_status: Dict) -> Dict[str, Any]:
        """Analyze overall cooling status and provide recommendations"""
        analysis = {
            "status": "NORMAL",
            "recommendations": [],
            "alerts": []
        }
        
        # Analyze CPU temperatures
        if "error" not in cpu_temps:
            max_cpu_temp = 0
            for zone, temp in cpu_temps.items():
                if isinstance(temp, (int, float)):
                    max_cpu_temp = max(max_cpu_temp, temp)
            
            if max_cpu_temp > self.critical_cpu_temp:
                analysis["status"] = "CRITICAL"
                analysis["alerts"].append(f"CPU temperature critical: {max_cpu_temp}°C")
                analysis["recommendations"].append("Immediate action required - reduce system load")
            elif max_cpu_temp > 70:
                analysis["status"] = "WARNING"
                analysis["alerts"].append(f"CPU temperature high: {max_cpu_temp}°C")
                analysis["recommendations"].append("Consider increasing cooling or reducing load")
        
        # Analyze water cooling
        if "error" not in water_status and isinstance(water_status, list) and len(water_status) > 0:
            device_data = water_status[0]
            status_items = device_data.get("status", [])
            
            water_temp = None
            pump_speed = None
            
            for item in status_items:
                key = item.get("key", "")
                value = item.get("value", 0)
                
                if "Water temperature" in key:
                    water_temp = value
                elif "Pump speed" in key:
                    pump_speed = value
            
            if water_temp is not None:
                if water_temp > self.critical_water_temp:
                    analysis["status"] = "CRITICAL"
                    analysis["alerts"].append(f"Water temperature critical: {water_temp}°C")
                    analysis["recommendations"].append("Check water cooling system immediately")
                elif water_temp > 50:
                    analysis["status"] = "WARNING" if analysis["status"] == "NORMAL" else analysis["status"]
                    analysis["alerts"].append(f"Water temperature elevated: {water_temp}°C")
                    analysis["recommendations"].append("Monitor water cooling performance")
            
            if pump_speed is not None and pump_speed == 0:
                analysis["status"] = "CRITICAL"
                analysis["alerts"].append("Pump not running!")
                analysis["recommendations"].append("Check pump connection and power")
        
        return analysis
    
    def monitor_once(self) -> Dict[str, Any]:
        """Perform one complete monitoring cycle"""
        timestamp = datetime.now().isoformat()
        
        # Gather all data
        cpu_temps = self.get_cpu_temps()
        water_status = self.get_water_cooling_status()
        system_load = self.get_system_load()
        docker_stats = self.get_docker_stats()
        
        # Analyze cooling status
        cooling_analysis = self.analyze_cooling_status(cpu_temps, water_status)
        
        data = {
            "timestamp": timestamp,
            "cpu_temperatures": cpu_temps,
            "water_cooling": water_status,
            "system_load": system_load,
            "docker_stats": docker_stats,
            "cooling_analysis": cooling_analysis
        }
        
        return data
    
    def monitor_continuous(self, interval: int = 30, max_cycles: Optional[int] = None):
        """Monitor continuously"""
        cycle = 0
        
        print(f"🔄 Starting Unified System Cooling Monitor (interval: {interval}s)")
        print("=" * 70)
        
        while max_cycles is None or cycle < max_cycles:
            data = self.monitor_once()
            
            # Print summary
            print(f"\n[{data['timestamp']}]")
            print(f"📊 Status: {data['cooling_analysis']['status']}")
            
            # CPU temperatures
            if "error" not in data['cpu_temperatures']:
                max_temp = max([temp for temp in data['cpu_temperatures'].values() 
                              if isinstance(temp, (int, float))], default=0)
                print(f"🔥 CPU Max: {max_temp}°C")
            
            # Water cooling
            if "error" not in data['water_cooling'] and isinstance(data['water_cooling'], list):
                device_data = data['water_cooling'][0]
                status_items = device_data.get("status", [])
                
                for item in status_items:
                    key = item.get("key", "")
                    value = item.get("value", 0)
                    
                    if "Water temperature" in key:
                        print(f"💧 Water: {value}°C")
                    elif "Pump speed" in key:
                        print(f"🔧 Pump: {value} RPM")
            
            # System load
            if "error" not in data['system_load']:
                load = data['system_load']
                print(f"⚡ Load: {load['1min']:.2f} (1m), {load['5min']:.2f} (5m), {load['15min']:.2f} (15m)")
            
            # Alerts and recommendations
            if data['cooling_analysis']['alerts']:
                print("⚠️  Alerts:")
                for alert in data['cooling_analysis']['alerts']:
                    print(f"   • {alert}")
            
            if data['cooling_analysis']['recommendations']:
                print("💡 Recommendations:")
                for rec in data['cooling_analysis']['recommendations']:
                    print(f"   • {rec}")
            
            cycle += 1
            if max_cycles is None or cycle < max_cycles:
                time.sleep(interval)
    
    def generate_report(self) -> str:
        """Generate a comprehensive cooling report"""
        data = self.monitor_once()
        
        report = f"""
=== SYSTEM COOLING REPORT ===
Generated: {data['timestamp']}
Overall Status: {data['cooling_analysis']['status']}

CPU TEMPERATURES:
"""
        
        if "error" not in data['cpu_temperatures']:
            for zone, temp in data['cpu_temperatures'].items():
                report += f"  {zone}: {temp}°C\n"
        else:
            report += f"  Error: {data['cpu_temperatures']['error']}\n"
        
        report += "\nWATER COOLING:\n"
        if "error" not in data['water_cooling'] and isinstance(data['water_cooling'], list):
            device_data = data['water_cooling'][0]
            status_items = device_data.get("status", [])
            
            for item in status_items:
                key = item.get("key", "")
                value = item.get("value", 0)
                unit = item.get("unit", "")
                report += f"  {key}: {value}{unit}\n"
        else:
            report += f"  Error: {data['water_cooling'].get('error', 'Unknown error')}\n"
        
        report += f"\nSYSTEM LOAD:\n"
        if "error" not in data['system_load']:
            load = data['system_load']
            report += f"  1min: {load['1min']:.2f}\n"
            report += f"  5min: {load['5min']:.2f}\n"
            report += f"  15min: {load['15min']:.2f}\n"
        else:
            report += f"  Error: {data['system_load']['error']}\n"
        
        if data['cooling_analysis']['alerts']:
            report += "\nALERTS:\n"
            for alert in data['cooling_analysis']['alerts']:
                report += f"  • {alert}\n"
        
        if data['cooling_analysis']['recommendations']:
            report += "\nRECOMMENDATIONS:\n"
            for rec in data['cooling_analysis']['recommendations']:
                report += f"  • {rec}\n"
        
        return report

def main():
    monitor = SystemCoolingMonitor()
    
    parser = argparse.ArgumentParser(description="Unified system cooling monitor")
    parser.add_argument("--once", action="store_true", help="Monitor once and exit")
    parser.add_argument("--interval", type=int, default=30, help="Monitoring interval in seconds")
    parser.add_argument("--cycles", type=int, help="Number of monitoring cycles (default: continuous)")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument("--report", action="store_true", help="Generate comprehensive report")
    
    args = parser.parse_args()
    
    if args.report:
        report = monitor.generate_report()
        print(report)
    elif args.once:
        data = monitor.monitor_once()
        if args.json:
            print(json.dumps(data, indent=2))
        else:
            # Print summary
            print(f"Status: {data['cooling_analysis']['status']}")
            if "error" not in data['cpu_temperatures']:
                max_temp = max([temp for temp in data['cpu_temperatures'].values() 
                              if isinstance(temp, (int, float))], default=0)
                print(f"CPU Max: {max_temp}°C")
            
            if "error" not in data['water_cooling'] and isinstance(data['water_cooling'], list):
                device_data = data['water_cooling'][0]
                status_items = device_data.get("status", [])
                for item in status_items:
                    key = item.get("key", "")
                    value = item.get("value", 0)
                    if "Water temperature" in key:
                        print(f"Water: {value}°C")
                        break
    else:
        monitor.monitor_continuous(args.interval, args.cycles)

if __name__ == "__main__":
    main()
