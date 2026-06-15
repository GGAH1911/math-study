from sympy import Eq, simplify

CANDIDATE = 2

# 집합 A, B 정의
A = {2, 3, 4}
B = {3, 4, 5, 6}

# 교집합 계산: A∩B = {3, 4}
intersection = A & B

# 핵심 관계식: n(A∩B)의 값
# 교집합의 원소 개수를 계산
n_intersection = len(intersection)

# CANDIDATE 검증
# 핵심 등식: n(A∩B) = CANDIDATE
equation = Eq(n_intersection, CANDIDATE)

# 등식 검증
if simplify(equation):
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")