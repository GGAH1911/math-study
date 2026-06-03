import sympy as sp
x = sp.symbols('x')
f = sp.sqrt(sp.sec(x)**2 + sp.tan(x))  # 원래 곡선 y
cross_section_area = f**2  # 정사각형 단면의 넓이
V = sp.integrate(cross_section_area, (x, 0, sp.pi/3))
V_simplified = sp.simplify(V)
answer = sp.sqrt(3) + sp.ln(2)
if sp.simplify(V_simplified - answer) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print('Computed:', V_simplified)
    print('Expected:', answer)
