import sympy as sp

# 원래 문제 조건으로 직접 좌표 구성
R = 6
AB_len = 8*sp.sqrt(2)

# 중심 O를 원점, 현 AB의 중점이 (-2,0)이 되도록 배치 (OM = sqrt(R^2 - (AB/2)^2) = 2)
A_pt = sp.Matrix([-2, -4*sp.sqrt(2)])
B_pt = sp.Matrix([-2,  4*sp.sqrt(2)])
O_pt = sp.Matrix([0, 0])

# OA = OB = 6, AB = 8 sqrt 2 사전 검증
assert sp.simplify((A_pt - O_pt).norm() - R) == 0
assert sp.simplify((B_pt - O_pt).norm() - R) == 0
assert sp.simplify((A_pt - B_pt).norm() - AB_len) == 0

# 후보 답
BP_ans = sp.Rational(4,3)*sp.sqrt(6)
AP_ans = 3*BP_ans

# 원래 조건 그대로: P가 반지름 6인 원 위, AP:BP = 3:1, 그리고 호 AB 위 (부채꼴 단호 측면 = x < -2)
x, y = sp.symbols('x y', real=True)
eqs = [
    x**2 + y**2 - R**2,                                  # P는 원 위
    (x - A_pt[0])**2 + (y - A_pt[1])**2 - AP_ans**2,     # |PA| = AP_ans
    (x - B_pt[0])**2 + (y - B_pt[1])**2 - BP_ans**2,     # |PB| = BP_ans
]
sols = sp.solve(eqs, [x, y], dict=True)

ok = False
for s in sols:
    xv = sp.nsimplify(s[x])
    yv = sp.nsimplify(s[y])
    # P는 호 AB(단호) 위: O로부터 AB의 반대쪽, 즉 x < -2
    if float(xv) >= -2:
        continue
    # angle BPA > 90°  <=>  vec(PA)·vec(PB) < 0
    PA = sp.Matrix([A_pt[0]-xv, A_pt[1]-yv])
    PB = sp.Matrix([B_pt[0]-xv, B_pt[1]-yv])
    dot = sp.simplify(PA.dot(PB))
    if dot < 0:
        # 원래 AP/BP 비율 재확인
        ap = sp.simplify(PA.norm())
        bp = sp.simplify(PB.norm())
        if sp.simplify(ap/bp - 3) == 0 and sp.simplify(bp - BP_ans) == 0:
            ok = True
            break

print('VERIFY_PASS' if ok else 'VERIFY_FAIL')
