from sympy import symbols, solve

# 4줄의 값들이 모두 2배 규칙을 따르는지 검증
row4 = [1, 2, 4, 8, 16, 32, 64]

# 가로 인접 확인 (각 칸이 다음 칸의 절반)
for i in range(len(row4)-1):
    assert row4[i] * 2 == row4[i+1], f'가로 규칙 위반: {row4[i]} × 2 ≠ {row4[i+1]}'

# 세로 인접 확인 (3줄 ↔ 4줄)
row3 = [1, 2, 4, 8, 16]
for i in range(len(row3)):
    assert row3[i] * 2 == row4[i+1], f'세로 규칙 위반: {row3[i]} × 2 ≠ {row4[i+1]}'

# 합 계산
total = sum(row4)
assert total == 127, f'합 계산 오류: {total}'

print('VERIFY_PASS')