import math
from scipy.optimize import fminbound

def compute():
    # OA = sqrt(2), OB = 2*sqrt(2), cos(angle AOB) = 1/4
    OA = math.sqrt(2)
    OB = 2 * math.sqrt(2)
    cos_angle = 0.25
    sin_angle = math.sqrt(1 - 0.25**2)
    
    # OA·OB = |OA||OB|cos(angle) = sqrt(2)*2*sqrt(2)*1/4 = 1
    dot_OA_OB = 1
    
    # For each t in [0, 1/3], s = 1 - 3t
    # |OP|^2 = 20t^2 - 10t + 2
    
    def norm_OP_squared(t):
        return 20*t**2 - 10*t + 2
    
    # Find max and min of |OP| in [0, 1/3]
    t_opt = 0.25  # Critical point
    
    vals = [
        norm_OP_squared(0),
        norm_OP_squared(1/4),
        norm_OP_squared(1/3)
    ]
    
    min_norm_sq = min(vals)
    max_norm_sq = max(vals)
    
    min_norm = math.sqrt(min_norm_sq)
    max_norm = math.sqrt(max_norm_sq)
    
    # M = 3*max_norm + sqrt(2)
    # m = 3*min_norm - sqrt(2)
    sqrt2 = math.sqrt(2)
    
    M = 3*max_norm + sqrt2
    m = 3*min_norm - sqrt2
    
    prod = M * m
    
    # Should be 6*sqrt(6) - 8
    expected = 6*math.sqrt(6) - 8
    
    # Verify a=6, b=-8
    a, b = 6, -8
    answer = a**2 + b**2
    
    # Check: M*m = a*sqrt(6) + b
    if abs(prod - expected) < 1e-6:
        print('VERIFY_PASS')
    else:
        print(f'VERIFY_FAIL: {prod} vs {expected}')

compute()