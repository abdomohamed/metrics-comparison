#!/usr/bin/env python3
"""
Demo script for the Metrics Comparison Tool
"""

import subprocess
import sys
import time
from pathlib import Path

def run_demo():
    print("🎬 Metrics Comparison Tool Demo")
    print("=" * 50)
    
    # Check if files exist
    if not Path("aggregate_metrics.json").exists():
        print("❌ aggregate_metrics.json not found!")
        return
    
    if not Path("aggregate_metrics_new.json").exists():
        print("❌ aggregate_metrics_new.json not found!")
        return
    
    demos = [
        {
            "title": "📊 Basic Table Comparison",
            "command": ["python", "metrics_comparator.py", "aggregate_metrics.json", "aggregate_metrics_new.json"],
            "description": "Standard table view showing all changes"
        },
        {
            "title": "🌳 Tree View Comparison", 
            "command": ["python", "metrics_comparator.py", "-f", "tree", "aggregate_metrics.json", "aggregate_metrics_new.json"],
            "description": "Hierarchical tree view grouped by metrics"
        },
        {
            "title": "📋 Complete View (with unchanged)",
            "command": ["python", "metrics_comparator.py", "-u", "aggregate_metrics.json", "aggregate_metrics_new.json"],
            "description": "Table view including unchanged values"
        }
    ]
    
    for i, demo in enumerate(demos, 1):
        print(f"\n{i}. {demo['title']}")
        print(f"   {demo['description']}")
        print(f"   Command: {' '.join(demo['command'])}")
        
        response = input("\n   Press Enter to run this demo (or 's' to skip): ").strip().lower()
        
        if response == 's':
            print("   ⏭️  Skipped")
            continue
        
        print("\n" + "─" * 80)
        try:
            subprocess.run(demo['command'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Error running demo: {e}")
        except KeyboardInterrupt:
            print("\n⏹️  Demo interrupted")
            break
        
        print("─" * 80)
        
        if i < len(demos):
            input("\nPress Enter to continue to next demo...")
    
    print("\n🎉 Demo completed!")
    print("\nTo run comparisons manually:")
    print("python metrics_comparator.py --help")

if __name__ == "__main__":
    run_demo()
