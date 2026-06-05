import sympy as sp
x = sp.Symbol('x')
answer = 24

# 원래 문제 조건을 만족하는 임의의 다항함수 여러 쌍으로 검증
test_cases = [
    (8*x - 12, 8*x - 17),
    (8*x - 12 + (x-2)**2, 8*x - 17 - (x-2)**2),
    (4 + 8*(x-2) + 3*(x-2)**3, -1 + 8*(x-2) + 5*(x-2)**2),
    (4 + 8*(x-2) - 7*(x-2)**2 + 2*(x-2)**4, -1 + 8*(x-2) + 11*(x-2)**3),
]

all_pass = True
for f, g in test_cases:
    lim1 = sp.limit((f - 4)/(x**2 - 4), x, 2)
    lim2 = sp.limit((g + 1)/(x - 2), x, 2)
    if sp.simplify(lim1 - 2) != 0 or sp.simplify(lim2 - 8) != 0:
        all_pass = False
        break
    h = f * g
    hp = sp.diff(h, x).subs(x, 2)
    if sp.simplify(hp - answer) != 0:
        all_pass = False
        break

print('VERIFY_PASS' if all_pass else 'VERIFY_FAIL')
