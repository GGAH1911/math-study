from sympy import symbols, Eq, solve

# 구한 수열
a = [0, 2, 4, 12, 36, 108]
S = [0]
for i in range(1, 6):
    S.append(sum(a[1:i+1]))

# 점화식 a_{n+1}*S_n = a_n*S_{n+1} 검증 (n >= 2)
verified = True
for n in range(2, 5):
    lhs = a[n+1] * S[n]
    rhs = a[n] * S[n+1]
    if lhs != rhs:
        verified = False
        break

if verified and S[5] == 162:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')