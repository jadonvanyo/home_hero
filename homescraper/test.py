from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import smtplib

# Load the configuration file
def load_config(config_path='config.json'):
    """Load configuration file with all the """
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return config

email_config = load_config(config_path='/Users/jadonvanyo/Desktop/developer-tools/email_config.json')
# Sender and recipient email addresses
sender_address = email_config['sender_address']
receiver_address = email_config['receiver_address']
# Your email account password or an App Password if 2FA is enabled
password = email_config['password']

# Setup the MIME
message = MIMEMultipart()
message['From'] = sender_address
message['To'] = receiver_address
message['Subject'] = 'A test mail sent by Python. It has an attachment.'   # The subject line

# The body and the attachments for the mail
mail_content = '''Hello,
This is a test mail.
In this mail we are sending some attachments.
The mail is sent using Python SMTP library.
Thank You
'''
message.attach(MIMEText(mail_content, 'plain'))

# Create SMTP session for sending the mail
# Use gmail's SMTP server (or adjust for your server)
session = smtplib.SMTP('smtp.gmail.com', 587) 
session.starttls() # enable security
session.login(sender_address, password) # login with mail_id and password
text = message.as_string()
session.sendmail(sender_address, receiver_address, text)
session.quit()
print('Mail Sent')