import sympy as sp
x = sp.Symbol('x', real=True, positive=True)

# 원래 함수: y = 2^(x-2) + 3
# 역함수: y = 2 + log_2(x-3)
# 주어진 함수: y = log_2(4x-12)

# log_2(4x-12)를 전개
log_expr = sp.log(4*x - 12, 2)
expanded = sp.log(4, 2) + sp.log(x - 3, 2)  # log_2(4) + log_2(x-3) = 2 + log_2(x-3)

# 검증: log_2(4x-12) = 2 + log_2(x-3)인지 확인
diff = sp.simplify(log_expr - expanded)
if diff == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')