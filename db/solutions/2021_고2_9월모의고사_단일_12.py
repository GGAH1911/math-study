import math

# 주어진 조건: a_8 = 5
# 역계산으로 a_7, a_6 구하기

# n=7은 홀수이므로 a_8 = log_2(a_7)
a_8 = 5
a_7 = 2**a_8
assert a_7 == 32, f"a_7 should be 32, got {a_7}"

# n=6은 짝수이므로 a_7 = 2^(a_6+1)
# 32 = 2^(a_6+1)에서 a_6+1 = 5, a_6 = 4
a_6 = 4
assert 2**(a_6+1) == a_7, f"a_7 should be {a_7}, got {2**(a_6+1)}"

# 최종 답
answer = a_6 + a_7
assert answer == 36, f"answer should be 36, got {answer}"

print('VERIFY_PASS')