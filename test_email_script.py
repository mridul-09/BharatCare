import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
USERNAME = "mridulsrivastava101@gmail.com"  # Replace with your Gmail
PASSWORD = "wvlm dqon uzgv vutm"  # App password from Google

# Recipient Email (Replace with the target email address)
RECIPIENT = "connects.sde@gmail.com"

# Compose the email
subject = "Test Email"
body = "This is a test email sent from the Python script using Flask and SMTP."

# Creating email message
msg = MIMEMultipart()
msg['From'] = USERNAME
msg['To'] = RECIPIENT
msg['Subject'] = subject

msg.attach(MIMEText(body, 'plain'))

try:
    # Setting up the server
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()  # Secure the connection
    server.login(USERNAME, PASSWORD)  # Login to the email account
    server.sendmail(USERNAME, RECIPIENT, msg.as_string())  # Send the email
    server.quit()  # Close the connection
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
