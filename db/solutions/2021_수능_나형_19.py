from sympy import symbols, erf, sqrt, N

def phi(z):
    '''표준정규분포의 누적분포함수: Φ(z) = (1 + erf(z/√2))/2'''
    return (1 + erf(z/sqrt(2)))/2

# P(Z ≤ 2) 계산
z_target = 2
result = float(N(phi(z_target), 15))

# 표에서 주어진 P(0 ≤ Z ≤ 2.0) = 0.4772이므로 P(Z ≤ 2) = 0.9772
expected = 0.9772

if abs(result - expected) < 0.0001:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: {result} vs {expected}')