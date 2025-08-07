#!/usr/bin/env python3
"""
Quick test script for macOS setup
Run with: python3 test_mac_setup.py
"""

import sys
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

# Test imports
try:
    import flask
    print(f"✅ Flask {flask.__version__} installed")
except ImportError:
    print("❌ Flask not installed. Run: pip3 install Flask")

try:
    import selenium
    print(f"✅ Selenium installed")
except ImportError:
    print("❌ Selenium not installed. Run: pip3 install selenium")

try:
    from webdriver_manager.chrome import ChromeDriverManager
    print("✅ WebDriver Manager installed")
except ImportError:
    print("❌ WebDriver Manager not installed. Run: pip3 install webdriver-manager")

print("\nIf all packages show ✅, you're ready to run the app with:")
print("python3 app.py")