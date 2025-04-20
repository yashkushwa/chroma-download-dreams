
#!/usr/bin/env python3
import os
import sys
import subprocess
import platform
import webbrowser
from pathlib import Path

def check_dependency(name, install_cmd=None):
    """Check if a command-line dependency is installed."""
    try:
        subprocess.run([name, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        return True
    except FileNotFoundError:
        if install_cmd:
            print(f"⚠️ {name} is not installed. Install command: {install_cmd}")
        else:
            print(f"⚠️ {name} is not installed.")
        return False

def check_python_package(package):
    """Check if a Python package is installed."""
    try:
        __import__(package)
        return True
    except ImportError:
        return False

def install_python_package(package):
    """Install a Python package using pip."""
    print(f"📦 Installing {package}...")
    subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)

def main():
    print("\n" + "=" * 60)
    print("🚀 Chroma Video Downloader - Setup & Launch")
    print("=" * 60)
    
    # Check Python version
    py_version = sys.version_info
    if py_version.major < 3 or (py_version.major == 3 and py_version.minor < 7):
        print("❌ Python 3.7 or higher is required.")
        sys.exit(1)
    else:
        print(f"✅ Python version: {py_version.major}.{py_version.minor}.{py_version.micro}")
    
    # Create downloads directory if it doesn't exist
    downloads_dir = Path("downloads")
    if not downloads_dir.exists():
        downloads_dir.mkdir(parents=True)
        print("✅ Created downloads directory")
    
    # Required Python packages
    required_packages = ["flask", "yt_dlp"]
    missing_packages = []
    
    for package in required_packages:
        if not check_python_package(package):
            missing_packages.append(package)
    
    if missing_packages:
        print("\n📦 Installing missing Python packages...")
        for package in missing_packages:
            install_python_package(package)
    else:
        print("✅ All required Python packages are installed")
    
    # Check for aria2c
    if not check_dependency("aria2c"):
        print("\nℹ️ aria2c is recommended for faster downloads but not required.")
        if platform.system() == "Linux":
            print("   Install with: sudo apt install aria2")
        elif platform.system() == "Darwin":  # macOS
            print("   Install with: brew install aria2")
        elif platform.system() == "Windows":
            print("   Install with: choco install aria2 or download from https://github.com/aria2/aria2/releases")
    else:
        print("✅ aria2c is installed")
    
    # Run the app
    print("\n🚀 Starting the video downloader server...")
    
    # Try to open browser automatically
    url = "http://localhost:8000"
    try:
        webbrowser.open(url)
        print(f"✅ Opened browser to {url}")
    except:
        print(f"ℹ️ Please open your browser and navigate to {url}")
    
    # Start the server
    try:
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Thank you for using Chroma Video Downloader!")

if __name__ == "__main__":
    main()
