import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'  # Gmail SMTP server
SMTP_PORT = 587  # Gmail SMTP port (TLS)
EMAIL_ADDRESS = '7307645@gmail.com'  # Replace with your Gmail
EMAIL_PASSWORD = 'qdge haco molv wkko'  # Replace with your App Password
RECIPIENT_EMAIL = '8009698@gmail.com'  # Replace with recipient's email

# Tracking server configuration
TRACKING_SERVER_HOST = '0.0.0.0'  # Host for the tracking server
TRACKING_SERVER_PORT = 8080  # Port for the tracking server
TRACKING_PIXEL_URL = 'https://9789-2401-4900-1ca3-145f-d90c-5d5a-4c37-ff67.ngrok-free.app/pixel.png'


# Invisible 1x1 transparent PNG image
TRACKING_PIXEL = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0eIDATx\x9cc\x62\x60\x60\x60\x00\x00\x00\x04\x00\x01\xf4\xce\x0f\x0e\x00\x00\x00\x00IEND\xaeB`\x82'

# HTTP server to handle tracking pixel requests
class TrackingPixelHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/pixel.png':
            # Log the request (email opened)
            print(f"Email opened by {self.client_address[0]}")
            # Send the tracking pixel
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

# Send email with tracking pixel
def send_email_with_tracking():
    # Create the email
    msg = MIMEMultipart('alternative')
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = 'Test Email with Tracking Pixel'

    # HTML body with tracking pixel
    html = f"""
    <html>
      <body>
        <p>This is a test email.</p>
        <img src="{TRACKING_PIXEL_URL}" alt="" style="display:none;" />
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

    # Send the email
    send_email_with_tracking()

    # Keep the script running to allow the tracking server to handle requests
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Tracking server stopped.")
