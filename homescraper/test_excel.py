from datetime import date
import json
import pandas as pd
import openpyxl
import smtplib, ssl
from tabulate import tabulate

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
        self.year = []
        self.property_value = []
        self.loan_balance = []
        self.equity = []
        self.rent_growth = []
        self.profit_if_sold = []
        self.cash_flow_yearly = []
        self.annualized_return_percent = []
        
        # Loop though all the years of the loan term to determine yearly statistics of the property
        for x in range(self.loan_term_yrs + 1):
            self.year.append(x)
            self.property_value.append(round(self.price * (1 + self.expected_annual_growth) ** x, 2))
            self.loan_balance.append(round((self.principle_interest_monthly / (self.interest_rate / 12)) * (1 - (1 / ((1 + self.interest_rate / 12) ** (self.loan_term_yrs * 12 - x * 12)))), 2))
            self.equity.append(round(self.property_value[x] - self.loan_balance[x], 2))
            self.rent_growth.append(round(self.suggested_total_rent_monthly * (1 + self.expected_annual_growth) ** x, 2))
            self.profit_if_sold.append(round(self.property_value[x] * (1 - self.closing_cost_seller_decimal) + sum(self.cash_flow_yearly) - self.cash_needed_total - self.loan_balance[x], 2))
            self.cash_flow_yearly.append(round((self.rent_growth[x] * (1 - self.expected_repairs_monthly - self.expected_vacancy_monthly - self.expected_capx_monthly - self.expected_management_monthly) - (1 + self.expected_annual_growth) ** x * (self.insurance_monthly + self.taxes_monthly) - self.principle_interest_monthly)  * 12, 2))
            self.annualized_return_percent.append(round((((self.profit_if_sold[x] + self.cash_needed_total) / self.cash_needed_total) ** (1 / (x + 1)) - 1) * 100, 2))
            
            
    def email_format_html(self):
        """Method to load all the required information into HTMl format for an email"""
        # Add all the appropriate labels and rows for the table
        formatted_table_data = [
            ['Year'] + self.year[:6],
            ['Property Value'] + self.property_value[:6],
            ['Loan Balance'] + self.loan_balance[:6],
            ['Equity'] + self.equity[:6],
            ['Expected Rents'] + self.rent_growth[:6],
            ['Profit if Sold'] + self.profit_if_sold[:6],
            ['Yearly Cash Flow'] + self.cash_flow_yearly[:6],
            ['Annualized Return'] + self.annualized_return_percent[:6]
        ]
        
        # Turn all the table data into HTML format
        yearly_statistics_table_html = tabulate(formatted_table_data, tablefmt='html')
        
        house_email_html = f"""
            <div>
                <h4>
                    <a href="{self.url}">{self.address}</a>
                </h4>
                <ul>
                    <li>Price: ${self.price}</li>
                    <li>Type: {self.property_subtype}</li>
                    <li>Layout: Beds: {self.beds} Baths: {self.baths} SQFT: {self.sqft} sqft</li>
                    <li>Price per SQFT: {self.price_per_sqft}</li>
                    <li>Estimated Monthly Rent: <a href="{self.rent_url}">${self.suggested_total_rent_monthly}</a></li>
                    <li>Monthly Operating Expenses: ${self.total_operating_costs_monthly}</li>
                    <li>Total Monthly Expenses: ${self.total_expenses_monthly}</li>
                    <li>Monthly Cash Flow: ${self.cash_flow_monthly}</li>
                    <li>1% Rule: {self.percent_rule_decimal * 100}%</li>
                    <li>50% Rule Cash Flow: ${self.cash_flow_50}</li>
                    <li>Estimated Total Cash Needed: ${self.cash_needed_total}</li>
                </ul>
                <h6>First 5 years yearly breakdown</h6>
                {yearly_statistics_table_html}
                <p>Description: {self.description}</p>
            </div>
        """
        
        return house_email_html
    
    
    def email_format_plain(self):
        """Method to load all the required information into a plain text format for email"""
        
        house_email_plain = f"""
            Link: {self.url}
            Address: {self.address}
            Price: ${self.price}
            Type: {self.property_subtype}
            Layout: Beds: {self.beds} Baths: {self.baths} SQFT: {self.sqft} sqft
            Price per SQFT: {self.price_per_sqft}
            Estimated Monthly Rent: ${self.suggested_total_rent_monthly}
            Rent URL: {self.rent_url}
            Monthly Operating Expenses: ${self.total_operating_costs_monthly}
            Total Monthly Expenses: ${self.total_expenses_monthly}
            Monthly Cash Flow: ${self.cash_flow_monthly}
            1% Rule: {self.percent_rule_decimal * 100}%
            50% Rule Cash Flow: ${self.cash_flow_50}
            Estimated Total Cash Needed: ${self.cash_needed_total}
            First 5 years yearly breakdown:
            {['Year'] + self.year[:6]}
            {['Property Value'] + self.property_value[:6]}
            {['Loan Balance'] + self.loan_balance[:6]}
            {['Equity'] + self.equity[:6]}
            {['Expected Rents'] + self.rent_growth[:6]}
            {['Profit if Sold'] + self.profit_if_sold[:6]}
            {['Yearly Cash Flow'] + self.cash_flow_yearly[:6]}
            {['Annualized Return'] + self.annualized_return_percent[:6]}
            Description: {self.description}
        """
        
        return house_email_plain
    # TODO: Create a method to determine if a home should be a feature home
    # TODO: Create a method to create pandas data frames for the data
    def house_pd_df(self):
        """Create a pandas data frame with the required structure to populate an excel sheet"""
        # Create an empty DataFrame with the desired structure
        # index=range(1, 34), columns=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        df = pd.DataFrame()
        
        # Populate the DataFrame with house values
        df.at[1, 'A'] = 'Address'
        df.at[3, 'A'] = 'Purchase Price'
        df.at[4, 'A'] = 'Closing Costs'
        df.at[5, 'A'] = 'Closing Costs (%)'
        df.at[6, 'A'] = 'Annual Growth'
        df.at[8, 'A'] = 'Loan'
        df.at[9, 'A'] = 'Downpayment (%)'
        df.at[10, 'A'] = 'Downpayment ($)'
        df.at[11, 'A'] = 'Loan'
        df.at[12, 'A'] = 'Interest Rate (%)'
        df.at[13, 'A'] = 'Loan Term (Yrs)'
        df.at[14, 'A'] = 'Monthly Payment'
        df.at[16, 'A'] = 'Rental Income'
        df.at[17, 'A'] = 'Rent'
        df.at[19, 'A'] = 'Expenses'
        df.at[20, 'A'] = 'Property Taxes (mo)'
        df.at[21, 'A'] = 'Insurance (mo)'
        df.at[22, 'A'] = 'Repairs (%-mo)'
        df.at[23, 'A'] = 'Vacancy (%-mo)'
        df.at[24, 'A'] = 'Capital Expenses (%-mo)'
        df.at[25, 'A'] = 'Management Fees (%-mo)'
        df.at[27, 'A'] = 'Year'
        df.at[28, 'A'] = 'Property Value'
        df.at[29, 'A'] = 'Equity'
        df.at[30, 'A'] = 'Loan Balance'
        df.at[31, 'A'] = 'Rent'
        df.at[32, 'A'] = 'Cash Flow'
        df.at[33, 'A'] = 'Profit If Sold'
        df.at[34, 'A'] = 'Annualized Return'
        df.at[1, 'B'] = self.address
        df.at[3, 'B'] = self.price
        df.at[4, 'B'] = '=B5*B3'
        df.at[5, 'B'] = self.closing_cost_buyer_decimal
        df.at[6, 'B'] = self.expected_annual_growth
        df.at[9, 'B'] = self.down_payment_decimal
        df.at[10, 'B'] = '=B3*B9'
        df.at[11, 'B'] = '=B3-B10'
        df.at[12, 'B'] = self.interest_rate
        df.at[13, 'B'] = self.loan_term_yrs
        df.at[14, 'B'] = '=(B11*(B12/12)*(1+B12/12)^(B13*12))/((1+B12/12)^(B13*12)-1)'
        df.at[17, 'B'] = self.suggested_total_rent_monthly
        df.at[20, 'B'] = self.taxes_monthly
        df.at[21, 'B'] = self.insurance_monthly
        df.at[22, 'B'] = self.total_repairs_monthly
        df.at[23, 'B'] = self.total_vacancy_monthly
        df.at[24, 'B'] = self.total_capx_monthly
        df.at[25, 'B'] = self.total_management_monthly
        df.at[27, 'B'] = 0
        df.at[28, 'B'] = '=B3*(1+B6)^B27'
        df.at[29, 'B'] = '=B28-B30'
        df.at[30, 'B'] = '=B3-B10'
        df.at[31, 'B'] = '=(B17*(1+B6)^B27)'
        df.at[32, 'B'] = '=(B31-B31*B22-B31*B23-B31*B24-B31*B25-B21*(1+B6)^B27-B20*(1+B6)^B27-B14)*12'
        df.at[33, 'B'] = f'=B28*(1-{self.closing_cost_seller_decimal})-E6-B30' # This is the one that was changed
        df.at[34, 'B'] = '=((B28/B3)-1)/1'
        df.at[1, 'C'] = 'Beds'
        df.at[19, 'C'] = 'Monthly'
        df.at[20, 'C'] = '=B20'
        df.at[21, 'C'] = '=B21'
        df.at[22, 'C'] = '=B22*B17'
        df.at[23, 'C'] = '=B23*B17'
        df.at[24, 'C'] = '=B24*B17'
        df.at[25, 'C'] = '=B25*B17'
        df.at[27, 'C'] = 1
        df.at[28, 'C'] = '=B3*(1+B6)^C27'
        df.at[29, 'C'] = '=C28-C30'
        df.at[30, 'C'] = '=(B14/(B12/12))*(1-(1/((1+B12/12)^(B13*12-C27*12))))'
        df.at[31, 'C'] = '=(B17*(1+B6)^C27)'
        df.at[32, 'C'] = '=(C31-C31*B22-C31*B23-C31*B24-C31*B25-B21*(1+B6)^C27-B20*(1+B6)^C27-B14)*12'
        df.at[33, 'C'] = f'=C28*(1-{self.closing_cost_seller_decimal})+B32-E6-C30'
        df.at[34, 'C'] = '=((C33+E6)/E6)^(1/C27)-1'
        df.at[1, 'D'] = self.beds
        df.at[3, 'D'] = 'Income (mo)'
        df.at[4, 'D'] = 'Operate Cost (mo)'
        df.at[5, 'D'] = 'Expenses (mo)'
        df.at[6, 'D'] = 'Cash Needed'
        df.at[8, 'D'] = 'Total CF (mo)'
        df.at[9, 'D'] = 'CoC'
        df.at[11, 'D'] = '1-2% Rule'
        df.at[12, 'D'] = '50% Rule'
        df.at[13, 'D'] = '50% Rule (CF)'
        df.at[16, 'D'] = 'NOI (P&I not included)'
        df.at[17, 'D'] = 'Pro Forma Cap'
        df.at[19, 'D'] = 'Yearly'
        df.at[20, 'D'] = '=C20*12'
        df.at[21, 'D'] = '=C21*12'
        df.at[22, 'D'] = '=C22*12'
        df.at[23, 'D'] = '=C23*12'
        df.at[24, 'D'] = '=C24*12'
        df.at[25, 'D'] = '=C25*12'
        df.at[27, 'D'] = 2
        df.at[28, 'D'] = '=B3*(1+B6)^D27'
        df.at[29, 'D'] = '=D28-D30'
        df.at[30, 'D'] = '=(B14/(B12/12))*(1-(1/((1+B12/12)^(B13*12-D27*12))))'
        df.at[31, 'D'] = '=(B17*(1+B6)^D27)'
        df.at[32, 'D'] = '=(D31-D31*B22-D31*B23-D31*B24-D31*B25-B21*(1+B6)^D27-B20*(1+B6)^D27-B14)*12'
        df.at[33, 'D'] = '=D28*(1-B5)+sum(B32:C32)-E6-D30'
        df.at[34, 'D'] = '=((D33+E6)/E6)^(1/D27)-1'
        df.at[1, 'E'] = 'Baths'
        df.at[3, 'E'] = '=B17'
        df.at[4, 'E'] = '=B14+B20+B21'
        df.at[5, 'E'] = '=B14+B20+B21+C22+C23+C24+C25'
        df.at[6, 'E'] = '=B4+B10'
        df.at[8, 'E'] = '=E3-E5'
        df.at[9, 'E'] = '=B17/B10'
        df.at[11, 'E'] = '=B17/B3'
        df.at[12, 'E'] = '=B17/2'
        df.at[13, 'E'] = '=E12-B14'
        df.at[16, 'E'] = '=B17*12-D22-D23-D24-D25-B20*12-B21*12'
        df.at[17, 'E'] = '=E16/B3'
        df.at[19, 'E'] = 'Yearly'
        df.at[20, 'E'] = '=C20*12'
        df.at[21, 'E'] = '=C21*12'
        df.at[22, 'E'] = '=C22*12'
        df.at[23, 'E'] = '=C23*12'
        df.at[24, 'E'] = '=C24*12'
        df.at[25, 'E'] = '=C25*12'
        df.at[27, 'E'] = 3
        df.at[28, 'E'] = '=B3*(1+B6)^E27'
        df.at[29, 'E'] = '=E28-E30'
        df.at[30, 'E'] = '=(B14/(B12/12))*(1-(1/((1+B12/12)^(B13*12-E27*12))))'
        df.at[31, 'E'] = '=(B17*(1+B6)^E27)'
        df.at[32, 'E'] = '=(E31-E31*B22-E31*B23-E31*B24-E31*B25-B21*(1+B6)^E27-B20*(1+B6)^E27-B14)*12'
        df.at[33, 'E'] = '=E28*(1-B5)+sum(B32:D32)-E6-E30'
        df.at[34, 'E'] = '=((E33+E6)/E6)^(1/E27)-1'
        df.at[1, 'F'] = self.baths
        df.at[27, 'F'] = 4
        df.at[28, 'F'] = '=B3*(1+B6)^F27'
        df.at[29, 'F'] = '=F28-F30'
        df.at[30, 'F'] = '=(B14/(B12/12))*(1-(1/((1+B12/12)^(B13*12-F27*12))))'
        df.at[31, 'F'] = '=(B17*(1+B6)^F27)'
        df.at[32, 'F'] = '=(F31-F31*B22-F31*B23-F31*B24-F31*B25-B21*(1+B6)^F27-B20*(1+B6)^F27-B14)*12'
        df.at[33, 'F'] = '=F28*(1-B5)+sum(B32:E32)-E6-F30'
        df.at[34, 'F'] = '=((F33+E6)/E6)^(1/F27)-1'
        df.at[1, 'G'] = 'SQFT'
        df.at[27, 'G'] = 5
        df.at[28, 'G'] = '=B3*(1+B6)^G27'
        df.at[29, 'G'] = '=G28-G30'
        df.at[30, 'G'] = '=(B14/(B12/12))*(1-(1/((1+B12/12)^(B13*12-G27*12))))'
        df.at[31, 'G'] = '=(B17*(1+B6)^G27)'
        df.at[32, 'G'] = '=(G31-G31*B22-G31*B23-G31*B24-G31*B25-B21*(1+B6)^G27-B20*(1+B6)^G27-B14)*12'
        df.at[33, 'G'] = '=G28*(1-B5)+sum(B32:F32)-E6-G30'
        df.at[34, 'G'] = '=((G33+E6)/E6)^(1/G27)-1'
        df.at[1, 'H'] = self.sqft
        df.at[27, 'H'] = 10
        df.at[28, 'H'] = '=B3*(1+B6)^H27'
        df.at[29, 'H'] = '=H28-H30'
        df.at[30, 'H'] = '=(B14/(B12/12))*(1-(1/((1+B12/12)^(B13*12-H27*12))))'
        df.at[31, 'H'] = '=(B17*(1+B6)^H27)'
        df.at[32, 'H'] = '=(H31-H31*B22-H31*B23-H31*B24-H31*B25-B21*(1+B6)^H27-B20*(1+B6)^H27-B14)*12'
        df.at[27, 'I'] = 10
        df.at[28, 'I'] = '=B3*(1+B6)^I27'
        df.at[29, 'I'] = '=I28-I30'
        df.at[30, 'I'] = '=(B14/(B12/12))*(1-(1/((1+B12/12)^(B13*12-I27*12))))'
        df.at[31, 'I'] = '=(B17*(1+B6)^I27)'
        df.at[32, 'I'] = '=(I31-I31*B22-I31*B23-I31*B24-I31*B25-B21*(1+B6)^I27-B20*(1+B6)^I27-B14)*12'

        return df

# Get all of the house data from homedata.json
with open('homedata.json') as file:
    data = json.load(file)

# Check if there are any houses in the list pulled
if not data:
    print("No houses found")
    
else:
    # TODO: Create a function for the excel file to be generated
    # Create a name for the excel file
    excel_file_name = str(date.today()) + "-house-analysis.xlsx"
    
    # Create a list to store all the dataframes
    house_dataframes = []
    
    # Loop through each of the houses in the dataset and add them to a list of analyzed houses
    for house_data in data:
        house = House(house_data)
        house_dataframes.append(house.house_pd_df())

    with pd.ExcelWriter(excel_file_name, engine="openpyxl") as writer:
        house.house_pd_df().to_excel(writer, sheet_name="Sheet1")