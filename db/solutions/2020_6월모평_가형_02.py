import sympy as sp

x = sp.Symbol('x')
f = 7 + 3*sp.ln(x)

# f'(x) 구하기
f_prime = sp.diff(f, x)

# f'(3) 계산
result = f_prime.subs(x, 3)

# 검증: 결과가 1인지 확인
if result == 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')