from sympy import *

# 변수 정의
x = symbols('x')

# 방정식 8^x = 18을 log2 이용하여 풀기
# 8^x = 2^(3x) = 18 = 2 * 3^2
# 3x = log2(18) = log2(2) + log2(9) = 1 + 2*log2(3)
# x = 1/3 + (2/3)*log2(3)

# x 값 계산 (sympy 정확값)
log2_3 = log(3, 2)
x_val = Rational(1, 3) + Rational(2, 3) * log2_3

# k 값 결론
k = Rational(2, 3)

# 검증 1: x_val이 실제로 8^x = 18을 만족하는가?
lhs = 8**x_val
rhs = 18
diff = simplify(lhs - rhs)

# 검증 2: x_val = 1/3 + k*log2(3) 을 만족하는 k가 2/3인가
x_expected = Rational(1, 3) + k * log2_3
diff2 = simplify(x_val - x_expected)

if diff == 0 and diff2 == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: lhs-rhs={diff}, x_diff={diff2}')
