from math import factorial
from itertools import permutations

def count_arrangements():
    # 양 끝이 (1,3)인 경우
    case1 = factorial(5) // (factorial(2) * factorial(2) * factorial(1))
    
    # 양 끝이 (3,1)인 경우
    case2 = factorial(5) // (factorial(2) * factorial(2) * factorial(1))
    
    # 양 끝이 (2,2)인 경우
    case3 = factorial(5) // (factorial(3) * factorial(2))
    
    total = case1 + case2 + case3
    return total

result = count_arrangements()
if result == 70:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')