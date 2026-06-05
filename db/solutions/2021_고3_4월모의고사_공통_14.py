from sympy import symbols, simplify

m = symbols('m', integer=True, positive=True)

# 정의된 함수들
def f(m_val):
    return m_val - 1

def g(m_val):
    return m_val * (m_val - 1)

def h(m_val):
    return m_val**2

# 직접 조건 검증: n=4~20에서 T_n 합이 614인지 확인
total = 0
for n in range(4, 21):
    if n % 2 == 0:
        m_val = n // 2
        T_n = m_val * (m_val - 1)
    else:
        m_val = (n - 1) // 2
        T_n = m_val**2
    total += T_n

assert total == 614, f'Sum check failed: {total} != 614'

# 최종 답 계산
answer = f(5) + g(6) + h(7)
assert answer == 83, f'Answer check failed: {answer} != 83'
print('VERIFY_PASS')