"""
Test script to verify keylogger and API are working
"""

import requests
import time
import json

def test_api_server():
    """Test if API server is running"""
    try:
        response = requests.get("http://localhost:5000/")
        if response.status_code == 200:
            print("✅ API server is running")
            return True
    except:
        print("❌ API server is not running")
        return False

def test_send_data():
    """Test sending data to API"""
    test_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "hostname": "test-machine",
        "keystrokes": "This is a test message from the keylogger",
        "raw_data": ["T", "h", "i", "s", " ", "i", "s", " ", "a", " ", "t", "e", "s", "t"]
    }
    
    try:
        response = requests.post(
            "http://localhost:5000/api/keystrokes",
            json=test_data
        )
        if response.status_code == 200:
            print("✅ Test data sent successfully")
            return True
        else:
            print(f"❌ Failed to send test data: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error sending test data: {e}")
        return False

def view_stats():
    """View API statistics"""
    try:
        response = requests.get("http://localhost:5000/api/stats")
        if response.status_code == 200:
            stats = response.json()
            print("\n📊 API Statistics:")
            print(json.dumps(stats, indent=2))
    except:
        pass

if __name__ == "__main__":
    print("="*60)
    print("🔐 KEYLOGGER TEST SCRIPT")
    print("="*60)
    
    if test_api_server():
        test_send_data()
        view_stats()
    
    print("\n" + "="*60)
    print("Next steps:")
    print("1. Start API server: python api_server.py")
    print("2. Start keylogger: python keylogger.py")
    print("3. Type something in any application")
    print("4. Check received data at: http://localhost:5000/view/data")
    print("="*60)
