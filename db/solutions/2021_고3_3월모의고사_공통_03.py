import math
from sympy import sin, pi, solve, symbols, N

x = symbols('x', real=True)
eq = sin(4*x) - 0.5

# 수치적으로 [0, 2π) 구간에서 모든 근을 찾기
roots = []
for n in range(8):
    root1 = pi/24 + n*pi/2
    root2 = 5*pi/24 + n*pi/2
    
    val1 = float(N(root1))
    val2 = float(N(root2))
    
    if 0 <= val1 < 2*math.pi:
        roots.append(val1)
    if 0 <= val2 < 2*math.pi:
        roots.append(val2)

roots = sorted(set([round(r, 10) for r in roots]))

# 각 근이 원래 방정식을 만족하는지 확인
verify_count = 0
for root in roots:
    check = abs(math.sin(4*root) - 0.5)
    if check < 1e-10:
        verify_count += 1

if verify_count == 8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')