from sympy import symbols, expand, factor

x = symbols('x')
P = (x - 1) * (x**2 - 4*x + 6)

# P(3) 계산
result = P.subs(x, 3)
print(f'P(3) = {result}')

# 검증: P(x) = (x-2)^2 * Q(x) + 2*Q(x)
# 여기서 Q(x) = x - 1
Q = x - 1
quotient_check = expand((x - 2)**2 * Q + 2 * Q)
P_expanded = expand(P)

if quotient_check == P_expanded:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Expected: {P_expanded}')
    print(f'Got: {quotient_check}')