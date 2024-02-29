import asyncio
from twisted.internet import asyncioreactor
asyncioreactor.install(asyncio.get_event_loop()) # Explicitly install and run a reactor before any imports

from analysis_functions import analyze_all_houses, create_house_analysis_excel_book, config_file_required_values_present, delete_file, config_file_required_email_values_present, load_json, send_featured_house_email, send_error_email
from datetime import date
from homescraper.spiders.rentspider import RentspiderSpider
from homescraper.spiders.taxspider import TaxspiderSpider
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

# Try to load the config file
config = load_json("config.json")

# Exit the program if no config file can be found
if not config:
    exit(1)

# Generate any error messages from the required values in the config file
error_messages = config_file_required_values_present(config)

# Verify all required values in the config file are present and accurate
if error_messages:
    for error in error_messages:
        print(error)
    exit(1)

# Generate any error messages from the required email values in the config file
error_messages = config_file_required_email_values_present(config)

# Verify all required email values in the config file are present and accurate
if error_messages:
    for error in error_messages:
        print(error)
    exit(1)

# Load in homespider after the config file has been verified since it is dependent on the config file
from homescraper.spiders.homespider import HomespiderSpider

# Get and configure the settings for all the spiders
settings = get_project_settings()
configure_logging(settings)

# Create instance of CrawlerRunner class to execute multiple spiders in the script using project settings
runner = CrawlerRunner(settings)

# Create a function to run the spiders sequentially and stop the twisted reactor after all the spiders have run
@defer.inlineCallbacks
def crawl():
    yield runner.crawl(HomespiderSpider)
    yield runner.crawl(TaxspiderSpider)
    yield runner.crawl(RentspiderSpider)
    reactor.stop()

# Call the crawl function to loop through the spiders sequentially
crawl()
reactor.run()  # the script will block here until the last crawl call is finished

# Try to pull the scraped home data
data = load_json("homedata.json")

# TODO: Remove all email_config
# Check if there are any houses in the list pulled
if not data:
    error_message = "No houses were found during the search."
    print(error_message)
    send_error_email(error_message, config)
    
else:   
    # Retrieve a list containing all the analyzed houses and one with any houses missing data
    analyzed_houses, error_houses = analyze_all_houses(config, data)
    
    # Verify there are analyzed houses to send to the user
    if len(analyzed_houses) == 0:
        error_message = f"{len(error_houses)} houses were scraped, but none contained all the required information. Review scrapping process for more details."
        print(error_message)
        send_error_email(error_message, config)
        exit(1)
    
    # Create a name for the excel file
    excel_filename = str(date.today()) + "-house-analysis.xlsx"
    
    # Create an excel book containing all of the houses that were scraped for analysis
    create_house_analysis_excel_book(analyzed_houses, excel_filename)
    
    # Send the html email content and excel file to the target user
    send_featured_house_email(analyzed_houses, excel_filename, config)
    
    # Determine if the user wants the file deleted
    if config['delete_excel_file']:
        # Delete the excel file that was created
        delete_file(config, excel_filename)