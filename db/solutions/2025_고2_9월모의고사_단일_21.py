from sympy import *

B = Matrix([0, 0])
C = Matrix([3, 0])
A = Matrix([1, sqrt(3)])
D = Matrix([Rational(20, 7), 4*sqrt(3)/7])

R = sqrt(21)/3
center = Matrix([Rational(3,2), 1/(2*sqrt(3))])

for P, name in [(A,'A'),(B,'B'),(C,'C'),(D,'D')]:
    d2 = (P-center).dot(P-center)
    assert simplify(d2 - R**2) == 0, f'{name} not on C1'

assert simplify((A-B).dot(A-B) - 4) == 0
assert simplify((A-C).dot(A-C) - 7) == 0

BC = simplify(sqrt((B-C).dot(B-C)))
CD = simplify(sqrt((C-D).dot(C-D)))
BD = simplify(sqrt((B-D).dot(B-D)))

assert BC > CD, f'BC={BC} > CD={CD} 위반'

area = simplify(Rational(1,2)*((C-B)[0]*(D-B)[1]-(C-B)[1]*(D-B)[0]))
s = (BC + CD + BD) / 2
r = simplify(area / s)

I = simplify((CD*B + BD*C + BC*D) / (CD + BD + BC))
line_val = simplify(sqrt(3)*I[0] + 2*I[1] - 3*sqrt(3))
assert line_val == 0, f'내심이 AC 위에 없음: {line_val}'

r_ans = sqrt(3) - Rational(2,7)*sqrt(21)
if simplify(r - r_ans) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'r={r}, ans={r_ans}')
