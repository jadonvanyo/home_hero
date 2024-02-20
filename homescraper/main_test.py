from analysis_functions import all_required_values_present, create_featured_house_email, create_house_analysis_excel_book, config_file_required_values_present, load_json, send_featured_house_email
from datetime import date
import json

# Get all of the house data from homedata.json
with open('homedata2.json') as file:
    data = json.load(file)

# Check if there are any houses in the list pulled
if not data:
    print("No houses found")
    
else:
    # Establish all the potential target variables required
    required_target_values = [
        "target_cash_flow_monthly_min",
        "target_percent_rule_min",
        "target_net_operating_income_min",
        "target_pro_forma_cap_min",
        "target_five_year_annualized_return_min",
        "target_cash_on_cash_return_min"
    ]
    
    # Load the config file
    config = load_json("config.json")
    
    # TODO: Verify all numbers in config.json are accurate (non zero, positive, within a specific range)
    if config_file_required_values_present(config):
        # Create a name for the excel file
        excel_filename = str(date.today()) + "-house-analysis.xlsx"
        
        # Create an excel book containing all of the houses that were scraped for analysis
        create_house_analysis_excel_book(config, data, excel_filename)
        
        # Create the email html content for the analyzed houses
        email_content_html = create_featured_house_email(data, required_target_values, config)
        print(email_content_html)
        
        # # Send the html email content and excel file to the target user
        # send_featured_house_email(email_content_html, excel_filename)
    
    else:
        print("Missing information in config.json")