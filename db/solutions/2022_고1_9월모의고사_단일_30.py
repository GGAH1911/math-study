import sympy as sp
x = sp.Symbol('x')
f = x**2 + 2*x - 16
g = -x**2 + 2*x + 16

# h 함수 정의
def h(val):
    if val < -4 or val > 4:
        return f.subs(x, val)
    else:
        return g.subs(x, val)

# h(2) + h(5) 계산
h2 = h(2)
h5 = h(5)
result = h2 + h5

print(f'h(2) = {h2}')
print(f'h(5) = {h5}')
print(f'h(2) + h(5) = {result}')

# 조건 (가) 검증: h(x) = h(4) = 8의 근
eq1 = f - 8  # x < -4
eq2 = g - 8  # -4 ≤ x ≤ 4
roots1 = sp.solve(eq1, x)
roots2 = sp.solve(eq2, x)
all_roots = [r for r in roots1 if r < -4] + [r for r in roots2 if -4 <= r <= 4]
root_sum = sum(all_roots) if len(all_roots) == 3 else None
print(f'Roots of h(x)=8: {all_roots}, Sum: {root_sum}')

if result == 35:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')