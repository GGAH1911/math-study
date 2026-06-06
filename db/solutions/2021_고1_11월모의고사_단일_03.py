# 문제 원래 조건: f: X->X, X={1,3,5,7}
# 그림에서 읽은 함수 정의
f = {1: 5, 3: 1, 5: 7, 7: 3}

# f는 함수여야 한다 (모든 원소에 대해 정의)
X = {1, 3, 5, 7}
assert set(f.keys()) == X, 'domain mismatch'
assert set(f.values()) == X, 'not a bijection'

# 역함수
f_inv = {v: k for k, v in f.items()}

# 검증: f(3) + f^{-1}(3)
result = f[3] + f_inv[3]

if result == 8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
