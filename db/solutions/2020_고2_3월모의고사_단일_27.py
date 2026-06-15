# '어떤 x: x²+8x+2k-1<=0' 거짓 ⟺ 모든 x>0 ⟺ D<0. 정수 k 최솟값?
CANDIDATE = 9
k = next(k for k in range(-100, 100) if 64 - 4*(2*k-1) < 0)
print('VERIFY_PASS' if k == CANDIDATE else 'VERIFY_FAIL')
