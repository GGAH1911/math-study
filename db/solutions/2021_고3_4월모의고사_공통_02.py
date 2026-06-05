d = 2
a1 = 1  # 임의의 값 설정
a2 = a1 + d
a5 = a1 + 4*d
result = a5 - a2
assert result == 6, f'Expected 6, got {result}'
print('VERIFY_PASS')