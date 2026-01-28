import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import secrets
import requests
import json

load_dotenv()

def generate_cancel_token():
    return secrets.token_urlsafe(32)

def get_location_address(location_name):
    if location_name and location_name.upper() == 'CONCELL':
        return 'Consell de Cent 250'
    else:
        return 'Carrer de Mallorca 233'

def send_appointment_email(client_email, client_name, service_name, barber_name, appointment_time, cancel_token, location_name=None):
    try:
        cancel_url = f"{os.getenv('BASE_URL', 'http://localhost:8000')}/cancel-appointment/{cancel_token}"
        
        # Professional HTML email template
        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Appointment Confirmation</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="background: #1d1a1c; color: #fbcc93; padding: 20px; text-align: center; border-radius: 8px 8px 0 0;">
        <h1 style="margin: 0; font-size: 24px;">MINORE BARBER</h1>
        <p style="margin: 5px 0 0 0; font-size: 14px;">Appointment Confirmation</p>
    </div>
    
    <div style="background: #f9f9f9; padding: 20px; border-radius: 0 0 8px 8px;">
        <p>Hello <strong>{client_name}</strong>,</p>
        
        <p>Your appointment has been confirmed! We look forward to seeing you.</p>
        
        <div style="background: white; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #fbcc93;">
            <h3 style="margin-top: 0; color: #1d1a1c;">📅 Appointment Details</h3>
            <p><strong>Service:</strong> {service_name}</p>
            <p><strong>Barber:</strong> {barber_name}</p>
            <p><strong>Date & Time:</strong> {appointment_time.strftime('%A, %B %d, %Y at %I:%M %p')}</p>
            <p><strong>Location:</strong> MINORE BARBER - {location_name or 'MALLORCA'}</p>
            <p><strong>Address:</strong> {get_location_address(location_name)}</p>
        </div>
        
        <div style="background: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <h4 style="margin-top: 0; color: #856404;">⏰ Important Reminders</h4>
            <ul style="margin: 0; padding-left: 20px;">
                <li>Please arrive 5 minutes early</li>
                <li>Bring a valid ID if requested</li>
                <li>Cancel at least 2 hours in advance if needed</li>
            </ul>
        </div>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="{cancel_url}" style="background: #dc3545; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">Cancel Appointment</a>
        </div>
        
        <p>Questions? Reply to this email or call us directly.</p>
        
        <p>Best regards,<br><strong>MINORE BARBER Team</strong></p>
    </div>
    
    <div style="text-align: center; padding: 15px; font-size: 12px; color: #666;">
        <p>This email was sent because you booked an appointment with MINORE BARBER.</p>
        <p>© 2024 MINORE BARBER. All rights reserved.</p>
    </div>
</body>
</html>
        """
        
        # Plain text version for better deliverability
        text_body = f"""
Hello {client_name},

Your appointment has been confirmed at MINORE BARBER!

APPOINTMENT DETAILS:
• Service: {service_name}
• Barber: {barber_name}
• Date & Time: {appointment_time.strftime('%A, %B %d, %Y at %I:%M %p')}
• Location: MINORE BARBER - {location_name or 'MALLORCA'}
• Address: {get_location_address(location_name)}

IMPORTANT REMINDERS:
• Please arrive 5 minutes early
• Bring a valid ID if requested
• Cancel at least 2 hours in advance if needed

NEED TO CANCEL?
Click here: {cancel_url}

Questions? Reply to this email or call us directly.

Best regards,
MINORE BARBER Team

---
This email was sent because you booked an appointment with MINORE BARBER.
© 2024 MINORE BARBER. All rights reserved.
        """
        
        api_key = os.getenv('EMAIL_PASSWORD')  # SendGrid API key
        
        data = {
            "personalizations": [{
                "to": [{"email": client_email, "name": client_name}],
                "subject": f"✅ Appointment Confirmed - {appointment_time.strftime('%b %d at %I:%M %p')}"
            }],
            "from": {
                "email": os.getenv('EMAIL_FROM'), 
                "name": "MINORE BARBER"
            },
            "reply_to": {
                "email": os.getenv('EMAIL_FROM'),
                "name": "MINORE BARBER"
            },
            "content": [
                {"type": "text/plain", "value": text_body},
                {"type": "text/html", "value": html_body}
            ],
            "categories": ["appointment_confirmation"],
            "custom_args": {
                "appointment_type": "confirmation",
                "location": location_name or "mallorca"
            }
        }
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        print(f"Sending confirmation email to {client_email}")
        response = requests.post(
            "https://api.sendgrid.com/v3/mail/send",
            headers=headers,
            data=json.dumps(data)
        )
        
        if response.status_code == 202:
            print("✅ Email sent successfully via SendGrid!")
            return True
        else:
            print(f"❌ SendGrid error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"Email error: {e}")
        return False

def send_cancellation_email(client_email, client_name, appointment_time, service_name):
    try:
        msg = MIMEMultipart()
        msg['From'] = os.getenv('EMAIL_FROM')
        msg['To'] = client_email
        msg['Subject'] = "MINORE BARBER - Appointment Cancelled"
        
        body = f"""
        Hello {client_name},

        Your appointment has been cancelled as requested.

        📅 CANCELLED APPOINTMENT:
        • Service: {service_name}
        • Date & Time: {appointment_time.strftime('%A, %B %d, %Y at %I:%M %p')}

        📝 WHAT'S NEXT?
        • Your time slot is now available for other customers
        • You can book a new appointment anytime at our website
        • No cancellation fees apply

        📞 QUESTIONS?
        Feel free to contact us if you need any assistance.

        We hope to see you again soon!
        
        Best regards,
        MINORE BARBER Team
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(os.getenv('EMAIL_HOST'), int(os.getenv('EMAIL_PORT')))
        server.starttls()
        server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASSWORD'))
        server.send_message(msg)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Cancellation email error: {e}")
        return False