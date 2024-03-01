# Home Hero

This project will scrape homes from Zillow based on a given Zillow URL and analyze these home's investment potential based on the user's input. The analyzed homes will be given to the user as an Excel file that can be accessed via the project folder or emailed directly to the user. This project was made due to me and some pf my friends spending hours each week looking for and analyzing houses on the MLS. This project takes a process that used to take a few hours each week down to a few minutes.

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

This project also requires a scrapeops API key that can be obtained for free [here](https://scrapeops.io/). Just create a free account and copy and paste your scrapeops API key into the `config.json` file for `scrapeops_api_key`.

TODO: Finish this section
## Installation

Provide detailed instructions on how to install your project. Include any prerequisites, libraries, or third-party tools that are needed.

```bash
git clone https://github.com/jayman779/home_hero.git
cd home_hero
```

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

- `scrapeops_api_key` (str): A string containing your Scrapeops API key. This will be validated.
- `starturls` (list): List of strings each containing the URL for Zillow to begin scraping. Must contain at least one URL.
- `down_payment_decimal` (float): Decimal representation of the expected down payment percentage. Must be between 0 and 1.
- `closing_cost_buyer_decimal` (float): Decimal representation of the expected closing costs percentage covered by the buyer. This is a percentage of the home purchase price. Must be between 0 and 0.25.
- `closing_cost_seller_decimal` (float): Decimal representation of the expected closing costs percentage covered by the seller. This is a percentage of the home sale price. Must be between 0 and 0.25.
- `expected_annual_growth` (float): Decimal representation of the expected annual growth of the property and rent values percentage. Must be between 0 and 2.
- `interest_rate` (float): Decimal representation of the expected interest rate percentage on the property loan. Must be between 0 and 1.
- `loan_term_yrs` (int): Integer representing the expected number of years for the house loan. Must be between 0 and 50.
- `expected_repairs_monthly` (float): Decimal representation of the expected percentage of monthly rent that will need to go towards repairs for the house each month. Must be between 0 and 0.25.
- `expected_vacancy_monthly` (float): Decimal representation of the expected percentage of monthly rent that will need to go towards potential vacancies for the house each month. Must be between 0 and 0.25.
- `expected_capx_monthly` (float): Decimal representation of the expected percentage of monthly rent that will need to go towards capital expenditures for the house each month. Must be between 0 and 0.25.
- `expected_management_monthly` (float): Decimal representation of the expected percentage of monthly rent that will need to go towards property management for the house each month. Must be between 0 and 0.25.
- `insurance_rate_yearly` (float): Decimal representation of the expected yearly insurance as a percentage of the home's purchased value. Must be between 0 and 0.25.
- `delete_excel_file` (bool): A boolean value representing if you want the excel file deleted after it has been created (`true`) or not (`false`). This should help prevent the files from building up if you are having them emailed. Must be `true` or `false`.
- `send_emails` (bool): A boolean value representing if you want to receive an email containing all excel file (`true`) or not (`false`). An excel file will be generated, regardless of if an email is requested. Must be `true` or `false`.
- `email_receiver_address` (str): A string containing the email address of the intended receiver of the house analysis email.
- `email_sender_address` (str): A string containing the email address of the sender of the house analysis email.
- `email_2FA_password` (str): A string containing the Gmail 2 factor authenticication password.

TODO: Finish this section
## Features

List the key features of your project. What makes it stand out?

TODO: Finish this section
## Contributing

If you're open to contributions, explain how others can contribute to your project. Outline the process they should follow.

1. Fork the Project
2. Create your Feature Branch (git checkout -b feature/AmazingFeature)
3. Commit your Changes (git commit -m 'Add some AmazingFeature')
4. Push to the Branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

TODO: Finish this section
## Credits

Acknowledge those who contributed to the project.

TODO: Finish this section
## License

State the license under which your project is released, and include a link to the license text.

Distributed under the MIT License. See LICENSE for more information.
