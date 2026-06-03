from sympy import symbols, solve, Rational
a, b, d = symbols('a b d')
# 네 수 a, 4, b, 10이 등차수열
sol = solve([4 - a - d, b - 4 - d, 10 - b - d], [a, b, d])
A = sol[a]
B = sol[b]
val = A + 2*B
print('VERIFY_PASS' if val == 15 else 'VERIFY_FAIL')
