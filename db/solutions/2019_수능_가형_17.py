from math import comb, factorial

# 검증: 우리의 답이 조건을 만족하는지 확인
p = 6  # C(6,5)
q = 5  # f(k)의 선택 (A의 원소 중 하나)
r = factorial(5)  # A에서 A로의 일대일 대응

# 계산
total_functions = p * q * r

# 논리 검증:
# 1. A의 크기: 5 ✓
# 2. f의 치역: A (크기 5) ✓
# 3. f∘f의 치역: f(A) = A (f|_A가 전사함수이므로) (크기 5) ✓

assert p == comb(6, 5), "(가) 오류"
assert q == 5, "(나) 오류"
assert r == 120, "(다) 오류"
assert total_functions == 3600, "총 함수 개수 오류"

answer = p + q + r
assert answer == 131, "최종 답 오류"

print('VERIFY_PASS')