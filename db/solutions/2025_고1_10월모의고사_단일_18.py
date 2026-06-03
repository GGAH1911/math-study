from sympy import symbols, expand, solve, Poly

x, a, b, c = symbols('x a b c', real=True)

# 원래 다항식
P = x**3 + (2*a + 3)*x**2 + (3*a + 5)*x + a + 3

# 인수분해된 형태
factored = (x + b) * (x + c)**2
factored_expanded = expand(factored)

# 세 경우를 모두 검증
cases = [(2, 5, 1), (1, 1, 2), (-2, 1, -1)]

for a_val, b_val, c_val in cases:
    # 원래 다항식에 a 값 대입
    P_val = P.subs(a, a_val)
    # 인수분해된 형태에 b, c 값 대입
    factored_val = factored_expanded.subs([(b, b_val), (c, c_val)])
    
    # 두 다항식이 같은지 확인
    assert expand(P_val - factored_val) == 0
    
    # 검증 조건들
    assert b_val * c_val**2 == a_val + 3
    assert 2*c_val + b_val == 2*a_val + 3

# 모든 검증 통과
values = [8, 4, -2]
assert max(values) + min(values) == 6
print('VERIFY_PASS')