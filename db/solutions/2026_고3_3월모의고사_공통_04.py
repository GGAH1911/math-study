import sympy as sp
a = 2
# x=2에서의 좌극한
left_limit = a * (2**2) - 2
# x=2에서의 함수값
function_value = 3 * 2
# 연속성 확인
if left_limit == function_value:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')