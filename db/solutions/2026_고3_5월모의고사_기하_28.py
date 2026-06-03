from sympy import *
a = Rational(1,4)/sqrt(2)  # 24a*sqrt(2)=6 => a=1/(4*sqrt(2))
A = Matrix([24*a, 24*a])
B = Matrix([0, 0])
F = Matrix([3*a, 4*a])
O = Matrix([0, 0])
OA = (A - O).norm()
AF = (A - F).norm()
BF = (B - F).norm()
# Verify original parabola equations at A and B
# C1: (y-4a)^2 = 16a*(x+a)
aa = Rational(1,4)/sqrt(2)
C1_A = (24*aa - 4*aa)**2 - 16*aa*(24*aa + aa)
C1_B = (0 - 4*aa)**2 - 16*aa*(0 + aa)
C2_A = (24*aa - 3*aa)**2 - 9*aa*(2*24*aa + aa)
C2_B = (0 - 3*aa)**2 - 9*aa*(2*0 + aa)
cond_OA = simplify(OA - 6) == 0
cond_ans = simplify(AF - BF - 3*sqrt(2)) == 0
cond_C1 = simplify(C1_A) == 0 and simplify(C1_B) == 0
cond_C2 = simplify(C2_A) == 0 and simplify(C2_B) == 0
cond_order = simplify(AF - BF) > 0
if cond_OA and cond_ans and cond_C1 and cond_C2 and cond_order:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL OA={simplify(OA)} ans={simplify(AF-BF)} C1A={simplify(C1_A)} C1B={simplify(C1_B)} C2A={simplify(C2_A)} C2B={simplify(C2_B)}')