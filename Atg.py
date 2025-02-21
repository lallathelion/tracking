import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import subprocess
import requests
import time
import os

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv('7307645@gmail.com')  # Use environment variables for security
EMAIL_PASSWORD = os.getenv('Akash@123')
RECIPIENT_EMAIL = '8009698@gmail.com'

# Tracking server configuration
TRACKING_SERVER_HOST = '0.0.0.0'
TRACKING_SERVER_PORT = 8080

# Invisible 1x1 transparent PNG image
TRACKING_PIXEL = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0eIDATx\x9cc\x62\x60\x60\x60\x00\x00\x00\x04\x00\x01\xf4\xce\x0f\x0e\x00\x00\x00\x00IEND\xaeB`\x82'

# HTTP server to handle tracking pixel requests
class TrackingPixelHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/pixel.png'):
            email = self.path.split('?email=')[-1] if '?email=' in self.path else "Unknown"
            print(f"Email opened by {email} from {self.client_address[0]}")
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            self.wfile.write(TRACKING_PIXEL)
        else:
            self.send_error(404)

def start_tracking_server():
    server = HTTPServer((TRACKING_SERVER_HOST, TRACKING_SERVER_PORT), TrackingPixelHandler)
    print(f"Tracking server started on {TRACKING_SERVER_HOST}:{TRACKING_SERVER_PORT}")
    server.serve_forever()

def start_ngrok():
    """Starts ngrok and returns the public URL."""
    print("Starting ngrok tunnel...")
    ngrok_process = subprocess.Popen(['ngrok', 'http', str(TRACKING_SERVER_PORT)], stdout=subprocess.DEVNULL)
    time.sleep(5)  # Wait for ngrok to initialize
    
    try:
        response = requests.get('http://localhost:4040/api/tunnels')
        tunnels = response.json().get('tunnels', [])
        public_url = tunnels[0]['public_url'] if tunnels else None
        print(f"ngrok tunnel established at: {public_url}")
        return public_url
    except Exception as e:
        print("Error getting ngrok URL:", e)
        return None

def send_email_with_tracking(tracking_url):
    """Sends an email containing the tracking pixel."""
    msg = MIMEMultipart('alternative')
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = 'Test Email with Tracking Pixel'

    # HTML body with tracking pixel
    html = f"""
    <html>
      <body>
        <p>This is a test email.</p>
        <img src="{tracking_url}/pixel.png?email={RECIPIENT_EMAIL}" alt="" style="display:none;" />
      </body>
    </html>
    """
    msg.attach(MIMEText(html, 'html'))

    # Send the email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())

    print("Email sent with tracking pixel.")

if __name__ == '__main__':
    # Start the tracking server in a separate thread
    server_thread = threading.Thread(target=start_tracking_server)
    server_thread.daemon = True
    server_thread.start()

    # Start ngrok and get the public URL
    ngrok_url = start_ngrok()
    
    if ngrok_url:
        # Send the email with the ngrok tracking URL
        send_email_with_tracking(ngrok_url)

    # Keep the script running to allow the tracking server to handle requests
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Tracking server stopped.")
