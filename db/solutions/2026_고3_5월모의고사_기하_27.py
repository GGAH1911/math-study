from sympy import *

c = Integer(8)
a = c / 2          # 4
b_sq = 3 * a**2   # 48
b = sqrt(b_sq)    # 4*sqrt(3)

# Foci
F  = Matrix([c, 0])
Fp = Matrix([-c, 0])

# Asymptote slopes
sl = b / a   # sqrt(3)
sm = -b / a  # -sqrt(3)

# P: intersection of line through F (slope sm) with l (y = sl*x)
x_P = c / 2
y_P = sl * x_P
P = Matrix([x_P, y_P])

# Check angle F'PF = pi/2
PF  = F  - P
PFp = Fp - P
dot = PF.dot(PFp)

# Q: intersection of line with hyperbola
# Line: y = sm*(x-c), substituting into 4x^2/c^2 - 4y^2/(3c^2) = 1
# 4x^2 - 4(x-c)^2 = c^2  =>  8cx = 5c^2  =>  x = 5c/8
x_Q = Rational(5,8) * c
y_Q = sm * (x_Q - c)
Q = Matrix([x_Q, y_Q])

# Check Q on hyperbola
on_hyp = x_Q**2 / a**2 - y_Q**2 / b_sq

# Check PQ = 2
PQ_dist = sqrt((x_Q - x_P)**2 + (y_Q - y_P)**2)

cond1 = simplify(dot) == 0
cond2 = simplify(on_hyp - 1) == 0
cond3 = simplify(PQ_dist - 2) == 0

if cond1 and cond2 and cond3:
    print('VERIFY_PASS')
else:
    print(f'dot={dot}, on_hyp={on_hyp}, PQ={PQ_dist}')
    print('VERIFY_FAIL')
