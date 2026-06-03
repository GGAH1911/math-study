import sympy as sp

a = -4
b = a - 8
print(f'a = {a}, b = {b}')

x = sp.Symbol('x')
P = x**3 + a*x**2 + b*x - 4
Q = x**2 + (a-1)*x - 7

# 검증: P(x) = (x+1)Q(x) + 3
quotient, remainder = sp.div(P, x+1)
print(f'P(x)를 (x+1)로 나눈 몫: {quotient}')
print(f'P(x)를 (x+1)로 나눈 나머지: {remainder}')
assert quotient == Q, f'몫이 일치하지 않음'
assert remainder == 3, f'나머지가 일치하지 않음'

# 검증: (x^2+a)Q(x-2)가 x-2로 나누어떨어짐
expr = (x**2 + a) * Q.subs(x, x-2)
quotient2, remainder2 = sp.div(expr, x-2)
print(f'(x^2+a)Q(x-2)을 (x-2)로 나눈 나머지: {remainder2}')
assert remainder2 == 0, f'나머지가 0이 아님'

# Q(1) 계산
result = Q.subs(x, 1)
print(f'Q(1) = {result}')
assert result == -11, f'Q(1)이 -11이 아님'

print('VERIFY_PASS')