import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import secrets

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
        msg = MIMEMultipart()
        msg['From'] = f"MINORE BARBER <{os.getenv('EMAIL_FROM')}>"
        msg['To'] = client_email
        msg['Subject'] = f"✅ Appointment Confirmed - {appointment_time.strftime('%b %d at %I:%M %p')}"
        
        cancel_url = f"{os.getenv('BASE_URL', 'http://localhost:8000')}/cancel-appointment/{cancel_token}"
        
        body = f"""
Hello {client_name},

Your appointment has been confirmed at MINORE BARBER!

APPOINTMENT DETAILS:
• Service: {service_name}
• Barber: {barber_name}
• Date & Time: {appointment_time.strftime('%A, %B %d, %Y at %I:%M %p')}
• Location: MINORE BARBER - {location_name or 'MALLORCA'}
• Address: {get_location_address(location_name)}

IMPORTANT:
• Please arrive 5 minutes early
• Cancel at least 2 hours in advance if needed

Need to cancel? Click: {cancel_url}

Best regards,
MINORE BARBER Team
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(os.getenv('EMAIL_HOST'), int(os.getenv('EMAIL_PORT')))
        server.starttls()
        server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASSWORD'))
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Email sent via Gmail to {client_email}")
        return True
        
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

CANCELLED APPOINTMENT:
• Service: {service_name}
• Date & Time: {appointment_time.strftime('%A, %B %d, %Y at %I:%M %p')}

You can book a new appointment anytime at our website.

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