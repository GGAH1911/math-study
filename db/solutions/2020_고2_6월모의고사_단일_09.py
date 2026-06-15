from sympy import symbols, log, solve, Rational
x, k = symbols('x k')
asymptote_y = -1
# 점근선 y=-1 과 y=log2(x+k) 의 교점이 y축(x=0) 위에 있음
# x=0 대입: log2(0+k) = -1 => k = 1/2
k_val = solve(log(0 + k, 2) - asymptote_y, k)
assert len(k_val) == 1
k_sol = k_val[0]
# 검증: x=0에서 y값
y_check = log(0 + k_sol, 2)
if y_check == asymptote_y:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')