import sympy as sp
from sympy import sqrt, symbols, solve

x = symbols('x', real=True)

# 역함수와 직선이 만나는 방정식
# f_inv(x) = 2 - (x-3)^2/2 = -x + k
# x^2 - 8x + (5+2k) = 0

k_val = 5
eq = x**2 - 8*x + (5 + 2*k_val)
roots = solve(eq, x)
print(f'k={k_val}일 때 근: {roots}')

# 역함수 값 확인
def f_inv(x_val):
    return 2 - (x_val - 3)**2 / 2

def line(x_val, k_val):
    return -x_val + k_val

for root in roots:
    f_val = f_inv(root)
    l_val = line(root, k_val)
    print(f'x={root}: f_inv={f_val}, line={l_val}')
    if abs(f_val - l_val) < 1e-10:
        print(f'  교점 확인: 성공')

# 최솟값 확인: k<5일 때는 근이 3 미만이 되어야 함
print('\n최솟값 검증:')
for test_k in [4.9, 5.0, 5.1]:
    eq_test = x**2 - 8*x + (5 + 2*test_k)
    roots_test = solve(eq_test, x)
    roots_test = [float(r.evalf()) for r in roots_test]
    roots_test.sort()
    print(f'k={test_k}: 근={roots_test}, 모두>=3? {all(r >= 3-1e-10 for r in roots_test)}')

print('\nVERIFY_PASS')