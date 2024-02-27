# Home Hero

This project will scrape homes from Zillow based on a given Zillow URL and analyze these home's investment potential based on the user's input. The analyzed homes will be given to the user as an Excel file that can be accessed via the project folder or emailed directly to the user. This project was made due to me and some pf my friends spending hours each week looking for and analyzing houses on the MLS. This project takes a process that used to take a few hours each week down to a few minutes.

## Table of Contents

- [Background](#background)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
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
- `twisted`: For asynchronous networking. The project uses Twisted's reactor and defer modules.
- `tabulate`: For pretty-printing tabular data in HTML format.
- `smtplib` and `email.mime`: For sending emails with attachments.
- `os`, `json`, `asyncio`: For various utility functions such as file handling, JSON parsing, and asynchronous programming.

You can use the following pip command to install the required Python packages:

```bash
pip install openpyxl scrapy twisted tabulate
```

This project also requires a scrapeops API key that can be obtained for free [here](https://scrapeops.io/). Just create a free account and copy and paste your scrapeops API key into the configuration file.

## Installation

Provide detailed instructions on how to install your project. Include any prerequisites, libraries, or third-party tools that are needed.

```bash
git clone https://yourproject.git
cd yourproject
./install.sh
```

## Usage

Explain how to use your project. Include code blocks and examples for common use cases.

## Features

List the key features of your project. What makes it stand out?

## Contributing

If you're open to contributions, explain how others can contribute to your project. Outline the process they should follow.

1. Fork the Project
2. Create your Feature Branch (git checkout -b feature/AmazingFeature)
3. Commit your Changes (git commit -m 'Add some AmazingFeature')
4. Push to the Branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

## Credits

Acknowledge those who contributed to the project.

## License

State the license under which your project is released, and include a link to the license text.

Distributed under the MIT License. See LICENSE for more information.