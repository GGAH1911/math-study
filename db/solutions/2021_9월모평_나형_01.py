from sympy import S, simplify

# 원식: ∛2 × 2^(2/3) = 2^(1/3) × 2^(2/3)
expr = S(2)**(S(1)/3) * S(2)**(S(2)/3)
result = simplify(expr)

if result == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')