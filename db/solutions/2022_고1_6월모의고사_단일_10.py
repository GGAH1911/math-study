import sympy as sp

x, a = sp.symbols('x a')
f = x**2 + 2*(a-1)*x + 2*a + 13
# 판별식: b^2 - 4ac (b = 2(a-1), c = 2a+13)
D = (2*(a-1))**2 - 4*(2*a + 13)
D_simplified = sp.expand(D)

# 정수 a에 대해 그래프가 x축과 만나지 않는 조건 D < 0
valid_integers = []
for a_val in range(-100, 101):
    d_val = D_simplified.subs(a, a_val)
    if d_val < 0:
        valid_integers.append(a_val)

total = sum(valid_integers)
expected = 14

# 추가 검증: 각 정수 a에 대해 실제로 x축과 만나지 않는지 확인
all_ok = True
for a_val in valid_integers:
    poly = f.subs(a, a_val)
    roots = sp.solve(poly, x)
    real_roots = [r for r in roots if r.is_real]
    if len(real_roots) > 0:
        all_ok = False
        break

if total == expected and all_ok and valid_integers == [-1,0,1,2,3,4,5]:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
