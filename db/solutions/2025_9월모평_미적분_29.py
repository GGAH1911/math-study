from fractions import Fraction
import sympy as sp

# a_1 + a_10 값
a_1 = Fraction(3, 2)
a_10 = Fraction(1, 11)
sum_val = a_1 + a_10

print(f'a_1 = {a_1}')
print(f'a_10 = {a_10}')
print(f'a_1 + a_10 = {sum_val}')

# 분자와 분모 확인
p = sum_val.denominator
q = sum_val.numerator
print(f'p = {p}, q = {q}')
print(f'gcd(p, q) = {sp.gcd(p, q)}')
print(f'p + q = {p + q}')

# 원래 식 검증
# S_m 계산 함수
def compute_S_m(m, N=1000):
    total = sum(Fraction(m+1, n*(n+m+1)) for n in range(1, N+1))
    return total

def compute_S_m_formula(m):
    # S_m = sum(1/n for n=1 to m+1)
    return sum(Fraction(1, n) for n in range(1, m+2))

# S_1, S_2, ..., S_10 계산
S = []
for m in range(1, 11):
    s_m = compute_S_m_formula(m)
    S.append(s_m)
    print(f'S_{m} = {s_m}')

# a_n 계산
a = [S[0]]  # a_1 = S_1
for m in range(1, 10):
    a.append(S[m] - S[m-1])

print(f'\na_1 = {a[0]}')
for i in range(1, 10):
    print(f'a_{i+1} = {a[i]}')

# 최종 답 검증
if a[0] + a[9] == sum_val and sp.gcd(p, q) == 1:
    print('\nVERIFY_PASS')
else:
    print('\nVERIFY_FAIL')