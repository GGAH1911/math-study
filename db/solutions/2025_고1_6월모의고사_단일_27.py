from sympy import symbols, solve, Rational

a, b, x = symbols('a b x', real=True)

# 주어진 함수
def f(x_val, a_val, b_val):
    return (x_val - a_val)**2 + 2*b_val

count = 0
valid_pairs = []

# 자연수 쌍 (a, b) 검사
for a_val in range(1, 20):  # a는 자연수
    for b_val in range(1, 20):  # b는 자연수
        # 구간 [-2, 2]에서 최솟값, 최댓값 계산
        f_neg2 = f(-2, a_val, b_val)
        f_2 = f(2, a_val, b_val)
        
        # 꼭짓점이 구간 내에 있는지 확인
        if -2 <= a_val <= 2:
            m = f(a_val, a_val, b_val)  # 최솟값
        elif a_val < -2:
            m = f_neg2  # 최솟값
        else:  # a_val > 2
            m = f_2  # 최솟값
        
        M = max(f_neg2, f_2)  # 최댓값
        
        # 조건 확인
        if m >= 5 and M <= 36:
            valid_pairs.append((a_val, b_val))
            count += 1

# 정답 확인
expected_answer = 23
if count == expected_answer:
    print("VERIFY_PASS")
else:
    print(f"VERIFY_FAIL: expected {expected_answer}, got {count}")
    print(f"Valid pairs: {valid_pairs[:30]}")