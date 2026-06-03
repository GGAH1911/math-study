from sympy import symbols, solve

# 함수 f를 딕셔너리로 정의
f = {1: 2, 2: 3, 3: 5, 4: 1, 5: 4}
f_inv = {v: k for k, v in f.items()}

# 조건 1 검증: f(1) + 2*f(3) = 12
cond1 = f[1] + 2*f[3]
assert cond1 == 12, f'조건 1 실패: {cond1}'

# 조건 2 검증: f^(-1)(1) - f^(-1)(3) = 2
cond2 = f_inv[1] - f_inv[3]
assert cond2 == 2, f'조건 2 실패: {cond2}'

# 역함수 존재 확인 (전단사)
assert len(set(f.values())) == 5, '전단사 아님'

# 최종 답 계산
result = f[4] + f_inv[4]
assert result == 6, f'최종 계산 실패: {result}'

print('VERIFY_PASS')