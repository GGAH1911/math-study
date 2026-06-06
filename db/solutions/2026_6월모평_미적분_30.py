from sympy import Rational

def solve(c1=Rational(1, 8), c2=Rational(3, 4), gamma=2):
    """
    Solve the parametric problem.
    
    Parameters:
    - c1, c2: coefficients in Q = c1 - c2*P (from differentiability condition)
    - gamma: location of constraint f(gamma) ≤ 0
    
    Returns p + q where m = p/q (in lowest terms) is the minimum value of g(x).
    """
    # From constraint f(gamma) ≤ 0 where f(x) = (x-1)^2(x-P) + Q
    # Calculate P_min from: (γ-1)^2(γ-P) + Q ≤ 0
    P = ((gamma - 1)**2 * gamma + c1) / ((gamma - 1)**2 + c2)
    
    # From differentiability condition: Q = c1 - c2*P
    Q = c1 - c2 * P
    
    # Minimum value: m = -Q
    m = -Q
    
    # Extract numerator and denominator (sympy ensures lowest terms)
    p = m.p
    q = m.q
    
    return p + q

# Verify with original problem parameters
CANDIDATE = 25
print('VERIFY_PASS' if solve() == CANDIDATE else 'VERIFY_FAIL')