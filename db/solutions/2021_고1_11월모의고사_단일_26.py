import sympy as sp
x, a = sp.symbols('x a', real=True)
f = x**2 - 2*a*x + 2*a**2

# a = 3을 대입
f_sub = f.subs(a, 3)

# 최솟값이 10인지 확인 (x=2에서)
min_val = f_sub.subs(x, 2)
assert min_val == 10, f'Min value check failed: {min_val}'

# 최댓값이 18인지 확인 (x=0에서)
max_val = f_sub.subs(x, 0)
assert max_val == 18, f'Max value check failed: {max_val}'

print('VERIFY_PASS')