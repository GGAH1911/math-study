from sympy import *

def f(m):
    """(가): (-1)^m / (m+1)"""
    return Rational((-1)**m, m + 1)

def g(m):
    """(나): m!"""
    return factorial(m)

def h(m):
    """(다): m+1"""
    return m + 1

numerator = g(3) + h(3)
denominator = f(4)
expression = numerator / denominator
CANDIDATE = 50
result = simplify(expression)

if result == CANDIDATE:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")