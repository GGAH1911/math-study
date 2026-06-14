CANDIDATE = 5
from sympy import *

n = symbols('n', positive=True)

# Points
An = Matrix([n, 0])
Bn = Matrix([n, 3])
P = Matrix([1, 0])
O = Matrix([0, 0])

# Distances
OAn = sqrt((An - O).dot(An - O))  # = n
OBn = sqrt((Bn - O).dot(Bn - O))  # = sqrt(n^2+9)

# Line OBn: y = (3/n)*x
# Intersection with x=1
Cn_y = Rational(3, 1) / n * 1
Cn = Matrix([1, Cn_y])

# PCn length
PCn = sqrt((Cn - P).dot(Cn - P))  # = 3/n

# Numerator and denominator
numerator = PCn
denominator = OBn - OAn

# Compute limit
ratio = simplify(numerator / denominator)
lim_val = limit(ratio, n, oo)
print('limit =', lim_val)

# Check p+q
q_val = Rational(2)
p_val = Rational(3)
pq_sum = p_val + q_val

if lim_val == Rational(2, 3) and pq_sum == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
