import sympy as sp

# 문제 조건
a, b, x = -1, -1, -2
f = lambda x: a*x**2 + b*x + 5

# 조건 검증
print('조건 (가) 검증:')
print(f'  a={a}, b={b} (모두 음의 정수): {a < 0 and b < 0 and isinstance(a, int) and isinstance(b, int)}')

print('\n조건 (나) 검증:')
f_vals = [f(x) for x in [1, 1.5, 2]]
max_f = max(f_vals)
print(f'  f(1)={f(1)}, f(1.5)={f(1.5)}, f(2)={f(2)}')
print(f'  [1,2]에서 최댓값={max_f}, 조건값=3: {max_f == 3}')

print('\n최종 답 검증:')
result = f(-2)
print(f'  f(-2)={result}')
print('VERIFY_PASS' if result == 3 else 'VERIFY_FAIL')