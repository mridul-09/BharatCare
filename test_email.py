import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
USERNAME = "mridulsrivastava101@gmail.com"
PASSWORD = "wvlm dqon uzgv vutm"  # App password

RECIPIENT = "connects.sde@gmail.com"  # Test recipient email

# Compose the email
subject = "Test Email"
body = "This is a test email sent from the Python script using Flask and SMTP."

msg = MIMEMultipart()
msg['From'] = USERNAME
msg['To'] = RECIPIENT
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))

try:
    # Set up the server
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(USERNAME, PASSWORD)
    server.sendmail(USERNAME, RECIPIENT, msg.as_string())
    server.quit()
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
