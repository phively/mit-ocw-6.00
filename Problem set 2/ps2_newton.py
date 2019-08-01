# 6.00 Problem Set 2
#
# Successive Approximation
# Paul Hively
# Time spent: about 25 minutes

def evaluate_poly(poly, x, debug = False):
    """
    Computes the polynomial function for a given value x. Returns that value.

    Example:
    >>> poly = (0.0, 0.0, 5.0, 9.3, 7.0)    # f(x) = 7x^4 + 9.3x^3 + 5x^2
    >>> x = -13
    >>> print evaluate_poly(poly, x)  # f(-13) = 7(-13)^4 + 9.3(-13)^3 + 5(-13)^2
    180339.9

    poly: tuple of numbers, length > 0
    x: number
    returns: float
    """
    # Variables for use
    y = 0.0 # float
    
    # Loop through the tuple, incrementing y by the current term
    # Note that enumerate returns an index (power) and float (the coefficient)
    for power, coef in enumerate(poly):
        y += coef * x ** power
        if debug:
            print y
        
    return(y)


def compute_deriv(poly):
    """
    Computes and returns the derivative of a polynomial function. If the
    derivative is 0, returns (0.0,).

    Example:
    >>> poly = (-13.39, 0.0, 17.5, 3.0, 1.0)    # x^4 + 3x^3 + 17.5x^2 - 13.39
    >>> print compute_deriv(poly)        # 4x^3 + 9x^2 + 35^x
    (0.0, 35.0, 9.0, 4.0)

    poly: tuple of numbers, length > 0
    returns: tuple of numbers
    """
    # Variables for use
    dydx = ( ) # empty tuple
    
    # Again, we use enumerate to get an index and float
    for power, coef in enumerate(poly):
        if power > 0: # when deriving the constant falls off
            dydx += (coef * power, )
            
    return(dydx)

        
def compute_root(poly, x_0, epsilon, debug = False):
    """
    Uses Newton's method to find and return a root of a polynomial function.
    Returns a tuple containing the root and the number of iterations required
    to get to the root.

    Example:
    >>> poly = (-13.39, 0.0, 17.5, 3.0, 1.0)    #x^4 + 3x^3 + 17.5x^2 - 13.39
    >>> x_0 = 0.1
    >>> epsilon = .0001
    >>> print compute_root(poly, x_0, epsilon)
    (0.80679075379635201, 8.0)

    poly: tuple of numbers, length > 1.
         Represents a polynomial function containing at least one real root.
         The derivative of this polynomial function at x_0 is not 0.
    x_0: float
    epsilon: float > 0
    returns: tuple (float, int)
    """
    # Variables for use
    x = x_0
    y = evaluate_poly(poly, x)
    iters = 1 # iterations through the loop
    
    # Loop while not within epsilon of the answer
    while abs(y) > epsilon:
        
        # Debug printout
        if debug:
            print 'After iteration ' + str(iters) + ':'
            print '  x = ' + str(x) + '  and  y = ' + str(y)
        
        # Increment iteration count
        iters += 1
        # Find new x_{n+1} = x_n - f(x_n) / f'(x_n)
        x -= evaluate_poly(poly, x) / evaluate_poly(compute_deriv(poly), x)
        # Updated y computation
        y = evaluate_poly(poly, x)
            
    return(x, iters)
    
# Check my work for #1: 180339.9
poly = (0.0, 0.0, 5.0, 9.3, 7.0)    # f(x) = 7x^4 + 9.3x^3 + 5x^2
x = -13
print evaluate_poly(poly, x)  # f(-13) = 7(-13)^4 + 9.3(-13)^3 + 5(-13)^2

# Check #2: (0.0, 35.0, 9.0, 4.0)
poly = (-13.39, 0.0, 17.5, 3.0, 1.0) # x4 + 3.0x3 + 17.5x2 - 13.39
print compute_deriv(poly) # 4.0x3 + 9.0x2 + 35.0x

# Check #3: (0.80679075379635201, 8)
poly = (-13.39, 0.0, 17.5, 3.0, 1.0) #x4 + 3.0x3 + 17.5x2 - 13.39
x_0 = 0.1
epsilon = .0001
print compute_root(poly, x_0, epsilon)