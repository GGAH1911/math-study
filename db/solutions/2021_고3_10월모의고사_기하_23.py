import sympy as sp
m = sp.Symbol('m')
# 벡터 a와 b의 성분
a1, a2 = m - 2, 3
b1, b2 = 2*m + 1, 9
# 평행 조건: a1*b2 - a2*b1 = 0
parallel_condition = a1 * b2 - a2 * b1
solution = sp.solve(parallel_condition, m)
m_val = solution[0]
# m=7에서 검증
a_vec = (m_val - 2, 3)
b_vec = (2*m_val + 1, 9)
# 외적이 0인지 확인
cross_product = a_vec[0] * b_vec[1] - a_vec[1] * b_vec[0]
if cross_product == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')