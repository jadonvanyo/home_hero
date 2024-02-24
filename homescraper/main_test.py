from analysis_functions import analyze_all_houses, create_house_analysis_excel_book, config_file_required_values_present, delete_file, email_config_file_required_values_present, load_json, send_featured_house_email, send_error_email
from datetime import date
from homescraper.spiders.rentspider import RentspiderSpider
from homescraper.spiders.taxspider import TaxspiderSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


# Try to load the config file
config = load_json("config.json")

# Exit the program if no config file can be found
if not config:
    exit(1)

# Verify all required values in the config file are present and accurate
if not config_file_required_values_present(config):
    exit(1)

# Check all the email config data in config file if the user requests to send emails
email_config = email_config_file_required_values_present(config)

# If the email config file cannot be loaded or does not have the required information, exit the program
if not email_config:
    exit(1)

# Load in homespider after the config file has been verified since it is dependent on the config file
from homescraper.spiders.homespider import HomespiderSpider

# Get the settings for all of the spiders
settings = get_project_settings()

# Define any custom settings for this project of spiders
process = CrawlerProcess(settings)

# Create a list of all the required spiders to gather the house info
spiders = [HomespiderSpider, TaxspiderSpider, RentspiderSpider]

# Loop through each of the spiders until all the required information has been gathered
for spider in spiders:
    print(f"#################{spider}#################")
    process.crawl(spider)

# Stop the script here until all crawling jobs are finished
process.start()

# Try to pull the scraped home data
data = load_json("homedata.json")

# Check if there are any houses in the list pulled
if not data:
    error_message = "No houses were found during the search."
    print(error_message)
    send_error_email(error_message, config, email_config)
    
else:   
    # Retrieve a list containing all the analyzed houses and one with any houses missing data
    analyzed_houses, error_houses = analyze_all_houses(config, data)
    
    # Verify there are analyzed houses to send to the user
    if len(analyzed_houses) == 0:
        error_message = f"{len(error_houses)} houses were scraped, but none contained all the required information. Review scrapping process for more details."
        print(error_message)
        send_error_email(error_message, config, email_config)
        exit(1)
    
    # Create a name for the excel file
    excel_filename = str(date.today()) + "-house-analysis.xlsx"
    
    # Create an excel book containing all of the houses that were scraped for analysis
    create_house_analysis_excel_book(analyzed_houses, excel_filename)
    
    # Send the html email content and excel file to the target user
    send_featured_house_email(analyzed_houses, excel_filename, config, email_config)
    
    # Delete the excel file that was created
    delete_file(config, excel_filename)