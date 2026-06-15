from sympy import symbols, Abs, solve
import sympy as sp

# 변수 선언
x = sp.Symbol('x', real=True)

# 원래 부등식: |x-2| < 3
def original_inequality(val):
    """원래 부등식 |x-2| < 3을 만족하는지 확인"""
    return abs(val - 2) < 3

# sympy로 부등식 풀기
inequality = Abs(x - 2) < 3
solution_interval = solve(inequality, x)
print(f"부등식 |x-2| < 3의 해: {solution_interval}")

# 이 구간에 속하는 정수 찾기
# 부등식을 풀면: -3 < x-2 < 3 → -1 < x < 5
integer_solutions = []
for i in range(-100, 100):
    if original_inequality(i):
        integer_solutions.append(i)

print(f"조건을 만족하는 정수들: {integer_solutions}")

# 답: 정수의 개수
answer = len(integer_solutions)
print(f"정수의 개수: {answer}")

# 검증
all_valid = all(original_inequality(i) for i in integer_solutions)
correct_count = (answer == 5)
correct_values = (integer_solutions == [0, 1, 2, 3, 4])

if all_valid and correct_count and correct_values:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")