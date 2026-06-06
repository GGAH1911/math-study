from sympy import symbols, expand
x, a = symbols('x a')
# 원래 함수: y = x^2 + 4x + a
# a = 4일 때
y = x**2 + 4*x + 4
# 중근 확인: 완전제곱식이 되는지
factored = expand((x + 2)**2)
if y == factored:
    # x축과의 교점이 정확히 하나인지 확인
    from sympy import solve
    roots = solve(y, x)
    if len(roots) == 1:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')