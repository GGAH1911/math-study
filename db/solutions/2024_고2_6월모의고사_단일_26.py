import sympy as sp
from sympy import symbols, simplify, nsimplify

# n의 가능한 값들
valid_n = [1, 2, 3, 5, 11]
all_valid = True

for n in valid_n:
    # sqrt[n+1]{8}을 계산
    root_expr = 8 ** (1 / (n + 1))
    
    # 이것이 어떤 자연수의 4제곱근이 되는지 확인
    # (root_expr)^4 = k가 자연수인지 확인
    k = root_expr ** 4
    
    # k는 2^(12/(n+1))이어야 함
    expected_k = 2 ** (12 / (n + 1))
    
    # 정수인지 확인
    if abs(k - round(k)) < 1e-9 and k > 0:
        is_valid = True
    else:
        is_valid = False
        all_valid = False
    
sum_n = sum(valid_n)
if sum_n == 22 and all_valid:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')