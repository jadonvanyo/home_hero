import unittest
from analysis_functions import config_file_required_values_present, config_file_required_email_values_present

# TODO: Add additional tests
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
        self.assertEqual(config_file_required_values_present(config), [])

    def test_invalid_scrapeops_api_key(self):
        """Test case where there is an invalid Scrapeops API key."""
        config = {
            "scrapeops_api_key": "a" * 36, # Invalid API key given
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
        self.assertEqual(config_file_required_values_present(config), ["Invalid API Key entered, please enter a valid API Key in `config.json`."])

    def test_empty_scrapeops_api_key_value(self):
        """Test case where one value is empty."""
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
        self.assertEqual(config_file_required_values_present(config), ['"scrapeops_api_key" is incorrectly entered in the config file. Review documentation for how to enter "scrapeops_api_key".'])

    def test_missing_scrapeops_api_key(self):
        """Test case where the Scrapeops API key is missing."""
        config = {
            # Omitting "scrapeops_api_key"
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
        self.assertEqual(config_file_required_values_present(config), ['"scrapeops_api_key" is not in the config file. Please enter "scrapeops_api_key" in the config file.'])

    def test_incorrect_value_type(self):
        """Test case where one value has an incorrect type."""
        config = {
            "scrapeops_api_key": "d875dca3-61b5-4126-9181-24e588fe58d3",
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
        self.assertEqual(config_file_required_values_present(config), ['"starturls" is incorrectly entered in the config file. Review documentation for how to enter "starturls".'])
        
    def test_incorrect_value_type_2(self):
        """Test case where two values have an incorrect type."""
        config = {
            "scrapeops_api_key": "d875dca3-61b5-4126-9181-24e588fe58d3",
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
        self.assertEqual(config_file_required_values_present(config), ['"closing_cost_buyer_decimal" is incorrectly entered in the config file. Review documentation for how to enter "closing_cost_buyer_decimal".', '"loan_term_yrs" is incorrectly entered in the config file. Review documentation for how to enter "loan_term_yrs".'])
        
    def test_scrapeops_api_key_incorrect_value(self):
        """Test case where scrapeops_api_key value is outside of the boundary."""
        config = {
            "scrapeops_api_key": "thisistooshort", # scrapeops api key outside of value boundary
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
        self.assertEqual(config_file_required_values_present(config), ['"scrapeops_api_key" is incorrectly entered in the config file. Review documentation for how to enter "scrapeops_api_key".', 'Invalid API Key entered, please enter a valid API Key in `config.json`.'])

class TestConfigFileRequiredEmailValuesPresent(unittest.TestCase):
    
    def test_all_values_correct(self):
        """Test case where all config email values are correct."""
        config = {
            "send_emails": True,
            "email_sender_address": "sender.example@gmail.com",
            "email_receiver_address": "reciver.example@gmail.com",
            "email_2FA_password": "example_password",
            "send_error_emails": False,
            "featured_house_required": True,
            "target_cash_flow_monthly_min": -200,
            "target_percent_rule_min": None,
            "target_net_operating_income_min": None,
            "target_pro_forma_cap_min": None,
            "target_five_year_annualized_return_min": 0.1,
            "target_cash_on_cash_return_min": None
        }
        self.assertEqual(config_file_required_email_values_present(config), [])
        
    def test_missing_email_password(self):
        """Test case where one of the main values is missing."""
        config = {
            "send_emails": True,
            "email_sender_address": "sender.example@gmail.com",
            "email_receiver_address": "reciver.example@gmail.com",
            # email password has been omitted
            "send_error_emails": False,
            "featured_house_required": True,
            "target_cash_flow_monthly_min": -200,
            "target_percent_rule_min": None,
            "target_net_operating_income_min": None,
            "target_pro_forma_cap_min": None,
            "target_five_year_annualized_return_min": 0.1,
            "target_cash_on_cash_return_min": None
        }
        self.assertEqual(config_file_required_email_values_present(config), ['"email_2FA_password" is not in the config file. Please enter "email_2FA_password" in the config file.'])

    def test_send_emails_false_errors_after(self):
        """Test case where send_emails is false and there are additional errors afterwards that do not need to be detected."""
        config = {
            "send_emails": False,
            "email_sender_address": "sender.example@gmail.com",
            "email_receiver_address": "reciver.example@gmail.com",
            # email password has been omitted
            "send_error_emails": False,
            "featured_house_required": True,
            "target_cash_flow_monthly_min": -200,
            "target_percent_rule_min": "None", # This is the wrong type
            "target_net_operating_income_min": None,
            "target_pro_forma_cap_min": None,
            "target_five_year_annualized_return_min": 25, # This is out of the value range
            "target_cash_on_cash_return_min": None
        }
        self.assertEqual(config_file_required_email_values_present(config), [])
        
    def test_one_incorrect_target_value_type(self):
        """Test case where one of the target values is the wrong type."""
        config = {
            "send_emails": True,
            "email_sender_address": "sender.example@gmail.com",
            "email_receiver_address": "reciver.example@gmail.com",
            "email_2FA_password": "example_password",
            "send_error_emails": False,
            "featured_house_required": True,
            "target_cash_flow_monthly_min": -200,
            "target_percent_rule_min": "None", # This is the wrong type
            "target_net_operating_income_min": None,
            "target_pro_forma_cap_min": None,
            "target_five_year_annualized_return_min": 0.1,
            "target_cash_on_cash_return_min": None
        }
        self.assertEqual(config_file_required_email_values_present(config), ['"target_percent_rule_min" was entered incorrectly in the config file. Refer to the documentation on how to enter "target_percent_rule_min".'])
        
    def test_missing_target_value(self):
        """Test case where one of the target values is the wrong type."""
        config = {
            "send_emails": True,
            "email_sender_address": "sender.example@gmail.com",
            "email_receiver_address": "reciver.example@gmail.com",
            "email_2FA_password": "example_password",
            "send_error_emails": False,
            "featured_house_required": True,
            "target_cash_flow_monthly_min": None,
            # Target percent rule min has been omitted
            "target_net_operating_income_min": None,
            "target_pro_forma_cap_min": None,
            "target_five_year_annualized_return_min": 0.1,
            "target_cash_on_cash_return_min": None
        }
        self.assertEqual(config_file_required_email_values_present(config), [])
        
    def test_no_target_values(self):
        """Test case where a featured house is requested, but no target values are given."""
        config = {
            "send_emails": True,
            "email_sender_address": "sender.example@gmail.com",
            "email_receiver_address": "reciver.example@gmail.com",
            "email_2FA_password": "example_password",
            "send_error_emails": False,
            "featured_house_required": True,
            "target_cash_flow_monthly_min": None,
            "target_percent_rule_min": None,
            "target_net_operating_income_min": None,
            "target_pro_forma_cap_min": None,
            "target_five_year_annualized_return_min": None,
            "target_cash_on_cash_return_min": None
        }
        self.assertEqual(config_file_required_email_values_present(config), ["'featured_house_required' was selected, but no target values were established. Refer to the documentation on how to use 'featured_house_required'."])
        
    def test_all_target_values_missing(self):
        """Test case where a featured house is requested, but all target values are missing."""
        config = {
            "send_emails": True,
            "email_sender_address": "sender.example@gmail.com",
            "email_receiver_address": "reciver.example@gmail.com",
            "email_2FA_password": "example_password",
            "send_error_emails": False,
            "featured_house_required": True,
            # All the target values are missing
        }
        self.assertEqual(config_file_required_email_values_present(config), ["'featured_house_required' was selected, but no target values were established. Refer to the documentation on how to use 'featured_house_required'."])
        
    def test_two_target_values_out_bounds_values(self):
        """Test case where two of the target values are outside of the set boundaries."""
        config = {
            "send_emails": True,
            "email_sender_address": "sender.example@gmail.com",
            "email_receiver_address": "reciver.example@gmail.com",
            "email_2FA_password": "example_password",
            "send_error_emails": False,
            "featured_house_required": True,
            "target_cash_flow_monthly_min": None,
            "target_percent_rule_min": 3,
            "target_net_operating_income_min": None,
            "target_pro_forma_cap_min": None,
            "target_five_year_annualized_return_min": 15,
            "target_cash_on_cash_return_min": None
        }
        self.assertEqual(config_file_required_email_values_present(config), ['"target_percent_rule_min" was entered incorrectly in the config file. Refer to the documentation on how to enter "target_percent_rule_min".', '"target_five_year_annualized_return_min" was entered incorrectly in the config file. Refer to the documentation on how to enter "target_five_year_annualized_return_min".'])
        
    def test_all_values_correct(self):
        """Test case where featured house variable is missing."""
        config = {
            "send_emails": True,
            "email_sender_address": "sender.example@gmail.com",
            "email_receiver_address": "reciver.example@gmail.com",
            "email_2FA_password": "example_password",
            "send_error_emails": False,
            # featured_house_required is missing
            "target_cash_flow_monthly_min": -200,
            "target_percent_rule_min": None,
            "target_net_operating_income_min": None,
            "target_pro_forma_cap_min": None,
            "target_five_year_annualized_return_min": 0.1,
            "target_cash_on_cash_return_min": None
        }
        self.assertEqual(config_file_required_email_values_present(config), ['"featured_house_required" is not in the config file. Please enter "featured_house_required" in the config file.'])
        
if __name__ == '__main__':
    unittest.main()
