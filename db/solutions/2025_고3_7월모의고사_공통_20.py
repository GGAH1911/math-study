def solve(critical_point=4, eval_point=6):
    """
    Parametric solver for the 수능 function problem.
    
    Given:
    - f(x) = -2^{-x+a} + b
    - g(x) piecewise function with critical point at critical_point
    - Condition: For all real t, y=g(x) and y=t intersect in exactly 0 or 2 points
    
    From the intersection condition:
    - For x < critical_point: g(x) = 2^{x+1}, range = (0, 2^{critical_point+1})
    - For x > critical_point: g(x) = -2^{-x+a+1} + 2b, range must equal above
    
    Solving the range equality constraint:
    - 2b = 2^{critical_point+1}  =>  b = 2^{critical_point}
    - -2^{-critical_point+a+1} + 2b = 0  =>  a = 2*critical_point
    
    Parameters:
    - critical_point: The x-value where g(x) behavior changes (default 4)
    - eval_point: The x-value at which to evaluate g(x) (default 6)
    """
    
    # Derive a and b from the constraint condition
    a = 2 * critical_point
    b = 2 ** critical_point
    
    # Evaluate g(eval_point)
    if eval_point <= critical_point:
        # For x < critical_point: g(x) = 2^{x+1}
        return 2 ** (eval_point + 1)
    else:
        # For x > critical_point: g(x) = -2^{-x+a+1} + 2b
        exponent = -eval_point + a + 1
        return -2**exponent + 2*b


CANDIDATE = 24
print('VERIFY_PASS' if solve() == CANDIDATE else 'VERIFY_FAIL')