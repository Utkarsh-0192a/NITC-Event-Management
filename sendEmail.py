import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email():
    message = Mail(
        from_email='dipanshutiwari1155@gmail.com',
        to_emails='dipanshutiwari115@gmail.com',
        subject='Test Email from SendGrid',
        plain_text_content='This is a test email sent using SendGrid API.',
        html_content='<strong>This is a test email sent using SendGrid API.</strong>'
    )
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(f"Email sent! Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")

# Call the function
send_email()