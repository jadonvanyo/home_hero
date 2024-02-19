from analysis_functions import create_featured_house_email
from datetime import date
import json

# Get all of the house data from homedata.json
with open('homedata2.json') as file:
    data = json.load(file)

# Check if there are any houses in the list pulled
if not data:
    print("No houses found")
    
else:
    # Create the email html content for the analyzed houses
    email_content_html = create_featured_house_email(data)
    
    print(email_content_html)