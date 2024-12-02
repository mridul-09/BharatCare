import smtplib
from email.mime.text import MIMEText

# SMTP Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
USERNAME = "mridulsrivastava101@gmail.com"  # Your email
PASSWORD = "wvlm dqon uzgv vutm"            # Your app password

# Email Details
msg = MIMEText("This is a test email.")
msg["Subject"] = "Test Email"
msg["From"] = USERNAME
msg["To"] = "connects.sde@gmail.com"        # Recipient email

try:
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(USERNAME, PASSWORD)
    server.sendmail(USERNAME, [msg["To"]], msg.as_string())
    server.quit()
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
