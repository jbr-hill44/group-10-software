import yagmail
import random
import string
import os
from dotenv import load_dotenv
from config import sender_mail, sender_mail_pass

# Load environment variables from .config file
load_dotenv()

def generate_otp():
    '''Generate one-time password'''
    otp = ''.join(random.choices(string.digits, k=4))
    return otp

def send_email(email, otp):
    sender_email = sender_mail
    password = sender_mail_pass  # your App Password if 2-factor authentication (2FA) is enabled
    
    # Initialize the Yagmail SMTP client
    yag = yagmail.SMTP(sender_email, password)
    
    # Send the email
    subject = 'OTP Verification'
    body = f"Your OTP is: {otp}"
    yag.send(to=email, subject=subject, contents=body)
    
    print(f'OTP sent to {email} successfully.')
