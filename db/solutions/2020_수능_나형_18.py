import sympy as sp

# 2020 수능 나형 18 (자기닮음 등비급수): lim S_n?  (보기 ⑤ = 100/9 (2-√3+π/3))
# 좌표 A(0,0),B(5,0),C(5,5),D(0,5). 부채꼴 ABD 중심A r=5.
# A1=(0,3) (AD 3:2 내분), y=3 ∩ 호(x²+y²=25): B1=(4,3) → 정사각형 A1B1C1D1 변=4, 닮음비 4/5.
# 부채꼴 D1A1C1 중심 D1=(0,7) r=4. DC(y=5) ∩ 호 A1C1: E1=(2√3,5); ∩ B1C1(x=4): F1=(4,5).
# 색칠1 (x=0,y=5,호 A1E1) = ∫_3^5 arc;  색칠2 (y=5,x=4,호 E1C1) = ∫_5^7 (4-arc).
CANDIDATE = sp.Rational(100, 9) * (2 - sp.sqrt(3) + sp.pi / 3)
y = sp.symbols('y')
arc = sp.sqrt(16 - (y - 7) ** 2)            # 호의 x좌표 (중심 D1=(0,7), 반지름 4)
S1 = sp.integrate(arc, (y, 3, 5)) + sp.integrate(4 - arc, (y, 5, 7))
ratio = sp.Rational(4, 5) ** 2               # 면적 닮음비 (변 4/5)
lim = S1 / (1 - ratio)
print('VERIFY_PASS' if sp.simplify(lim - CANDIDATE) == 0 else 'VERIFY_FAIL')
