import sympy as sp
x = sp.Symbol('x')

# 경우 2: P(x) = x^2 - 2x - 9
P2 = x**2 - 2*x - 9
P2_sq = sp.expand(P2**2)
divisor = x**2 - 4*x - 5
quotient2, remainder2 = sp.div(P2_sq, divisor)
Q2 = quotient2
Q2_at_minus1 = Q2.subs(x, -1)

# 경우 3: P(x) = x^2 - 6x - 1
P3 = x**2 - 6*x - 1
P3_sq = sp.expand(P3**2)
quotient3, remainder3 = sp.div(P3_sq, divisor)
Q3 = quotient3
Q3_at_minus1 = Q3.subs(x, -1)

# 검증
verify2 = sp.expand(divisor * quotient2 + 36) == P2_sq
verify3 = sp.expand(divisor * quotient3 + 36) == P3_sq

sum_Q_minus1 = int(Q2_at_minus1) + int(Q3_at_minus1)

if verify2 and verify3 and sum_Q_minus1 == 8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')