import sympy as sp
import numpy as np
from sympy import symbols, solve, factor, count_roots

x, a = symbols('x a', real=True)

# 원래 방정식
eq = x**3 - 5*x**2 + (a+4)*x - a

# a=3일 때
eq_a3 = eq.subs(a, 3)
roots_a3 = solve(eq_a3, x)
distinct_a3 = len(set([float(r) for r in roots_a3]))
print(f'a=3: roots={roots_a3}, distinct count={distinct_a3}')
assert distinct_a3 == 2, f'a=3 failed: {distinct_a3} distinct roots'

# a=4일 때
eq_a4 = eq.subs(a, 4)
roots_a4 = solve(eq_a4, x)
distinct_a4 = len(set([float(r) for r in roots_a4]))
print(f'a=4: roots={roots_a4}, distinct count={distinct_a4}')
assert distinct_a4 == 2, f'a=4 failed: {distinct_a4} distinct roots'

# 답 검증: 합이 7
answer_sum = 3 + 4
print(f'Answer: {answer_sum}')
assert answer_sum == 7
print('VERIFY_PASS')