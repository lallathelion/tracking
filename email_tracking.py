import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import datetime

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = '7307645@gmail.com'  # Replace with your Gmail address
EMAIL_PASSWORD = 'zubj hngg rygb pxpm'  # Replace with your app password
RECIPIENT_EMAILS = ['8009698@gmail.com', '8009869@gmail.com']  # List of recipients

# Tracking server configuration
TRACKING_IMAGE_URL_1 = 'https://www.bing.com/images/search?view=detailV2&ccid=iDvQH2mK&id=A30D945891F5A7626C72AC14B59B3EE0161C2730&thid=OIP.iDvQH2mK3omhPoWdSonQVgHaEK&mediaurl=https%3A%2F%2Flogos-world.net%2Fwp-content%2Fuploads%2F2020%2F09%2FGoogle-Logo-1998-1999.jpg&exph=2160&expw=3840'
TRACKING_IMAGE_URL_2 = 'https://www.bing.com/images/search?view=detailV2&ccid=87vo3z5V&id=A5FA55B87B2235B37BCEB83659FB42E912A1422A&thid=OIP.87vo3z5V-mwhQDDrWe8-SwAAAA&mediaurl=https%3A%2F%2Fnews-cdn.softpedia.com%2Fimages%2Fnews2%2FGoogle-incotro-2.jpg&exph=224&expw=220'

# HTTP server to handle image requests (if hosting locally)
class TrackingImageHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"Email opened at {timestamp} by {self.client_address[0]}")
        self.send_response(200)
        self.end_headers()

def start_tracking_server():
    server = HTTPServer(('0.0.0.0', 8080), TrackingImageHandler)
    print("Tracking server started on port 8080")
    server.serve_forever()

# Send email with tracking images
def send_email_with_tracking():
    for recipient in RECIPIENT_EMAILS:
        # Create the email
        msg = MIMEMultipart('alternative')
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient
        msg['Subject'] = 'Test Email with External Images for Tracking'

        # HTML body with the external images
        html = f"""
        <html>
          <body>
            <p>This is a test email with tracking images.</p>
            <img src="{TRACKING_IMAGE_URL_1}" alt="Tracking Image 1" style="display:none;" />
            <img src="{TRACKING_IMAGE_URL_2}" alt="Tracking Image 2" style="display:none;" />
          </body>
        </html>
        """
        msg.attach(MIMEText(html, 'html'))

        # Send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, recipient, msg.as_string())
        print(f"Email sent to {recipient} with tracking images.")

if __name__ == '__main__':
    # Start the tracking server in a separate thread (if using a local server)
    server_thread = threading.Thread(target=start_tracking_server)
    server_thread.daemon = True
    server_thread.start()

    # Send the email
    send_email_with_tracking()

    # Keep the script running to allow the server to track requests
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Tracking server stopped.")
