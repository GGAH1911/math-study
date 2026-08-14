import sympy as sp

A = sp.Matrix([0,6])
B = sp.Matrix([0,0])
C = sp.Matrix([8,0])
D = sp.Matrix([8,6])

# 조건 (나)
BA = A - B
AD = D - A
Q = B + (2*BA + 3*AD)/sp.Integer(10)

# 조건 (가): PQ . QA = 0, P=(8,p) on CD
p = sp.symbols('p', real=True)
P = sp.Matrix([8, p])
QA = A - Q
PQ = Q - P
eq = sp.Eq(PQ.dot(QA), 0)
p_val = sp.solve(eq, p)[0]
P = sp.Matrix([8, p_val])
assert 0 <= p_val <= 6

# 검산: 원래 조건 (가)
PA = A - P
PQ2 = Q - P
assert sp.simplify(PA.dot(PQ2) - PQ2.dot(PQ2)) == 0

# R의 자취: 지름이 M1M2인 원
M1 = (A+Q)/2
M2 = (P+Q)/2
O = (M1+M2)/2
r = sp.sqrt((M2-M1).dot(M2-M1))/2

QP = P - Q
QPnorm = sp.sqrt(QP.dot(QP))

Mval = O.dot(QP) + r*QPnorm
mval = O.dot(QP) - r*QPnorm

result = sp.nsimplify(sp.simplify(Mval+mval))
target = sp.Rational(266,5)

print(result)
if sp.simplify(result - target) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')