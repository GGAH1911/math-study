from sympy import sqrt, simplify

S = 10 + 2*sqrt(15)

# 고객용 넓이 = (√15/5) * S
customer = (sqrt(15)/5) * S

# 회수용 넓이 = 4
collection = 4

# 검증: 고객용 + 회수용 == S
diff = simplify(customer + collection - S)

if diff == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL:', diff)
