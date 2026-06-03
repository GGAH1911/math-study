import numpy as np

# 문제의 원래 식 계산
original_expr = (1 + 2j) - 5j

# 우리의 답
our_answer = 1 - 3j

# 검증
if original_expr == our_answer:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')