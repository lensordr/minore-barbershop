#!/usr/bin/env python3
"""
Test Gmail SMTP email sending
"""

import os
from email_service import send_appointment_email, generate_cancel_token
from datetime import datetime, timedelta

def test_email():
    # Test appointment details
    client_email = "rares.og@gmail.com"
    client_name = "Rares Test"
    service_name = "Classic Haircut"
    barber_name = "Luca"
    appointment_time = datetime.now() + timedelta(days=1)
    cancel_token = generate_cancel_token()
    location_name = "MALLORCA"
    
    print(f"Sending test email to {client_email}...")
    
    success = send_appointment_email(
        client_email, 
        client_name, 
        service_name, 
        barber_name, 
        appointment_time, 
        cancel_token, 
        location_name
    )
    
    if success:
        print("✅ Test email sent successfully!")
    else:
        print("❌ Test email failed!")

if __name__ == "__main__":
    test_email()