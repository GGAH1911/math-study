import sympy as sp
x, a, b = sp.symbols('x a b', real=True)

# a = 6, b = 6
a_val, b_val = 6, 6

# Check that x^2 - bx + 9 = (x - a/2)^2
quadratic = x**2 - b_val*x + 9
factored = (x - a_val/2)**2

# Verify they are equal
if sp.simplify(quadratic - factored) == 0:
    # Verify conditions
    # At x = a/2 = 3: quadratic should be 0 (not > 0)
    at_critical = quadratic.subs(x, a_val/2)
    # For x != 3: quadratic should be > 0 for all such x
    discriminant = b_val**2 - 4*9
    
    if at_critical == 0 and discriminant == 0:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')