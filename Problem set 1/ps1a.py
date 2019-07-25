# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 21:30:42 2019

@author: Paul

Time spent: about 30 minutes to learn and debug creating a function
"""

def credit_card_interest(balance, int_rate, min_pay, max_months = 12):
    """
    Function to compute interest; note that it asymptotically approaches 0 since min_pay has no floor
    balance: float
    int_rate: float
    min_pay: float
    max_months: integer, 12 by default
    """

    # Other variables used
    month = 0
    tot_paid = 0.0

    # Main loop
    while balance > 0 and month < max_months:
        # Look at balance next month
        month += 1
        print('Month: ' + str(month))
        
        # Definitions given in the problem set
        pay = round(min_pay * balance, 2)
        interest = round(int_rate/12 * balance, 2)
        principal = pay - interest
        balance = balance - principal
        tot_paid += pay
        
        # Print current results
        print('  Minimum monthly payment: $' + str(pay))
        print('  Principal paid: $' + str(principal))
        print('  Remaining balance: $' + str(balance))
        
    # Print final stats
    print('Total amount paid: $' + str(tot_paid))
    print('Remaining balance: $' + str(balance))
    print('')

## First test case
#credit_card_interest(balance = 4800, int_rate = .2, min_pay = .02, max_months = 12)
#
## Second test case
#credit_card_interest(balance = 4800, int_rate = .2, min_pay = .04, max_months = 12)

# Custom parameters
balance = float(raw_input('Enter the outstanding balance on your credit card: '))
int_rate = float(raw_input('Enter the annual credit card interest rate as a decimal: '))
min_pay = float(raw_input('Enter the minimum monthly payment rate as a decimal: '))

credit_card_interest(balance, int_rate, min_pay)