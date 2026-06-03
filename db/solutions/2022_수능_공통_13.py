from sympy import symbols, solve, log, simplify

# 주어진 조건: b^a = a^b, a^b = 20
# f(x) = a^(bx) + b^(ax)
# f(1) = a^b + b^a = 40을 만족하는지 확인

# a^b = 20, b^a = 20이므로
a_b = 20
b_a = 20

f_1 = a_b + b_a
print(f'f(1) = {f_1}')
assert f_1 == 40, f'f(1) should be 40, got {f_1}'

# f(2) 계산
f_2 = a_b**2 + b_a**2
print(f'f(2) = {f_2}')
assert f_2 == 800, f'f(2) should be 800, got {f_2}'

print('VERIFY_PASS')