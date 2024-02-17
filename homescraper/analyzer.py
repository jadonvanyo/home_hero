import json

# Global variables for analysis
closing_cost_buyer_decimal = 0.03 # Usually between 0.02 and 0.05
closing_cost_seller_decimal = 0.08 # Usually between 0.06 and 0.10
expected_annual_growth = 0.02
down_payment_decimal = 0.12
interest_rate = 0.06
loan_term_yrs = 30
expected_repairs_monthly = 0.05 # Usually between 0.04 and 0.08
expected_vacancy_monthly = 0.09 # Usually between 0.06 and 0.12 (3-6 weeks per year)
expected_capx_monthly = 0.1 # Usually between 0.08 and 0.12
expected_management_monthly = 0.1 # Usually between 0.9 and 0.12
insurance_rate_yearly = 0.006 # Usually between 0.005 and 0.01

# Create a list to store all the analyzed homes
analyzed_homes = []

# TODO: Create a class for each analyzed home

# Get all of the house data from homedata.json
with open('homedata.json') as file:
    data = json.load(file)

# Check if there are any houses in the list pulled
if not data:
    print("No houses found")
    
else:
    # Loop through each of the houses in the dataset
    for house in data:
        # Calculate the price per sqft
        price_per_sqft = round(int(house.get('price')) / int(house.get('sqft')), 2)
        print(f'Price per sqft: {price_per_sqft}')
        
        # Calculate the monthly insurance
        insurance_monthly = round(((int(house.get('price')) * insurance_rate_yearly) / 12), 2)
        print(f'Monthly insurance: {insurance_monthly}')
        
        # Calculate the down payment needed
        down_payment_cost = int(house.get('price')) * down_payment_decimal
        print(f'Down payment: {down_payment_cost}')
        
        # Calculate the loan needed
        loan = int(house.get('price')) - float(down_payment_cost)
        print(f'Loan: {loan}')
        
        # Calculate the closing costs required
        closing_costs = int(house.get('price')) * closing_cost_buyer_decimal
        print(f'Closing costs: {closing_costs}')
        
        # Calculate the monthly principle and interest payments
        principle_interest_monthly = round((loan * (interest_rate / 12) * (1 + interest_rate / 12) ** (loan_term_yrs * 12)) / ((1 + interest_rate / 12) ** (loan_term_yrs * 12) - 1), 2)
        print(f'Monthly principle and interest: {principle_interest_monthly}')
        
        # Calculate the monthly taxes
        taxes_monthly = round(int(house.get('tax')) / 12, 2)
        print(f'Monthly taxes: {taxes_monthly}')
        
        # Calculate the operating costs
        total_operating_costs_monthly = round(principle_interest_monthly + taxes_monthly + insurance_monthly, 2)
        print(f'Total operating costs: {total_operating_costs_monthly}')
        
        # Determine how many units are contained in the property
        property_subtypes = {
            'duplex': 2,
            'triplex': 3,
            'quadplex': 4,
            'quinplex': 5
        }

        property_subtype = house.get('property_subtype')
        number_units = property_subtypes.get(property_subtype, 1)
        print(f'Number of units {number_units}')
            
        # Calculate the suggested total rent for the unit
        suggested_total_rent_monthly = round(number_units * float(house.get('rent')), 2)
        print(f'Suggested total monthly rent {suggested_total_rent_monthly}')
        
        # Calculate the monthly repair expenses
        total_repairs_monthly = round(suggested_total_rent_monthly * expected_repairs_monthly, 2)
        print(f'Expected monthly repairs {total_repairs_monthly}')
        
        # Calculate the monthly capital expenditures
        total_capx_monthly = round(suggested_total_rent_monthly * expected_capx_monthly, 2)
        print(f'Expected monthly capx {total_capx_monthly}')
        
        # Calculate the monthly expected vacancy
        total_vacancy_monthly = round(suggested_total_rent_monthly * expected_vacancy_monthly, 2)
        print(f'Expected monthly vacancy {total_vacancy_monthly}')
        
        # Calculate the monthly expected management fees
        total_management_monthly = round(suggested_total_rent_monthly * expected_management_monthly, 2)
        print(f'Expected monthly management {total_management_monthly}')
        
        # Calculate the total amount of monthly expanses
        total_expenses_monthly = total_operating_costs_monthly + total_repairs_monthly + total_capx_monthly + total_vacancy_monthly + total_management_monthly
        print(f'Expected monthly expenses {total_expenses_monthly}')
        
        # Calculate the total expected monthly cash flow
        cash_flow_monthly = round(suggested_total_rent_monthly - total_expenses_monthly, 2)
        print(f'Expected monthly cash flow {cash_flow_monthly}')
        
        # Calculate the expected cash flow from the 50% rule
        cash_flow_50 = round(suggested_total_rent_monthly / 2 - principle_interest_monthly, 2)
        print(f'Expected cash from from 50% rule {cash_flow_50}')
        
        # Calculate the total cash needed to complete the deal
        cash_needed_total = down_payment_cost + closing_costs
        print(f'Total amount of cash needed {cash_needed_total}')
        
        # Calculate the cash on cash return for the property
        cash_on_cash_decimal = round(suggested_total_rent_monthly / cash_needed_total, 4)
        print(f'Cash on cash return {cash_on_cash_decimal * 100}')
        
        # Calculate the 1% rule
        percent_rule_decimal = round(suggested_total_rent_monthly / float(house.get('price')), 4)
        print(f'1% Rule {percent_rule_decimal * 100}')
        
        # Calculate the Net Operating Income
        net_operating_income = suggested_total_rent_monthly * 12 - (taxes_monthly + insurance_monthly + total_repairs_monthly + + total_capx_monthly + total_vacancy_monthly + total_management_monthly) * 12
        print(f'NOI {net_operating_income}')
        
        # Calculate the pro forma cap
        pro_forma_cap_decimal = round(net_operating_income / float(house.get('price')), 4)
        print(f'Pro Forma Cap {pro_forma_cap_decimal * 100}')
        
        # Declare lists for the property value, equity, loan balance, rent_growth, cashflow, profit if sold, and annualized return
        property_value = []
        loan_balance = []
        equity = []
        rent_growth = []
        profit_if_sold = []
        cash_flow_yearly = []
        annualized_return_percent = []
        
        # Loop though all the years of the loan term to determine yearly statistics of the property
        for x in range(loan_term_yrs + 1):
            property_value.append(round(float(house.get('price')) * (1 + expected_annual_growth) ** x, 2))
            loan_balance.append(round((principle_interest_monthly / (interest_rate / 12)) * (1 - (1 / ((1 + interest_rate / 12) ** (loan_term_yrs * 12 - x * 12)))), 2))
            equity.append(round(property_value[x] - loan_balance[x], 2))
            rent_growth.append(round(suggested_total_rent_monthly * (1 + expected_annual_growth) ** x, 2))
            profit_if_sold.append(round(property_value[x] * (1 - closing_cost_seller_decimal) + sum(cash_flow_yearly) - cash_needed_total - loan_balance[x], 2))
            cash_flow_yearly.append(round((rent_growth[x] * (1 - expected_repairs_monthly - expected_vacancy_monthly - expected_capx_monthly - expected_management_monthly) - (1 + expected_annual_growth) ** x * (insurance_monthly + taxes_monthly) - principle_interest_monthly)  * 12, 2))
            annualized_return_percent.append(round((((profit_if_sold[x] + cash_needed_total) / cash_needed_total) ** (1 / (x + 1)) - 1) * 100, 2))
            
        print(f'Property values: {property_value}')
        print(f'Loan Balance: {loan_balance}')
        print(f'Rent Growth: {rent_growth}')
        print(f'Equity: {equity}')
        print(f'Profit if sold: {profit_if_sold}')
        print(f'Yearly Cash Flow: {cash_flow_yearly}')
        print(f'Annualized Return:{annualized_return_percent}')
        
        