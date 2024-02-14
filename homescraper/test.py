import json

class House:
    def __init__(
            self, 
            data, 
            down_payment_decimal=0.12, 
            closing_cost_buyer_decimal=0.03, # Usually between 0.02 and 0.05
            closing_cost_seller_decimal=0.08, # Usually between 0.06 and 0.10
            expected_annual_growth=0.02,
            interest_rate=0.06,
            loan_term_yrs=30,
            expected_repairs_monthly=0.05, # Usually between 0.04 and 0.08
            expected_vacancy_monthly=0.09, # Usually between 0.06 and 0.12 (3-6 weeks per year)
            expected_capx_monthly=0.1, # Usually between 0.08 and 0.12
            expected_management_monthly=0.1, # Usually between 0.9 and 0.12
            insurance_rate_yearly=0.006, # Usually between 0.005 and 0.01
        ):
        self.price = float(data.get('price'))
        self.sqft = float(data.get('sqft'))
        self.tax = float(data.get('tax'))
        self.rent = float(data.get('rent'))
        self.property_subtype = data.get('property_subtype')
        self.address = data.get('address')
        self.beds = data.get('beds')
        self.baths = data.get('baths')
        self.description = data.get('description')
        self.year_built = data.get('year_built')
        self.region = data.get('region')
        self.subdivision = data.get('subdivision')
        self.tax_url = data.get('tax_url')
        self.rent_url = data.get('rent_url')
        self.url = data.get('url')
        self.min_rent = data.get('min_rent')
        self.max_rent = data.get('max_rent')
        self.down_payment_decimal = down_payment_decimal
        self.closing_cost_buyer_decimal = closing_cost_buyer_decimal
        self.closing_cost_seller_decimal = closing_cost_seller_decimal
        self.expected_annual_growth = expected_annual_growth
        self.interest_rate = interest_rate
        self.loan_term_yrs = loan_term_yrs
        self.expected_repairs_monthly = expected_repairs_monthly
        self.expected_vacancy_monthly = expected_vacancy_monthly
        self.expected_capx_monthly = expected_capx_monthly
        self.expected_management_monthly = expected_management_monthly
        self.insurance_rate_yearly = insurance_rate_yearly
        self.calculate_metrics()

    def calculate_metrics(self):
        """Calculate all the necessary information to analyze a house"""
        # Calculate the price per sqft
        self.price_per_sqft = round(self.price / self.sqft, 2)
        
        # Calculate the monthly insurance
        self.insurance_monthly = round((self.price * self.insurance_rate_yearly) / 12, 2)
        
        # Calculate the down payment needed
        self.down_payment_cost = round(self.price * self.down_payment_decimal, 2)
        
        # Calculate the loan needed
        self.loan = self.price - self.down_payment_cost
        
        # Calculate the closing costs required
        self.closing_costs = self.price * self.closing_cost_buyer_decimal
        
        # Calculate the monthly principle and interest payments
        self.principle_interest_monthly = round((self.loan * (self.interest_rate / 12) * (1 + self.interest_rate / 12) ** (self.loan_term_yrs * 12)) / ((1 + self.interest_rate / 12) ** (self.loan_term_yrs * 12) - 1), 2)
        
        # Calculate the monthly taxes
        self.taxes_monthly = round(self.tax / 12, 2)
        
        # Calculate the operating costs
        self.total_operating_costs_monthly = round(self.principle_interest_monthly + self.taxes_monthly + self.insurance_monthly, 2)
        
        # Determine how many units are contained in the property
        property_subtypes = {
            'duplex': 2,
            'triplex': 3,
            'quadplex': 4,
            'quinplex': 5
        }

        self.number_units = property_subtypes.get(self.property_subtype, 1)
            
        # Calculate the suggested total rent for the unit
        self.suggested_total_rent_monthly = round(self.number_units * self.rent, 2)
        
        # Calculate the monthly repair expenses
        self.total_repairs_monthly = round(self.suggested_total_rent_monthly * self.expected_repairs_monthly, 2)
        
        # Calculate the monthly capital expenditures
        self.total_capx_monthly = round(self.suggested_total_rent_monthly * self.expected_capx_monthly, 2)
        
        # Calculate the monthly expected vacancy
        self.total_vacancy_monthly = round(self.suggested_total_rent_monthly * self.expected_vacancy_monthly, 2)
        
        # Calculate the monthly expected management fees
        self.total_management_monthly = round(self.suggested_total_rent_monthly * self.expected_management_monthly, 2)
        
        # Calculate the total amount of monthly expanses
        self.total_expenses_monthly = self.total_operating_costs_monthly + self.total_repairs_monthly + self.total_capx_monthly + self.total_vacancy_monthly + self.total_management_monthly
        
        # Calculate the total expected monthly cash flow
        self.cash_flow_monthly = round(self.suggested_total_rent_monthly - self.total_expenses_monthly, 2)
        
        # Calculate the expected cash flow from the 50% rule
        self.cash_flow_50 = round(self.suggested_total_rent_monthly / 2 - self.principle_interest_monthly, 2)
        
        # Calculate the total cash needed to complete the deal
        self.cash_needed_total = self.down_payment_cost + self.closing_costs
        
        # Calculate the cash on cash return for the property
        self.cash_on_cash_decimal = round(self.suggested_total_rent_monthly / self.cash_needed_total, 4)
        
        # Calculate the 1% rule
        self.percent_rule_decimal = round(self.suggested_total_rent_monthly / self.price, 4)
        
        # Calculate the Net Operating Income
        self.net_operating_income = self.suggested_total_rent_monthly * 12 - (self.taxes_monthly + self.insurance_monthly + self.total_repairs_monthly + + self.total_capx_monthly + self.total_vacancy_monthly + self.total_management_monthly) * 12
        
        # Calculate the pro forma cap
        self.pro_forma_cap_decimal = round(self.net_operating_income / self.price, 4)
        
        # Declare lists for the property value, equity, loan balance, rent_growth, cashflow, profit if sold, and annualized return
        self.property_value = []
        self.loan_balance = []
        self.equity = []
        self.rent_growth = []
        self.profit_if_sold = []
        self.cash_flow_yearly = []
        self.annualized_return_percent = []
        
        # Loop though all the years of the loan term to determine yearly statistics of the property
        for x in range(self.loan_term_yrs + 1):
            self.property_value.append(round(self.price * (1 + self.expected_annual_growth) ** x, 2))
            self.loan_balance.append(round((self.principle_interest_monthly / (self.interest_rate / 12)) * (1 - (1 / ((1 + self.interest_rate / 12) ** (self.loan_term_yrs * 12 - x * 12)))), 2))
            self.equity.append(round(self.property_value[x] - self.loan_balance[x], 2))
            self.rent_growth.append(round(self.suggested_total_rent_monthly * (1 + self.expected_annual_growth) ** x, 2))
            self.profit_if_sold.append(round(self.property_value[x] * (1 - self.closing_cost_seller_decimal) + sum(self.cash_flow_yearly) - self.cash_needed_total - self.loan_balance[x], 2))
            self.cash_flow_yearly.append(round((self.rent_growth[x] * (1 - self.expected_repairs_monthly - self.expected_vacancy_monthly - self.expected_capx_monthly - self.expected_management_monthly) - (1 + self.expected_annual_growth) ** x * (self.insurance_monthly + self.taxes_monthly) - self.principle_interest_monthly)  * 12, 2))
            self.annualized_return_percent.append(round((((self.profit_if_sold[x] + self.cash_needed_total) / self.cash_needed_total) ** (1 / (x + 1)) - 1) * 100, 2))
            
            # TODO: Create a method to present a featured home in an email
            # TODO: Create a method to determine if a home should be a feature home
            # TODO: Create a method to store all the house information in a json or csv

# Create a list to store all the analyzed homes
analyzed_homes = []

# Get all of the house data from homedata.json
with open('homedata.json') as file:
    data = json.load(file)

# Check if there are any houses in the list pulled
if not data:
    print("No houses found")
    
else:
    # Loop through each of the houses in the dataset
    for house_data in data:
        house = House(house_data)
        analyzed_homes.append(house)

        print(f'Price per sqft: {house.price_per_sqft}')
        print(f'Monthly insurance: {house.insurance_monthly}')
        print(f'Yearly cash flow: {house.cash_flow_yearly}')
        # Access other calculated metrics directly from the House object

