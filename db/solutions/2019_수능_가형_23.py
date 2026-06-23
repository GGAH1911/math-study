import sympy as sp
# 파라미터: tan θ = t (유사문제 재생성용 — t 바꾸면 새 문제)
t = 5
CANDIDATE = 26
# 원식 그대로: sec²θ = 1 + tan²θ (삼각함수 상호관계)
theta = sp.atan(t)
sec2 = sp.simplify(1 + sp.tan(theta)**2)
print('VERIFY_PASS' if sp.nsimplify(sec2) == CANDIDATE else 'VERIFY_FAIL')
