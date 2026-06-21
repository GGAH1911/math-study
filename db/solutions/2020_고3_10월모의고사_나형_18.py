from sympy import symbols, binomial, simplify, Eq, solve
from fractions import Fraction

# A_n 정의: (p, q) 쌍으로 p < q, p,q ∈ {1,...,n}
# |A_n| = C(n,2) = n(n-1)/2

def compute_a_n(n):
    """직접 계산: A_n의 모든 q 값 평균"""
    total = 0
    count = 0
    for q in range(2, n+1):
        for p in range(1, q):
            total += q
            count += 1
    return Fraction(total, count)

def compute_a_n_formula(n):
    """공식: a_n = (2n+2)/3"""
    return Fraction(2*n+2, 3)

# 검증: 공식이 맞는지 확인
for n in range(3, 8):
    direct = compute_a_n(n)
    formula = compute_a_n_formula(n)
    assert direct == formula, f"n={n}에서 불일치: {direct} vs {formula}"

# (가) = |A_k| = C(k,2) = k(k-1)/2
def f(k):
    return k*(k-1)//2

# (나) = k(k+1)  (새 원소 k개의 q값 합 = k * (k+1))
def g(k):
    return k*(k+1)

# 검증: a_{k+1} 공식 확인
def verify_induction(k):
    """a_{k+1} = (2(k+1)+2)/3 확인"""
    a_k = Fraction(2*k+2, 3)
    elements_k = f(k)  # |A_k|
    new_element_sum = g(k)  # 새로 추가되는 k개 원소의 q값 합
    
    numerator = a_k * elements_k + new_element_sum
    denominator = binomial(k+1, 2)
    a_k_plus_1 = numerator / denominator
    expected = Fraction(2*(k+1)+2, 3)
    
    return a_k_plus_1 == expected

for k in range(3, 10):
    assert verify_induction(k), f"k={k}에서 귀납 검증 실패"

# 최종 답: f(10) + g(9)
answer = f(10) + g(9)
assert answer == 135, f"계산 오류: {answer}"

print('VERIFY_PASS')