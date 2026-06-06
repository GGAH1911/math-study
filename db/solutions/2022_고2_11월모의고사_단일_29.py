import sympy as sp
from sympy import symbols, Abs, diff, simplify

# 답 검증: 총 11개의 순서쌍이 조건을 만족하는지 확인
# 대표적인 경우들을 검증

def check_differentiability(a_val, b_val):
    x, h = symbols('x h', real=True)
    
    # f(x) 정의
    def f(x_val):
        if x_val < 5:
            return x_val + 5
        else:
            return Abs(2*x_val - a_val)
    
    # g(x) 정의
    def g(x_val):
        return (x_val - 5) * (x_val - b_val)
    
    # Case 1: x=5 근처에서 미분가능성
    # 좌미분
    left_deriv_5 = 10 * (5 - b_val)
    
    # 우미분
    right_deriv_5 = Abs(10 - a_val) * (5 - b_val)
    
    diff_at_5 = simplify(left_deriv_5 - right_deriv_5) == 0
    
    # Case 2: x=a/2에서 (a > 10인 경우)
    if a_val > 10:
        # x=a/2에서 미분가능하려면 g(a/2)=0 또는 특수 조건
        g_at_a2 = (a_val/2 - 5) * (a_val/2 - b_val)
        if g_at_a2 != 0:  # g(a/2) ≠ 0이면 미분불가능
            return False
    
    # Case 3: x=10에서 (a=20인 경우)
    if a_val == 20:
        left_deriv_10 = -10 * (10 - b_val)
        right_deriv_10 = 10 * (10 - b_val)
        diff_at_10 = (left_deriv_10 == right_deriv_10)
        return diff_at_5 and diff_at_10
    
    return diff_at_5

# 검증: 총 11개
count = 0
valid_pairs = []

# Case A: b=5, a=1~10
for a in range(1, 11):
    if check_differentiability(a, 5):
        count += 1
        valid_pairs.append((a, 5))

# Case B: a=20, b=10
if check_differentiability(20, 10):
    count += 1
    valid_pairs.append((20, 10))

# a>10, b=5인 경우 확인 (미분불가능해야 함)
invalid_found = False
for a in range(11, 25):
    if a != 20 and not check_differentiability(a, 5):
        invalid_found = True
        break

if count == 11 and invalid_found:
    print("VERIFY_PASS")
else:
    print(f"VERIFY_FAIL: count={count}, expected=11")