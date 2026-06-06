import sympy as sp

def a_n(n):
    if n % 5 == 0:
        return -4*n + 10
    else:
        return n

def S_m(m):
    return sum(a_n(k) for k in range(1, m+1))

valid_m_values = []
for m in range(1, 100):
    s = S_m(m)
    if 20 <= s < 30:
        valid_m_values.append(m)

if valid_m_values == [8, 12, 21, 26]:
    answer_sum = sum(valid_m_values)
    if answer_sum == 67:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')