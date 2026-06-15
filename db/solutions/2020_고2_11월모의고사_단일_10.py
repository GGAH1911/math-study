# a1=4, a_{n+1}=a_n-3 (a_n>=6), (a_n-1)^2 (a_n<6). a10? (보기 ⑤=9)
CANDIDATE = 9
a = 4
for _ in range(9):
    a = a-3 if a >= 6 else (a-1)**2
print('VERIFY_PASS' if a == CANDIDATE else 'VERIFY_FAIL')
