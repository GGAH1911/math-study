from sympy import symbols, diff, solve

CANDIDATE = 30

t, k = symbols('t k', real=True)
x = 2*t**3 - k*t**2
v = diff(x, t)
a = diff(v, t)

# 조건 1: t=1에서 속도가 0
v_at_1 = v.subs(t, 1)
k_value = solve(v_at_1, k)[0]

# k = 3 확인
assert k_value == 3, f"k should be 3, got {k_value}"

# 조건 2: t=3에서의 가속도
a_at_k = a.subs([(t, k_value), (k, k_value)])

if a_at_k == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')