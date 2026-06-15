# 조건 p와 q의 관계: p ⟹ q ⟺ P ⊆ Q
# P = [a-1, a+1], Q = (-∞, 10)
# P ⊆ Q ⟺ a+1 < 10 ⟺ a < 9

import sympy as sp
a = sp.Symbol('a', integer=True)

# 조건: P의 최댓값이 Q의 상한보다 작아야 함
# P = [a-1, a+1]에서 우측 끝점 a+1
# Q = (-∞, 10)에서 상한 10
# 포함 조건: a+1 < 10

ineq = a + 1 < 10
sol = sp.solve(ineq, a)
print(f"a < 9인 경우, 정수 a의 최댓값: 8")

# 검증
for test_a in [7, 8, 9]:
    p_right = test_a + 1
    is_valid = p_right < 10
    print(f"a = {test_a}: a+1 = {p_right}, [a-1, a+1] ⊆ (-∞, 10)? {is_valid}")

if 8 < 9:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")