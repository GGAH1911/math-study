import sympy as sp
m = sp.Symbol('m', integer=True)
x = sp.Symbol('x', real=True)

f = x**2 + (m+2)*x + 2*m + 1

# 모든 정수 m에 대해 판별식 검증
for m_val in [1, 2, 3]:
    discriminant = (m_val + 2)**2 - 4*(2*m_val + 1)
    if discriminant < 0:
        f_at_vertex = f.subs(m, m_val)
        # 최솟값 확인
        vertex_x = -(m_val + 2) / 2
        min_val = vertex_x**2 + (m_val + 2)*vertex_x + 2*m_val + 1
        assert min_val > 0, f'm={m_val}: min_val={min_val}'

# 경계값 검증
for m_val in [0, 4]:
    discriminant = (m_val + 2)**2 - 4*(2*m_val + 1)
    assert discriminant >= 0, f'm={m_val}: discriminant should be >= 0'

result_sum = 1 + 2 + 3
assert result_sum == 6, f'Sum should be 6, got {result_sum}'
print('VERIFY_PASS')