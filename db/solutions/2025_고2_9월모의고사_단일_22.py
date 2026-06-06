from sympy import symbols, simplify, Integer

CANDIDATE = 3

# 원래 방정식: 25^x = (1/5)^(x-9)
# 이를 정리하면: 5^(2x) = 5^(9-x)
left_side = Integer(5)**(2*CANDIDATE)
right_side = Integer(5)**(9 - CANDIDATE)

if left_side == right_side:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")