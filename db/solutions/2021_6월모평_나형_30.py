import sympy as sp
from sympy import sqrt, symbols, solve, simplify

x = symbols('x', real=True)
a = 3
c = sp.Rational(2, 3)
d = -6
b = symbols('b', real=True)

f = -a*(x+1)**2 + b
g = c*x**3 + d*x + (-a + b)

# 검증 1: h(x) = h(0) 실근의 합 = 1
root_left = solve(f - (-a + b), x)
root_right = solve(g - (-a + b), x)
root_right = [r for r in root_right if r > 0]
all_roots = root_left + root_right
sum_roots = sum(all_roots)
if simplify(sum_roots - 1) == 0:
    check1 = True
else:
    check1 = False

# 검증 2: 최댓값과 최솟값의 차
f_prime = sp.diff(f, x)
g_prime = sp.diff(g, x)
crit_x1 = -1  # f 극값
crit_x2 = sqrt(3)  # g 극값

f_at_1 = f.subs(x, -1)
f_at_m2 = f.subs(x, -2)
f_at_0 = f.subs(x, 0)
g_at_sqrt3 = g.subs(x, sqrt(3))
g_at_3 = g.subs(x, 3)

max_val = f_at_1
min_val = g_at_sqrt3
diff = simplify(max_val - min_val)
expected_diff = 3 + 4*sqrt(3)

if simplify(diff - expected_diff) == 0:
    check2 = True
else:
    check2 = False

# 검증 3: 답
h_prime_m3 = f_prime.subs(x, -3)
h_prime_4 = g_prime.subs(x, 4)
answer = h_prime_m3 + h_prime_4

if answer == 38 and check1 and check2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')