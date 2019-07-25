# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 22:31:12 2019

@author: Paul

Time spent: About half an hour, mostly spent tweaking the stopping condition
"""

# Bisection search method
def credit_card_exact_payoff(balance, int_rate, dollar_increment = 0.01, max_months = 12, debug = False):
    """
    Function to compute minimum fixed payment to pay off a balance within 12 months
    balance: float
    int_rate: float
    dollar_increment: float, monthly payment must be a multiple of this number
    max_months: integer, 12 by default
    debug: when True, print debug information
    """

    # Initialize variables
    lbound = balance / 12.0
    ubound = (balance * (1 + int_rate / 12.0) ** 12) / 12
    # Pay amount starts at the midpoint, rounded up
    tmp_balance = balance

    # Main loop
    # My stopping condition needs to check that we are to the nearest cent
    while ubound - lbound > .01:
    
        # Set the current helper variables
        tmp_balance = balance
        pay = round(100 * (lbound + ubound) / 2, 0) / 100
        month = 0

        # Check if current payment amount works
        while tmp_balance > 0 and month < max_months:
            # Look at balance next month
            month += 1
            
            # Definitions given in the problem set
            # Add the month's interest then subtract the month's payment
            tmp_balance = tmp_balance + tmp_balance * int_rate/12 - pay
        
        # Debugging
        if debug:
            print('  When paying $' + str(pay) +  ' per month, the balance after ' + str(month) + ' months is $' + str(tmp_balance))
            print('    Current lbound = ' + str(lbound))
            print('    Current ubound = ' + str(ubound))
        
        # Update ubound and lbound for the next run
        if tmp_balance > 0:
            lbound = (lbound + ubound) / 2
        elif tmp_balance < 0:
            ubound = (lbound + ubound) / 2
    
    # Print final results
    print('RESULTS')
    print('Monthly payment to pay off debt in 1 year: $' + str(pay))
    print('Number of months needed: ' + str(month))
    print('Balance: $' + str(round(tmp_balance, 2)))
    print('')
    
## First test case
#credit_card_exact_payoff(320000, .2, debug = True)
#
## Second test case
#credit_card_exact_payoff(999999, .18, debug = True)
#    
# Custom parameters
balance = float(raw_input('Enter the outstanding balance on your credit card: '))
int_rate = float(raw_input('Enter the annual credit card interest rate as a decimal: '))

credit_card_exact_payoff(balance, int_rate)