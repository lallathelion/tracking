import io
import smtplib
import os
from flask import Flask, request, send_file
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

# Load email credentials from environment variables
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# Tracking pixel (invisible 1x1 PNG)
TRACKING_PIXEL = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0eIDATx\x9cc\x62\x60\x60\x60\x00\x00\x00\x04\x00\x01\xf4\xce\x0f\x0e\x00\x00\x00\x00IEND\xaeB`\x82'

@app.route('/pixel.png')
def tracking_pixel():
    """Serves a tracking pixel and logs email opens."""
    print(f"Email opened by {request.remote_addr}")
    return send_file(
        io.BytesIO(TRACKING_PIXEL), 
        mimetype='image/png'
    )

def send_email_with_tracking(recipient_email):
    """Sends an email with a tracking pixel."""
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient_email
    msg['Subject'] = 'Tracked Email'

    # Use your Render service URL instead of ngrok
    render_tracking_url = "https://your-render-app.onrender.com/pixel.png"

    html = f"""
    <html>
      <body>
        <p>Hello, this email contains a tracking pixel.</p>
        <img src="{render_tracking_url}" alt="" style="display:none;" />
      </body>
    </html>
    """
    msg.attach(MIMEText(html, 'html'))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, recipient_email, msg.as_string())
    print("Email sent with tracking pixel.")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
