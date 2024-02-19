from analysis_functions import create_featured_house_email, create_house_analysis_excel_book, send_featured_house_email
from datetime import date
import json

# Get all of the house data from homedata.json
with open('homedata2.json') as file:
    data = json.load(file)

# Check if there are any houses in the list pulled
if not data:
    print("No houses found")
    
else:
    # Create a name for the excel file
    excel_filename = str(date.today()) + "-house-analysis.xlsx"
    
    # Create an excel book containing all of the houses that were scraped for analysis
    create_house_analysis_excel_book(data, excel_filename)
    
    # Create the email html content for the analyzed houses
    email_content_html = create_featured_house_email(data)
    
    # Send the html email content and excel file to the target user
    send_featured_house_email(email_content_html, excel_filename)