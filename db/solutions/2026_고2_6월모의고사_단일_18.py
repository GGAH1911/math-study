import sympy as sp

AB = sp.Integer(2)
R = sp.Rational(3) * sp.sqrt(3) / 5

# p = sin(θ1+θ2) from sine rule in triangle PAB
p = sp.simplify(AB / (2 * R))
# Should be 5√3/9
assert sp.simplify(p - 5*sp.sqrt(3)/9) == 0, f'p wrong: {p}'

# cos(θ1+θ2)
cos_sum = sp.simplify(sp.sqrt(1 - p**2))
assert sp.simplify(cos_sum - sp.sqrt(6)/9) == 0, f'cos wrong: {cos_sum}'

# q = sin θ1 / sin θ2 = √3/√2 = √6/2
q = sp.sqrt(sp.Rational(3, 2))
assert sp.simplify(q - sp.sqrt(6)/2) == 0, f'q wrong: {q}'

# r^2 = 24/19 from cosine rule in triangle QAB
# 4 = a^2*(1 + 3/2 + 2/3) = a^2*(19/6)
r_sq = sp.Rational(24, 19)

# Verify cosine rule
a = sp.sqrt(r_sq)
QB = q * a
cos_AQB = -cos_sum
lhs = AB**2
rhs = sp.simplify(a**2 + QB**2 - 2*a*QB*cos_AQB)
assert sp.simplify(lhs - rhs) == 0, f'cosine rule fail: lhs={lhs}, rhs={rhs}'

# Final result
result = sp.simplify(p * q * r_sq)
expected = 20 * sp.sqrt(2) / 19

if sp.simplify(result - expected) == 0:
    print('VERIFY_PASS')
else:
    print(f'result={result}, expected={expected}')
    print('VERIFY_FAIL')
