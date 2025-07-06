#!/usr/bin/env python3
"""
Simple script to run the Text-to-SQL Agent UI
"""

import subprocess
import sys
import os

def main():
    """Run the Streamlit UI"""
    try:
        # Check if streamlit is installed
        import streamlit
        print("🚀 Starting Text-to-SQL Agent UI...")
        print("📱 The UI will open in your default web browser")
        print("🔗 If it doesn't open automatically, go to: http://localhost:8501")
        print("⏹️  Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
        
    except ImportError:
        print("❌ Streamlit is not installed. Please install it first:")
        print("pip install streamlit")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 UI stopped by user")
    except Exception as e:
        print(f"❌ Error running UI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 