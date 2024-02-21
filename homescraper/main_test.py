from analysis_functions import analyze_all_houses, create_featured_house_email, create_house_analysis_excel_book, config_file_required_values_present, load_json, send_featured_house_email
from datetime import date
import json

# TODO: use try on all the open json files
# Get all of the house data from homedata.json
data = load_json("homedata2.json")

# Check if there are any houses in the list pulled
if not data:
    print("No houses found")
    
else:
    # Load the config file
    config = load_json("config.json")
    
    # TODO: Verify all numbers in config.json are accurate (non zero, positive, within a specific range)
    if config_file_required_values_present(config):
        
        # Retrieve a list containing all the analyzed houses and one with any houses missing data
        analyzed_houses, error_houses = analyze_all_houses(config, data)
        
        # Create a name for the excel file
        # excel_filename = str(date.today()) + "-house-analysis.xlsx"
        
        # Create an excel book containing all of the houses that were scraped for analysis
        # create_house_analysis_excel_book(analyzed_houses, excel_filename)
        
        # Create the email html content for the analyzed houses
        email_content_html = create_featured_house_email(analyzed_houses, config)
        print(email_content_html)
        
        # # Send the html email content and excel file to the target user
        # send_featured_house_email(email_content_html, excel_filename)
    
    else:
        print("Missing information in config.json")