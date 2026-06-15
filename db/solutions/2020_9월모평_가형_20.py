import sympy as sp

# 2020 9월모평 가형 20: 반지름1·중심각 π/2 부채꼴 OAB. 호 위 P, H=P의 OA정사영,
# Q=(P에서의 접선)∩OA, R=(중심Q 반지름QA 원)∩PQ. f=△OHP 넓이, g=부채꼴 QRA 넓이.
# lim_{θ→0+} √(g)/(θ f)?  (보기 ④=√π/2)
# P=(cosθ,sinθ), H=(cosθ,0) → f=½ sinθ cosθ.  접선 ∩ x축: Q=(secθ,0), QA=secθ-1.
# OP⊥PQ, ∠POQ=θ → ∠OQP=π/2-θ = 부채꼴 중심각. g=½ (secθ-1)^2 (π/2-θ).
CANDIDATE = sp.sqrt(sp.pi) / 2
th = sp.symbols('theta', positive=True)
f = sp.Rational(1, 2) * sp.sin(th) * sp.cos(th)
g = sp.Rational(1, 2) * (1 / sp.cos(th) - 1) ** 2 * (sp.pi / 2 - th)
L = sp.limit(sp.sqrt(g) / (th * f), th, 0, '+')
print('VERIFY_PASS' if sp.simplify(L - CANDIDATE) == 0 else 'VERIFY_FAIL')
