#!/usr/bin/env python3
import os
from email_service import send_appointment_email
from datetime import datetime, timedelta

# Test with production environment variables
print("Testing email with production settings...")
print(f"EMAIL_HOST: {os.getenv('EMAIL_HOST')}")
print(f"EMAIL_PORT: {os.getenv('EMAIL_PORT')}")
print(f"EMAIL_USER: {os.getenv('EMAIL_USER')}")
print(f"EMAIL_FROM: {os.getenv('EMAIL_FROM')}")

success = send_appointment_email(
    client_email="your-test-email@gmail.com",
    client_name="Test Customer",
    appointment_time=datetime.now() + timedelta(hours=2),
    service_name="Test Haircut",
    barber_name="Test Barber",
    cancel_token="test-123"
)

print(f"Email sent: {success}")