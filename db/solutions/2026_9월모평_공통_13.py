import sympy as sp

x = sp.symbols('x')
f = x**2 + 6*x + 12

def check_condition(k_val):
    # g(x) = f(x) - k(x+2) = x^2 + (6-k)x + (12-2k)
    coeff_b = 6 - k_val
    coeff_c = 12 - 2*k_val
    
    # 판별식
    delta = coeff_b**2 - 4*coeff_c
    
    # 극한이 존재하는 조건
    if delta < 0:
        return True  # 실근 없음
    elif delta == 0:
        root = -coeff_b / 2  # 중근
        return root == 0  # 중근이 0인지 확인
    else:
        return False  # 0이 아닌 실근 존재

# 정수 k에서 조건을 만족하는 개수
valid_k = [k for k in range(-10, 15) if check_condition(k)]
count = len(valid_k)

print(f"조건을 만족하는 정수 k: {valid_k}")
print(f"개수: {count}")

if count == 8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')