from sympy import symbols, Eq, solve as sym_solve, simplify

def solve(coeff_left=4, coeff_quad=-1, coeff_lin=6):
    """
    Parametric solver for the 수능 piecewise function problem.
    
    Parameters:
    - coeff_left: constant in (x + coeff_left) on left region
    - coeff_quad: quadratic coefficient on right region
    - coeff_lin: linear coefficient on right region
    
    Function definition:
    f(x) = (x + coeff_left)(x + a)  for x < -coeff_left or -coeff_left < x < 0
         = b                        for x = -coeff_left
         = coeff_quad*x^2 + coeff_lin*x + c  for x >= 0
    
    From condition (가): a = k + coeff_left, c = coeff_left * a
    From conditions (가)+(나): f(k - coeff_left) = f(k)
    """
    k = symbols('k', positive=True, real=True)
    
    # Derived relationships from condition (가)
    a = k + coeff_left
    c = coeff_left * a
    
    # f(k) in right region (x >= 0)
    f_k = coeff_quad * k**2 + coeff_lin * k + c
    
    # f(k - coeff_left) in right region
    f_k_minus_shift = (coeff_quad * (k - coeff_left)**2 + 
                       coeff_lin * (k - coeff_left) + c)
    
    # Continuity condition from (가)+(나): f(k - coeff_left) = f(k)
    eq = Eq(f_k_minus_shift, f_k)
    
    # Solve for k
    k_sols = sym_solve(eq, k)
    k_val = [sol for sol in k_sols if sol.is_positive][0]
    
    # Substitute back to find all parameters
    a_val = k_val + coeff_left
    c_val = coeff_left * a_val
    b_val = coeff_quad * k_val**2 + coeff_lin * k_val + c_val
    
    # Calculate target: x = c - a - b
    x_val = c_val - a_val - b_val
    
    # Compute f(x) using left region formula: (x + coeff_left)(x + a)
    f_result = (x_val + coeff_left) * (x_val + a_val)
    
    return simplify(f_result)

# Verification
CANDIDATE = 50
print('VERIFY_PASS' if solve() == CANDIDATE else 'VERIFY_FAIL')