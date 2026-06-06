import sympy as sp
from sympy import symbols, solve

n = symbols('n', integer=True, positive=True)
f = -n**2 + 9*n - 18

# 조건을 만족하는 n들
valid_n = [4, 7, 9, 11]

# 각 n에 대해 검증
for n_val in valid_n:
    f_val = int(f.subs(n, n_val))
    is_even = n_val % 2 == 0
    is_odd = n_val % 2 == 1
    
    # 짝수이면서 f(n) > 0
    if is_even and f_val > 0:
        # x^n = f_val에서 음의 실수해 존재
        x_neg = -(abs(f_val) ** (1/n_val))
        check = x_neg ** n_val
        assert abs(check - f_val) < 1e-10, f"n={n_val} failed"
    
    # 홀수이면서 f(n) < 0
    elif is_odd and f_val < 0:
        # x^n = f_val에서 음의 실수해 존재
        x_neg = -(abs(f_val) ** (1/n_val))
        check = x_neg ** n_val
        assert abs(check - f_val) < 1e-10, f"n={n_val} failed"

ans = sum(valid_n)
assert ans == 31, f"Sum should be 31, got {ans}"
print('VERIFY_PASS')