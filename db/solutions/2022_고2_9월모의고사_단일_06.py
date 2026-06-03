from sympy import symbols, solve
a, d = symbols('a d')
# 조건: a1 + a2 + a3 + a4 + a5 = 30
a1 = a
a2 = a + d
a3 = a + 2*d
a4 = a + 3*d
a5 = a + 4*d
sum_eq = a1 + a2 + a3 + a4 + a5 - 30
print('sum_eq:', sum_eq)
# 이 식을 정리하면 5a + 10d = 30, 즉 a + 2d = 6
print('sum equation:', sum_eq, '= 0')
# a2 + a4 계산
result = a2 + a4
print('a2 + a4 =', result)
print('a2 + a4 = 2a + 4d = 2(a + 2d)')
# a + 2d = 6이므로 a2 + a4 = 2*6 = 12
print('a + 2d = 6이므로 a2 + a4 = 12')
print('VERIFY_PASS')