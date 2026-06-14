from sympy import log, sqrt, simplify, Rational, nsimplify
import sympy as sp

CANDIDATE = Rational(3, 2)

# 원래 함수: log_2(sqrt(8))
# 로그의 정의: log_a(x) = y <=> a^y = x
# 따라서 log_2(sqrt(8)) = CANDIDATE 이면,
# 2^CANDIDATE = sqrt(8) 이어야 한다.

original_arg = sqrt(8)
result_from_definition = 2 ** CANDIDATE

# 양쪽을 간단히 한다
left = simplify(result_from_definition)
right = simplify(original_arg)

# 수치적으로 확인
left_float = float(left)
right_float = float(right)

if abs(left_float - right_float) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')