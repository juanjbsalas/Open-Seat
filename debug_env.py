#!/usr/bin/env python3
"""
Debug .env file loading
"""
import os

print("🔍 Debug: Environment Variable Loading")
print("=" * 50)

# Check current directory
print(f"Current directory: {os.getcwd()}")

# Check if .env file exists
env_file = ".env"
if os.path.exists(env_file):
    print(f"✅ .env file found at: {os.path.abspath(env_file)}")
    
    # Read and display .env contents (safely)
    with open(env_file, 'r') as f:
        lines = f.readlines()
        print(f"📄 .env file contents ({len(lines)} lines):")
        for i, line in enumerate(lines, 1):
            if line.strip():
                key = line.split('=')[0] if '=' in line else line.strip()
                print(f"   Line {i}: {key}=***")
else:
    print(f"❌ .env file not found at: {os.path.abspath(env_file)}")

print("\n🔧 Testing dotenv import...")
try:
    from dotenv import load_dotenv
    print("✅ python-dotenv imported successfully")
    
    # Load .env file
    result = load_dotenv()
    print(f"✅ load_dotenv() returned: {result}")
    
except ImportError:
    print("❌ python-dotenv not installed")
    print("Run: pip install python-dotenv")

print("\n📧 Checking environment variables...")
sender_email = os.getenv('SENDER_EMAIL')
sender_password = os.getenv('SENDER_PASSWORD')

print(f"SENDER_EMAIL: {'✅ Found' if sender_email else '❌ Not found'}")
if sender_email:
    print(f"  Value: {sender_email}")

print(f"SENDER_PASSWORD: {'✅ Found' if sender_password else '❌ Not found'}")
if sender_password:
    print(f"  Length: {len(sender_password)} characters")

print("\n💡 All environment variables:")
for key, value in os.environ.items():
    if 'SENDER' in key:
        print(f"  {key}: {value[:3]}***{value[-3:] if len(value) > 6 else '***'}")