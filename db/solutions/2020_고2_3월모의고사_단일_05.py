# 대응 그림: f(5)+(f∘f)(9)? (보기②=16)
f = {1: 5, 3: 7, 5: 9, 7: 1, 9: 3}
CANDIDATE = 16
print('VERIFY_PASS' if f[5] + f[f[9]] == CANDIDATE else 'VERIFY_FAIL')
