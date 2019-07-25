# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 22:08:31 2019

@author: Paul

Time spent: About 20 minutes
"""

def credit_card_payoff(balance, int_rate, dollar_increment = 10.0, max_months = 12, debug = False):
    """
    Function to compute minimum fixed payment to pay off a balance within 12 months
    balance: float
    int_rate: float
    dollar_increment: float, monthly payment must be a multiple of this number
    max_months: integer, 12 by default
    """

    # Initialize variables
    pay = 0.0
    tmp_balance = balance

    # Main loop
    while tmp_balance > 0:
    
        # Set the current helper variables
        tmp_balance = balance
        pay += dollar_increment
        month = 0

        # Check if current payment amount works
        while tmp_balance > 0 and month < max_months:
            # Look at balance next month
            month += 1
            
            # Definitions given in the problem set
            # Add the month's interest then subtract the month's payment
            tmp_balance = round(tmp_balance + tmp_balance * int_rate/12 - pay, 2)
        
        # Debugging
        if debug:
            print('  When paying $' + str(pay) +  ' per month, the balance after ' + str(month) + ' months is $' + str(tmp_balance))
    
    # Print final results
    print('RESULTS')
    print('Monthly payment to pay off debt in 1 year: $' + str(pay))
    print('Number of months needed: ' + str(month))
    print('Balance: $' + str(tmp_balance))
    print('')
    
## First test case with debugging
#credit_card_payoff(1200, .18, debug = True)
#
## First test case
#credit_card_payoff(1200, .18)
#
## Second test case
#credit_card_payoff(32000, .2)
    
# Custom parameters
balance = float(raw_input('Enter the annual credit card interest rate as a decimal: '))
int_rate = float(raw_input('Enter the annual credit card interest rate as a decimal: '))

credit_card_payoff(balance, int_rate)