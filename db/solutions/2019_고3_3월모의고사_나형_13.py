from sympy import symbols, limit, floor, oo

n, m = symbols('n m', integer=True, positive=True)
a = floor(m/5)

# 극한 계산
limit_expr = ((n+1)*a + 2*n) / (n*a + 1)
limit_val = limit(limit_expr, n, oo)

# 극한이 2가 되는 조건
valid_count = 0
for m_val in range(1, 100):
    a_val = int(m_val / 5)  # floor(m/5)
    if a_val > 0:
        lim = (a_val + 2) / a_val
        if abs(lim - 2.0) < 1e-10:
            if 10 <= m_val < 15:
                valid_count += 1

# a=2일 때만 극한이 2
if valid_count == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')