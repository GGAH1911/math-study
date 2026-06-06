import numpy as np
from scipy.optimize import fsolve

def verify():
    # Case 2: f(x) = x^3/3 + x^2 - 18
    def f2(x):
        return x**3/3 + x**2 - 18
    
    # Check f(3) = 0
    assert abs(f2(3)) < 1e-9, f"f(3) = {f2(3)}"
    
    # Check original equation at several points
    for x_test in [-1, 0, 1, 2, 3, 4]:
        lhs = f2(x_test)**2
        
        # RHS: 2 * integral from 3 to x of (t^2 + 2t)*f(t) dt
        def integrand(t):
            return (t**2 + 2*t) * f2(t)
        
        from scipy.integrate import quad
        rhs = 2 * quad(integrand, 3, x_test)[0]
        
        if abs(lhs - rhs) > 1e-6:
            print(f"VERIFY_FAIL at x={x_test}: lhs={lhs}, rhs={rhs}")
            return
    
    # Verify integral calculation for Case 2
    from scipy.integrate import quad
    integral_case2 = quad(f2, -3, 0)[0]
    expected_case2 = -207/4
    assert abs(integral_case2 - expected_case2) < 1e-6, f"Integral Case 2: {integral_case2} vs {expected_case2}"
    
    # Case 3: f(x) = x^3/3 + x^2 for x<0, f(x)=0 for x>=0
    def f3(x):
        return (x**3/3 + x**2) if x < 0 else 0
    
    integral_case3 = quad(lambda x: f3(x) if x < 0 else 0, -3, 0)[0]
    expected_case3 = 9/4
    assert abs(integral_case3 - expected_case3) < 1e-6, f"Integral Case 3: {integral_case3} vs {expected_case3}"
    
    M = 9/4
    m = -207/4
    answer = M - m
    assert abs(answer - 54) < 1e-6, f"M - m = {answer}"
    
    print("VERIFY_PASS")

verify()