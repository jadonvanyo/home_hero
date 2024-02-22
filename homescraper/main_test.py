from analysis_functions import analyze_all_houses, create_featured_house_email, create_house_analysis_excel_book, config_file_required_values_present, delete_file, load_json, send_featured_house_email, send_error_email
from datetime import date
from homescraper.spiders.homespider import HomespiderSpider
from homescraper.spiders.rentspider import RentspiderSpider
from homescraper.spiders.taxspider import TaxspiderSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


# TODO: Verify that urls are given
# TODO: Put the crawl process and process.start() into a function

# Try to load the config file
config = load_json("config.json")

# Exit the program if no config file can be found
if not config:
    exit(1)

# Get the settings for all of the spiders
settings = get_project_settings()

# Define any custom settings for this project of spiders
process = CrawlerProcess(settings)

# Crawl zillow for all the available properties from the url in config
process.crawl(HomespiderSpider)

# Stop the script here until all crawling jobs are finished
process.start()

# Crawl zillow for all the available properties from the address in config
process.crawl(RentspiderSpider)

# Stop the script here until all crawling jobs are finished
process.start()

# Crawl zillow for all the available properties from the address in config
process.crawl(TaxspiderSpider)

# Stop the script here until all crawling jobs are finished
process.start()

# Try to pull the scraped home data
data = load_json("homedata2.json")

# Check if there are any houses in the list pulled
if not data:
    print("No houses found")
    
else:
    # Verify all required values in the config file are present and accurate
    if config_file_required_values_present(config):
        
        # Retrieve a list containing all the analyzed houses and one with any houses missing data
        analyzed_houses, error_houses = analyze_all_houses(config, data)
        
        # Verify there are analyzed houses to send to the user
        if len(analyzed_houses) == 0:
            error_message = f"{len(error_houses)} houses were scraped, but none contained all the required information. Review scrapping process for more details."
            print(error_message)
            send_error_email(error_message, config)
            exit(1)
        
        # Create a name for the excel file
        # excel_filename = str(date.today()) + "-house-analysis.xlsx"
        
        # Create an excel book containing all of the houses that were scraped for analysis
        # create_house_analysis_excel_book(analyzed_houses, excel_filename)
        
        # Create the email html content for the analyzed houses
        email_content_html = create_featured_house_email(analyzed_houses, config)
        print(email_content_html)
        
        # Send the html email content and excel file to the target user
        # send_featured_house_email(excel_filename, email_content_html)
        
        # Delete the excel file that was created
        # delete_file(excel_filename)