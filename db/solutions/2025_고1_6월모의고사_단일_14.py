import sympy as sp
from sympy import sqrt, symbols, solve, simplify

# 변의 길이
a, b, c = sqrt(2), sqrt(2), 2*sqrt(2)

# 조건 검증
edge_sum = 4*(a + b + c)
volume = a*b*c
diagonal_sq = a**2 + b**2 + c**2
diagonal = sqrt(diagonal_sq)

print(f"모서리 합: {edge_sum} (목표: 16√2)")
print(f"부피: {volume} (목표: 4√2)")
print(f"대각선: {diagonal} (목표: 2√3)")

# 넓이 계산
S1 = a*b
S2 = a*c
S3 = b*c

print(f"S1 = {S1}")
print(f"S2 = {S2}")
print(f"S3 = {S3}")

# 답 계산
answer = S1**2 + S2**2 + S3**2
answer_simplified = simplify(answer)

print(f"S1² + S2² + S3² = {answer_simplified}")

# 검증
if edge_sum == 16*sqrt(2) and volume == 4*sqrt(2) and diagonal == 2*sqrt(3) and answer_simplified == 36:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")