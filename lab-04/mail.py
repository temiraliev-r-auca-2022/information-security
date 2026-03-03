import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os
from datetime import datetime

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "temiraliev_r@auca.kg"
SENDER_PASSWORD = "your_app_password"
RECEIVER_EMAIL = "tala0068@gmail.com"

# Local server URL (when testing locally)
PHISHING_URL = "http://localhost:8000"

# HTML Email Template
def create_phishing_email():
    current_year = datetime.now().year
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Payment Verification Required</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                line-height: 1.6;
                color: #333333;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            .container {{
                max-width: 600px;
                margin: 20px auto;
                background: white;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px 20px;
                text-align: center;
            }}
            .logo {{
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            .badge {{
                background: rgba(255,255,255,0.2);
                padding: 5px 15px;
                border-radius: 20px;
                display: inline-block;
                font-size: 14px;
            }}
            .content {{
                padding: 30px;
            }}
            .alert {{
                background: #f8f9fa;
                border-left: 4px solid #dc3545;
                padding: 15px;
                margin: 20px 0;
                border-radius: 4px;
            }}
            .button {{
                display: inline-block;
                padding: 12px 30px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white !important;
                text-decoration: none;
                border-radius: 25px;
                margin: 20px 0;
                font-weight: bold;
                box-shadow: 0 4px 6px rgba(50,50,93,.11), 0 1px 3px rgba(0,0,0,.08);
            }}
            .warning {{
                background: #fff3cd;
                border: 1px solid #ffeeba;
                color: #856404;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                margin: 20px 0;
            }}
            .footer {{
                background: #f8f9fa;
                padding: 20px;
                text-align: center;
                font-size: 12px;
                color: #6c757d;
                border-top: 1px solid #dee2e6;
            }}
            .security-badge {{
                text-align: center;
                margin-top: 15px;
            }}
            .security-badge img {{
                width: 100px;
                opacity: 0.7;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">🔒 SecurePay</div>
                <div class="badge">Verified by Visa & Mastercard</div>
            </div>
            
            <div class="content">
                <h2 style="color: #333; margin-bottom: 20px;">Payment Verification Required</h2>
                
                <div class="alert">
                    <strong>⚠️ Action Required:</strong> Your recurring payment of $49.99 for "Premium Subscription" could not be processed.
                </div>
                
                <p>Dear Valued Customer,</p>
                
                <p>We attempted to process your recurring payment for the Premium Subscription plan, but the transaction was declined by your bank. This could be due to:</p>
                
                <ul style="color: #666; margin: 20px 0;">
                    <li>Expired credit card</li>
                    <li>Insufficient funds</li>
                    <li>Bank security restrictions</li>
                    <li>Incorrect card information</li>
                </ul>
                
                <p>To avoid service interruption and potential late fees, please verify your payment information immediately:</p>
                
                <div style="text-align: center;">
                    <a href="{PHISHING_URL}" class="button">🔒 Verify Payment Method</a>
                </div>
                
                <div class="warning">
                    <strong>⏰ Deadline:</strong> Please update your information within 24 hours to prevent service suspension.
                </div>
                
                <p style="font-size: 14px; color: #666;">If you've already updated your payment information, please ignore this message.</p>
                
                <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                
                <p style="font-size: 12px; color: #999;">
                    <strong>Transaction Details:</strong><br>
                    Date: {datetime.now().strftime('%B %d, %Y')}<br>
                    Amount: $49.99<br>
                    Reference: TXN-{datetime.now().strftime('%Y%m%d%H%M%S')}
                </p>
            </div>
            
            <div class="footer">
                <div class="security-badge">
                    🔒 256-bit SSL Encrypted | Verified by Visa | Mastercard SecureCode
                </div>
                <p style="margin-top: 15px;">
                    This is an automated message from our secure payment system. Please do not reply to this email.
                </p>
                <p style="margin-top: 15px;">
                    © {current_year} SecurePay. All rights reserved.<br>
                    123 Financial District, San Francisco, CA 94105
                </p>
                <p style="margin-top: 20px; font-size: 10px; color: #ccc;">
                    ⚠️ This is a simulated phishing email for educational purposes only.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

def send_phishing_email():
    """Send the phishing simulation email"""
    
    # Create message
    message = MIMEMultipart('alternative')
    message["From"] = SENDER_EMAIL
    message["To"] = RECEIVER_EMAIL
    message["Subject"] = "⚠️ Action Required: Your payment could not be processed"
    
    # Add headers to avoid spam filters (for educational purposes)
    message.add_header('List-Unsubscribe', '<mailto:unsubscribe@example.com>')
    message.add_header('Feedback-ID', f"{datetime.now().timestamp()}:example")
    
    # Create HTML content
    html_content = create_phishing_email()
    
    # Attach HTML part
    html_part = MIMEText(html_content, 'html')
    message.attach(html_part)
    
    try:
        # Connect to SMTP server
        print(f"📧 Connecting to {SMTP_SERVER}...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        
        # Login
        print(f"🔑 Logging in as {SENDER_EMAIL}...")
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        # Send email
        print(f"📨 Sending email to {RECEIVER_EMAIL}...")
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())
        
        print("✅ Phishing simulation email sent successfully!")
        print(f"🎯 Target: {RECEIVER_EMAIL}")
        print(f"🔗 Phishing URL: {PHISHING_URL}")
        
        server.quit()
        
    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. For Gmail, use an App Password instead of your regular password")
        print("2. Enable 'Less secure app access' if using regular password")
        print("3. Check your internet connection")
        print("4. Verify SMTP settings are correct")

def test_connection():
    """Test SMTP connection without sending email"""
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        print("✅ SMTP connection test successful!")
        server.quit()
        return True
    except Exception as e:
        print(f"❌ SMTP connection test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("Phishing Email Simulation")
    print("="*60)
    print("\n⚠️  FOR EDUCATIONAL PURPOSES ONLY ⚠️")
    print("\nConfiguration:")
    print(f"  SMTP Server: {SMTP_SERVER}")
    print(f"  SMTP Port: {SMTP_PORT}")
    print(f"  Sender: {SENDER_EMAIL}")
    print(f"  Recipient: {RECEIVER_EMAIL}")
    print(f"  Phishing URL: {PHISHING_URL}")
    
    print("\nOptions:")
    print("  1. Send phishing email")
    print("  2. Test SMTP connection only")
    print("  3. Exit")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == "1":
        print("\n" + "="*60)
        send_phishing_email()
        print("="*60)
    elif choice == "2":
        print("\n" + "="*60)
        test_connection()
        print("="*60)
    else:
        print("Exiting...")
