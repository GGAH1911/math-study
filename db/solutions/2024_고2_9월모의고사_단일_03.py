# 등차수열 검증
a1 = 1
d = 3

# 조건 1: a4 = 10
a4 = a1 + (4-1) * d
assert a4 == 10, f'a4={a4}, expected 10'

# 조건 2: a7 - a5 = 6
a7 = a1 + (7-1) * d
a5 = a1 + (5-1) * d
diff = a7 - a5
assert diff == 6, f'a7-a5={diff}, expected 6'

print('VERIFY_PASS')