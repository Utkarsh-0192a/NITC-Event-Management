import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendmail(email, sub, body):
    # Email configuration
    sender_email = "dipanshutiwari1155@gmail.com"
    recipient_email = f"{email}"
    subject = sub
    body = body

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:  # Use your SMTP server
            server.starttls()  # Upgrade to a secure connection
            server.login(sender_email, "jrfz fvxf pxbc kjpj")  # Login to the email account
            server.send_message(msg)  # Send the email
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")