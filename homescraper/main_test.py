from analysis_functions import all_required_values_present, create_featured_house_email, create_house_analysis_excel_book, send_featured_house_email
from datetime import date
import json

# Get all of the house data from homedata.json
with open('homedata2.json') as file:
    data = json.load(file)

# Check if there are any houses in the list pulled
if not data:
    print("No houses found")
    
else:
    # Establish all the potential target variables required in the config file
    required_config_values = [
        "down_payment_decimal", 
        "closing_cost_buyer_decimal",
        "closing_cost_seller_decimal",
        "expected_annual_growth",
        "interest_rate",
        "loan_term_yrs",
        "expected_repairs_monthly",
        "expected_vacancy_monthly",
        "expected_capx_monthly",
        "expected_management_monthly",
        "insurance_rate_yearly"
    ]
    
    # Establish all the potential target variables required
    required_target_values = [
        "target_cash_flow_monthly_min",
        "target_percent_rule_min",
        "target_net_operating_income_min",
        "target_pro_forma_cap_min",
        "target_five_year_annualized_return_min",
        "target_cash_on_cash_return_min"
    ]
    
    # Establish the required values to analyze a house
    required_house_values = [
        "price",
        "rent",
        "sqft",
        "tax"
    ]
    
    if all_required_values_present(required_config_values, "config.json"):
        # Create a name for the excel file
        excel_filename = str(date.today()) + "-house-analysis.xlsx"
        
        # # Create an excel book containing all of the houses that were scraped for analysis
        # create_house_analysis_excel_book(data, excel_filename)
        
        # Create the email html content for the analyzed houses
        email_content_html = create_featured_house_email(data, required_target_values, required_house_values)
        
        # # Send the html email content and excel file to the target user
        # send_featured_house_email(email_content_html, excel_filename)
    
    else:
        print("Missing information in config.json")