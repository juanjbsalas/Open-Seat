#!/usr/bin/env python3
"""
Test secure email configuration
"""
import os

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()  # This loads the .env file
    print("✅ dotenv loaded successfully")
except ImportError:
    print("❌ python-dotenv not installed. Run: pip install python-dotenv")

from notifier import send_email

def test_env_variables():
    """Test if environment variables are loaded"""
    print("🔍 Checking environment variables...")
    
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    
    if sender_email:
        print(f"✅ SENDER_EMAIL found: {sender_email}")
    else:
        print("❌ SENDER_EMAIL not found")
        
    if sender_password:
        print(f"✅ SENDER_PASSWORD found: {'*' * len(sender_password)}")
    else:
        print("❌ SENDER_PASSWORD not found")
        
    return bool(sender_email and sender_password)

def test_email_sending():
    """Test sending an email"""
    test_email = input("Enter your email for testing: ").strip()
    
    try:
        subject = "🔒 Secure Email Test"
        body = """This is a test email from your secure Open Seat application!

✅ Your email credentials are now safely stored in environment variables.
✅ No sensitive data is hardcoded in your source code.
✅ Your application is more secure!

Configuration successful!
"""
        
        send_email(test_email, subject, body)
        print("✅ Secure email test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Email test failed: {str(e)}")
        return False

def main():
    print("🔐 Secure Email Configuration Test")
    print("=" * 40)
    
    # Test 1: Environment variables
    env_ok = test_env_variables()
    
    if not env_ok:
        print("\n💡 Setup Instructions:")
        print("1. Create a .env file with:")
        print("   SENDER_EMAIL=your-email@gmail.com")
        print("   SENDER_PASSWORD=your-app-password")
        print("2. Or set environment variables in your shell")
        return
    
    # Test 2: Email sending
    print("\n📧 Testing email sending...")
    email_ok = test_email_sending()
    
    if email_ok:
        print("\n🎉 All tests passed! Your email is now secure.")
    else:
        print("\n⚠️ Email test failed. Check your credentials.")

if __name__ == "__main__":
    main()