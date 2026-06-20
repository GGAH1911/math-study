import sympy as sp

t, k = sp.symbols('t k', real=True, positive=True)
v = 2*t - 6

# 거리 계산: ∫₃ᵏ |v(t)| dt
# k > 3일 때 [3, k]에서 v(t) ≥ 0
distance = sp.integrate(v, (t, 3, k))
distance_simplified = sp.expand(distance)

# 거리가 25라는 조건
eq = sp.Eq(distance_simplified, 25)
solution = sp.solve(eq, k)

# k > 3인 해 찾기
valid_solutions = [sol for sol in solution if sol > 3]

if len(valid_solutions) == 1:
    k_value = valid_solutions[0]
    # 검증: k = 8일 때 거리가 25인지 확인
    distance_check = distance_simplified.subs(k, k_value)
    if distance_check == 25:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')