import unittest
from analysis_functions import config_file_required_values_present

class TestConfigFileRequiredValuesPresent(unittest.TestCase):

    def test_all_values_correct(self):
        """Test case where all config values are correct."""
        config = {
            "scrapeops_api_key": "d875dca3-61b5-4126-9181-24e588fe58d3",
            "starturls": ["https://www.zillow.com/fort-lauderdale-fl/duplex/"],
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
            "delete_excel_file": False,
            "send_emails": False,
        }
        self.assertTrue(config_file_required_values_present(config))

    def test_invalid_scrapeops_api_key(self):
        """Test case where there is an invalid Scrapeops API key."""
        config = {
            "scrapeops_api_key": "a" * 36,
            "starturls": ["https://www.zillow.com/fort-lauderdale-fl/duplex/"],
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
            "delete_excel_file": False,
            "send_emails": False,
        }
        self.assertFalse(config_file_required_values_present(config))

    def test_empty_value(self):
        """Test case where one value is missing."""
        config = {
            "scrapeops_api_key": "", # Empty scrapeops api key
            "starturls": ["https://www.zillow.com/fort-lauderdale-fl/duplex/"],
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
            "delete_excel_file": False,
            "send_emails": False,
        }
        self.assertFalse(config_file_required_values_present(config))

    def test_missing_value(self):
        """Test case where one value is missing."""
        config = {
            # Omitting "scrapeops_api_key" to simulate a missing value
            "starturls": ["https://www.zillow.com/fort-lauderdale-fl/duplex/"],
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
            "delete_excel_file": False,
            "send_emails": False,
        }
        self.assertFalse(config_file_required_values_present(config))

    def test_incorrect_value_type(self):
        """Test case where one value has an incorrect type."""
        config = {
            "scrapeops_api_key": "4aac8234-0r08-4286-345f-91878b766e57",
            "starturls": "https://www.zillow.com/fort-lauderdale-fl/duplex/",  # Incorrect type: should be a list
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
            "delete_excel_file": False,
            "send_emails": False,
        }
        self.assertFalse(config_file_required_values_present(config))
        
    def test_incorrect_value_type_2(self):
        """Test case where two values have an incorrect type."""
        config = {
            "scrapeops_api_key": "4aac8234-0r08-4286-345f-91878b766e57",
            "starturls": ["https://www.zillow.com/fort-lauderdale-fl/duplex/"],
            "down_payment_decimal": 0.12, 
            "closing_cost_buyer_decimal": 'taco', # enter a string
            "closing_cost_seller_decimal": 0.08,
            "expected_annual_growth": 0.02,
            "interest_rate": 0.06,
            "loan_term_yrs": '30', # enter the number as a string
            "expected_repairs_monthly": 0.05,
            "expected_vacancy_monthly": 0.09,
            "expected_capx_monthly": 0.1,
            "expected_management_monthly": 0.1,
            "insurance_rate_yearly": 0.006,
            "delete_excel_file": False,
            "send_emails": False,
        }
        self.assertFalse(config_file_required_values_present(config))

if __name__ == '__main__':
    unittest.main()
