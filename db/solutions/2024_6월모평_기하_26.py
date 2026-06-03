from sympy import *
x, y, t = symbols('x y t', real=True)
# 타원 C 위의 P 구하기
P_sols = solve([(x-4)**2/144 + y**2/80 - 1, (x+4)**2 + y**2 - 256], [x, y])
# P = (10, 2*sqrt(15)) 사용
P = Matrix([10, sqrt(60)])
F  = Matrix([12, 0])
Fp = Matrix([-4, 0])
# |PF| 확인
PF = (P - F).norm()
assert simplify(PF - 8) == 0, f'PF={PF} != 8'
# |F'P| 확인
PFp = (P - Fp).norm()
assert simplify(PFp - 16) == 0, f"F'P={PFp} != 16"
# Q = 중점
Q = (Fp + P) / 2  # (3, sqrt(15))
assert simplify(Q[0]-3)==0 and simplify(Q[1]-sqrt(15))==0, f'Q={Q}'
# 새 타원 조건
a2_val, b2_val = symbols('a2 b2', positive=True)
sol = solve([a2_val - b2_val - 16, Q[0]**2/a2_val + Q[1]**2/b2_val - 1], [a2_val, b2_val])
if isinstance(sol, list):
    sol = {a2_val: sol[0][0], b2_val: sol[0][1]}
a2 = float(sol[a2_val])
b2 = float(sol[b2_val])
assert abs(a2-36)<1e-9, f'a^2={a2}'
assert abs(b2-20)<1e-9, f'b^2={b2}'
final = 8 + a2 + b2
if abs(final-64)<1e-6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
