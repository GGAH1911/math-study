from sympy import symbols, solve

k = symbols('k', real=True)

def f(t):
    return -(t - 2)**2 + 4

def g(t):
    return (t - 2)**2

# f(2) = 4 확인
assert f(2) == 4, f'f(2) = {f(2)}, expected 4'

# Case A: f(k)=0 and g(k)=4
roots_f_zero = solve(f(k), k)
case_A = [kv for kv in roots_f_zero if g(kv) == 4]

# Case B: f(k)=4 and g(k)=0
roots_g_zero = solve(g(k), k)
case_B = [kv for kv in roots_g_zero if f(kv) == 4]

all_k = set(case_A + case_B)
count = len(all_k)

# 각 k에서 근이 {0,4}인지 확인
for kv in all_k:
    fk = f(kv)
    gk = g(kv)
    assert set([fk, gk]) == {0, 4}, f'At k={kv}: f={fk}, g={gk}'

# k의 개수 = 3 확인
assert count == 3, f'Expected 3 k values, got {count}'

# 최종 답 계산
result = g(8) - f(8)
expected = 68

if result == expected:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {result}, expected {expected}')
