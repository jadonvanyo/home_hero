# Home Hero

This project will scrape homes from Zillow using the Scrapy framework given a list of Zillow URLs and analyze these home's investment potential based on the user's input. The analyzed homes will be given to the user as an Excel file that can be accessed via the project folder or emailed directly to the user. This project was made due to me and some of my friends spending hours each week looking for and analyzing houses on the MLS. This project takes a process that used to take a few hours each week down to a few minutes.

## Table of Contents

- [Background](#background)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Features](#features)
- [Contributing](#contributing)
- [Credits](#credits)
- [License](#license)

## Background

I used to spend hours a week analyzing potential investment properties on Zillow. I would go through the same repetitive task of finding the properties in a given area, looking for all the key information to analyze these properties (taxes, rents, insurance, mortgages, ect.), and plugging all these values into a spreadsheet that would calculate various financial metrics for the house, including monthly insurance, down payment cost, loan amount, closing costs, monthly principle and interest payments, taxes, total operating costs, suggested total rent, and many more. The task was tedious and repetitive, so like any good programmer I decided to automate the collection and data entry, so I could focus on the fun parts. I added the ability to send email to make the process even easier. Just run the script or set it up to run in the cloud and potential investment properties are delivered directly to your inbox. This script will give anyone the ability to easily analysis hundreds of potential investment properties on the MLS, freeing them up to focus on the more fun aspects of investing.

## Dependencies

This project requires the following Python libraries and packages. Ensure you have them installed to run the project successfully:

- `openpyxl`: For creating and manipulating Excel files.
- `scrapy`: For crawling and scraping websites. This includes `CrawlerRunner` and other scrapy utilities.
- `smtplib` and `email.mime`: For sending emails with attachments.
- `twisted`: For asynchronous networking. The project uses Twisted's reactor and defer modules.
- `tabulate`: For pretty-printing tabular data in HTML format.
- `requests`: For sending HTTP requests and handling responses.
- `os`, `json`, `asyncio`: For various utility functions such as file handling, JSON parsing, and asynchronous programming.

You can use the following pip command to install the required Python packages:

```bash
pip install openpyxl scrapy twisted tabulate
```
> **_NOTE:_**  MacOS users will need to use `pip3` instead of `pip`.

Alternatively, you can install the the required dependencies using the `requirements.txt` file. Use the following command while in the home_hero directory:

```bash
pip install -r requirements.txt
```

This project also requires a scrapeops API key that can be obtained for free [here](https://scrapeops.io/). Just create a free account and copy and paste your scrapeops API key into the `config.json` file for `scrapeops_api_key`.

## Installation

This project is built using Python and requires a Python environment to run. Follow these steps to set up and run the project on your local machine.

### Prerequisites

- Python 3.7 or newer
- pip (Python package installer)

### Clone the repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/jayman779/home_hero.git
cd home_hero
```

### Setup Python Virtual Environment

It's recommended to use a virtual environment for Python projects to manage dependencies. Create and activate a virtual environment:

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On MacOS/Linux
source venv/bin/activate
```

### Install Dependencies

Install the required Python libraries mentioned in the Dependencies section using pip:

```bash
pip install openpyxl scrapy twisted tabulate
```
> **_NOTE:_**  MacOS users will need to use `pip3` instead of `pip`.

Alternatively, you can install the the required dependencies using the `requirements.txt` file. Use the following command while in the home_hero directory:

```bash
pip install -r requirements.txt
```

### Configure ScrapeOps API Key

As mentioned in the [Dependencies](#dependencies) section, this project requires a [ScrapeOps](https://scrapeops.io/) API key. After obtaining your API key from ScrapeOps, insert it into the `config.json` file.

Open `config.json` with a text editor and replace "your-scrapeops-api-key" with your actual ScrapeOps API key:

```json
{
    "scrapeops_api_key": "PASTE_YOUR_KEY_HERE",
    ...
}
```

### Gmail Two Factor Authentication Password Setup

If you want to send emails to a Gmail account, you will need to obtain a two factor authentication password using the following steps:

1. Go to your Google Account.
2. Select Security.
3. Under "Signing in to Google," select 2-Step Verification.
4. At the bottom of the page, select App passwords.
5. Enter "home_hero" for the name associated with the password.
6. Select Generate.
7. To enter the app password, follow the instructions on your screen. The app password is the 16-character code that generates on your device.
8. Select Done.

### Final Steps

After completing the above steps, you should be ready to use the project. Proceed to the [Usage](#usage) section for instructions on running the project and analyzing potential investment properties.

## Usage

This project is designed to be fully configurable via a `config.json` file, allowing users to run a series of web scrapers and analyses without direct code manipulation. Follow the steps below to set up and execute the application.

### Step 1: Configuration

Before running the application, you must configure the `config.json` file with your specific parameters. This file includes various settings, such as URLs to scrape, financial assumptions, email settings, and preferences regarding output and notifications.

```json
{
    "scrapeops_api_key": "your-scrapeops-api-key",
    "starturls": ["https://www.zillow.com/fort-lauderdale-fl/duplex/"],
    "down_payment_decimal": 0.12, 
    "closing_cost_buyer_decimal": 0.03,
    ...
    "email_receiver_address": "example_receiver@email.com",
    "email_sender_address": "example_sender@email.com",
    "email_2FA_password": "example_sender_email_password",
    "send_error_emails": false,
    "featured_house_required": true,
    ...
}
```

For a full explanation of each configuration option, refer to the [Configuration](#configuration) section.

The project is preset to be optimized for scraping 1 to 25 houses at a time. If you want to scrape more houses quicker, you can set up proxies for the spider to avoid being blocked for anti-bot behavior. You can do this using the Scrapeops API, but be aware that you will need to start buying credits for rotating the proxies.

In order to run the proxies while scraping, you will want to set the following lines of code in the `settings.py` to the respective values:

```python
SCRAPEOPS_PROXY_ENABLED = True
SCRAPEOPS_PROXY_SETTINGS = {'country': 'us'}
```

In addition, set the following parameters in `settings.py` to speed up the scraping process:

```python
CONCURRENT_REQUESTS = 1
DOWNLOAD_DELAY = 1
```

### Step 2: Running the Application

With your `config.json` file set up, run the application using the following commands in the home_hero directory:

```sh
cd homescraper
python main.py
```

> **_NOTE:_**  MacOS users will need to use `python3` instead of `python`.

This command initiates the scraping process based on your `config.json` settings, followed by an analysis of the collected data. The results will be compiled into an Excel file, and, if configured, an email summary will be sent.

### Step 3: Reviewing Results

After execution, check the output Excel file named with the current date (e.g., `2024-03-15-house-analysis.xlsx`) in the project directory. This file contains a detailed analysis of each property scraped, including financial metrics and other relevant data.

If you enabled email notifications in your configuration, you would also receive an email summary of the analysis, including featured houses that meet criteria that was enabled in your configuration or errors encountered during the scraping and analysis processes.

## Configuration

This section will review all the configurable options for the `config.json` file.

- "scrapeops_api_key" (str): A string containing your Scrapeops API key. This will be validated. See [Configure ScrapeOps API Key](#configure-scrapeops-api-key) for more details on obtaining this key.
- "starturls" (list): List of strings each containing the URL for Zillow to begin scraping. Must contain at least one URL.
- "down_payment_decimal" (float): Decimal representation of the expected down payment percentage. Must be between 0 and 1.
- "closing_cost_buyer_decimal" (float): Decimal representation of the expected closing costs percentage covered by the buyer. This is a percentage of the home purchase price. Must be between 0 and 0.25.
- "closing_cost_seller_decimal" (float): Decimal representation of the expected closing costs percentage covered by the seller. This is a percentage of the home sale price. Must be between 0 and 0.25.
- "expected_annual_growth" (float): Decimal representation of the expected annual growth of the property and rent values percentage. Must be between 0 and 2.
- "interest_rate" (float): Decimal representation of the expected interest rate percentage on the property loan. Must be between 0 and 1.
- "loan_term_yrs" (int): Integer representing the expected number of years for the house loan. Must be between 0 and 50.
- "expected_repairs_monthly" (float): Decimal representation of the expected percentage of monthly rent that will need to go towards repairs for the house each month. Must be between 0 and 0.25.
- "expected_vacancy_monthly" (float): Decimal representation of the expected percentage of monthly rent that will need to go towards potential vacancies for the house each month. Must be between 0 and 0.25.
- "expected_capx_monthly" (float): Decimal representation of the expected percentage of monthly rent that will need to go towards capital expenditures for the house each month. Must be between 0 and 0.25.
- "expected_management_monthly" (float): Decimal representation of the expected percentage of monthly rent that will need to go towards property management for the house each month. Must be between 0 and 0.25.
- "insurance_rate_yearly" (float): Decimal representation of the expected yearly insurance as a percentage of the home's purchased value. Must be between 0 and 0.25.
- "delete_excel_file" (bool): A boolean value representing if you want the excel file deleted after it has been created (`true`) or not (`false`). This should help prevent the files from building up if you are having them emailed. Must be `true` or `false`.
- "send_emails" (bool): A boolean value representing if you want to receive an email containing all excel file (`true`) or not (`false`). An excel file will be generated, regardless of if an email is requested. Must be `true` or `false`.
- "email_receiver_address" (str): A string containing the email address of the intended receiver of the house analysis email. This field is only required if "send_emails" is `true`.
- "email_sender_address" (str): A string containing the email address of the sender of the house analysis email. This field is only required if "send_emails" is `true`.
- "email_2FA_password" (str): A string containing the password for the sender's email address, or the senders 2 factor authentication if the sender is using a Gmail account. Go [here](#gmail-two-factor-authentication-password-setup) see how to obtain a Gmail 2 Factor Authentication Password. This field is only required if "send_emails" is `true`.
- "send_error_emails" (bool): A boolean value representing if the email receiver wants to receive error message emails if any issues arise in the scrapping process (`true`) or not (`false`). This field is only required if "send_emails" is `true`.
- "featured_house_required" (bool): A boolean value representing if the email receiver wants to receive a list of featured houses based on the target values entered (`true`) or not (`false`). This field is only required if "send_emails" is `true`.
- "target_cash_flow_monthly_min" (int or float): An integer or float value representing the minimum monthly cash flow in dollars that the user wants from any of the scrapped properties. This field is optional only if "send_emails" and "featured_house_required" are `true`.
- "target_percent_rule_min" (float): A float value representing the minimum percentage of the purchase price that the user wants the monthly rent to be represented as a decimal. Must be between 0 and 1. This field is optional only if "send_emails" and "featured_house_required" are `true`.
- "target_net_operating_income_min" (int or float): An integer or float value representing the minimum net operating income that a user want the property to make yearly. This field is optional only if "send_emails" and "featured_house_required" are `true`.
- "target_pro_forma_cap_min" (float): Decimal representation of the minimum pro forma cap that a user wants from a given property. Must be between 0 and 1. This field is optional only if "send_emails" and "featured_house_required" are `true`.
- "target_five_year_annualized_return_min" (float): Decimal representation of the minimum annualized return as a percentage after selling the property after 5 years of ownership. Must be between 0 and 1. This field is optional only if "send_emails" and "featured_house_required" are `true`.
- "target_cash_on_cash_return_min" (float): Decimal representation of the minimum cash on cash return that a user wants from a property. Must be between 0 and 1. This field is optional only if "send_emails" and "featured_house_required" are `true`.

Here is an example of a properly formatted configuration that will send an email containing the excel sheet of all the analyzed houses and any featured houses that exceed -$200 in monthly cash flow and a 10% annualized return after 5 years:

```json
{
    "scrapeops_api_key": "user_scrapeops_api_key",
    "starturls": ["https://www.zillow.com/ft-lauderdale-fl/duplex/"],
    "down_payment_decimal": 0.12, 
    "closing_cost_buyer_decimal": 0.03,
    "closing_cost_seller_decimal": 0.08,
    "expected_annual_growth": 0.02,
    "interest_rate": 0.06,
    "loan_term_yrs": 30,
    "expected_repairs_monthly": 0.05,
    "expected_vacancy_monthly": 0.09,
    "expected_capx_monthly": 0.1,
    "expected_management_monthly": 0.1,
    "insurance_rate_yearly": 0.006,
    "delete_excel_file": false,
    "send_emails": true,
    "email_receiver_address": "example_receiver@email.com",
    "email_sender_address": "example_sender@email.com",
    "email_2FA_password": "example_sender_email_password",
    "send_error_emails": false,
    "featured_house_required": true,
    "target_cash_flow_monthly_min": -200,
    "target_percent_rule_min": null,
    "target_net_operating_income_min": null,
    "target_pro_forma_cap_min": null,
    "target_five_year_annualized_return_min": 0.1,
    "target_cash_on_cash_return_min": null
}
```

## Features

Home Hero automates the tedious process of analyzing potential investment properties on Zillow, offering a range of features designed to save time and provide valuable insights. Here are the key features that make Home Hero an essential tool for real estate investors:

### Automated Property Scraping
- **Bulk Property Analysis:** Automatically scrape details of multiple properties from a given Zillow URL, allowing for the analysis of dozens of properties at once.
- **Cleans Scraped Data:** Automatically cleans all the data scraped to return prices, taxes, rent, addresses, number of bedrooms, bathrooms, and property subtypes that are easy to manipulate and analyze.
- **Customizable Search:** Users can specify the URLs of the Zillow listings they're interested in, making the search as broad or as narrow as desired.
- **Comprehensive Data Collection:** The scraping process will return the property address, price, number of bedrooms, bathrooms, square footage, house description, year built, property subtype, region and subdivision the house is located in, yearly taxes, expected monthly rent per unit, minimum and maximum expected rents, structure quality and condition, and URLs from where all the information was found.

### Comprehensive Financial Analysis
- **Detailed Financial Metrics:** Calculates a variety of financial metrics for each property, including monthly insurance, down payment cost, loan amount, closing costs, monthly principle and interest payments, taxes, total operating costs, suggested total rent, estimated monthly cash flows, net operating income, estimated yearly returns, and much more.
- **Investment Potential Evaluation:** Analyzes homes based on user-defined financial assumptions, helping investors to identify properties with the best investment potential.

### Excel Report Generation
- **Customizable Reports:** Generates an Excel file with a detailed analysis of each property, including all calculated financial metrics, which can be accessed directly from the project folder.
- **Automated Email Delivery:** Offers the option to have the Excel file emailed directly to the user, further simplifying the investment analysis process.

### Easy Configuration
- **Fully Configurable via JSON:** All aspects of the project can be configured through a config.json file, including URLs to scrape, financial assumptions, email settings, and output preferences, eliminating the need for direct code manipulation.

### Advanced Features
- **Proxy Support for High-Volume Scraping:** Supports the use of proxies through the ScrapeOps API to avoid being blocked for anti-bot behavior, enabling the scraping of a large number of houses quickly.
- **Email Notifications for Errors and Highlights:** Can be configured to send email notifications for errors encountered during the scraping and analysis processes, as well as summaries including featured houses that meet specific criteria. Featured house emails will include: A link to the house's listing page, key property details such as price, type (property subtype), layout (bedrooms, bathrooms, square footage), price per square foot, and estimated monthly rent with a link to the rent information, financial metrics including monthly operating expenses, total monthly expenses, monthly cash flow, adherence to the 1% rule, cash flow based on the 50% rule, and the estimated total cash needed for the purchase, a table showing a yearly breakdown for the first five years of financial metrics, and a brief description of the property
- **Extensive Error Handling:** All values from the configuration file are checked and verified to handle many potential errors that may arise when attempting to complete the configuration file.

### User-Friendly
- **Gmail Two-Factor Authentication Support:** Includes detailed instructions for setting up a two-factor authentication password for Gmail, ensuring secure email delivery of reports.
- **Comprehensive Documentation:** Offers thorough documentation, including a step-by-step installation guide, comprehensive configuration instructions, and a detailed usage section, making it accessible for users with varying levels of technical expertise.

Home Hero transforms the labor-intensive task of property analysis into a streamlined, automated process, making it easier than ever for investors to assess the investment potential of real estate listings on Zillow.

## Contributing

Thank you for your interest in contributing to this project! Contributions are welcome from anyone who wishes to improve or expand the project.

Here are some ways you can contribute:

- **Reporting bugs:** If you find a bug, please open an issue detailing the problem, how to reproduce it, and any other relevant information.
- **Suggesting enhancements:** Have an idea for a new feature or think something could be improved? Open an issue to suggest your enhancement.
- **Submitting pull requests:** Feel free to fork the repository and submit pull requests with your changes or additions. Whether it's fixing a typo, addressing an issue, or adding a new feature, all contributions are appreciated.

### How to Contribute

1. Fork the repository on GitHub.
2. Clone your fork to your local machine (`git clone YOUR_FORK`).
3. Create your Branch for changes (`git checkout -b YOUR_CHANGES`).
4. Make your changes and commit them with clear, descriptive messages (`git commit -m 'Detailed description of your amazing changes'`).
5. Push to the Branch (`git push origin YOUR_CHANGES`)
6. Submit a pull request against the main branch of this repository.
7. Wait for feedback or approval from the project maintainers.

## Credits

This project was developed by Jadon Vanyo. Special thanks to the following resources for guidance and inspiration:

- **Web Scraping Tutorial:** A comprehensive tutorial on web scraping using Python by Joe Kearney distibuted by freeCodeCamp.org on YouTube. This tutorial was instrumental in helping me understand the fundamentals of web scraping using Scrapy and apply them to this project. Watch the tutorial [here](https://www.youtube.com/watch?v=mBoX_JCKZTE&t=11517s).

I would also like to express my gratitude to the developers and contributors of the libraries and tools used in this project. Their hard work and dedication to open source have made this project possible.

## License

Distributed under the MIT License. See LICENSE for more information.
