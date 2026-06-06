def solve(period=3, boundary1=1, boundary2=2, xmin=-5, xmax=5):
    """
    Parametric solver for discontinuity weighting problem.
    
    Problem structure:
    - Piecewise linear periodic function with period 'period'
    - Type A discontinuities at k*period + boundary1
    - Type B discontinuities at k*period + boundary2
    - Each Type B point (x_i) contributes g(x_i) = 2*(k*period + boundary2)*ln(2)
    - Observation range: x in (-xmin, xmax), i.e., 2^x in (2^xmin, 2^xmax)
    
    Args:
        period: Period of the periodic function (default: 3)
        boundary1: Location of Type A discontinuities within period (default: 1)
        boundary2: Location of Type B discontinuities within period (default: 2)
        xmin, xmax: Bounds on x variable (default: -5, 5)
    
    Returns:
        n + sum of [2*(k*period + boundary2)] for all valid Type B points
    """
    
    pow2_max = 2 ** xmax  # Upper bound for 2^x
    
    # Count Type A discontinuities: k*period + boundary1 < pow2_max
    type_a_count = 0
    k = 0
    while k * period + boundary1 < pow2_max:
        type_a_count += 1
        k += 1
    
    # Count Type B discontinuities and sum g-contributions
    sum_g_contribution = 0
    k = 0
    while k * period + boundary2 < pow2_max:
        sum_g_contribution += 2 * (k * period + boundary2)
        k += 1
    type_b_count = k
    
    # Total number of discontinuity points
    n = type_a_count + type_b_count
    
    # Final answer: n + sum of (g(x_i)/ln(2))
    answer = n + sum_g_contribution
    
    return answer


# Verification
CANDIDATE = 331
print('VERIFY_PASS' if solve() == CANDIDATE else 'VERIFY_FAIL')