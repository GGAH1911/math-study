import sympy as sp
a = sp.Symbol('a', positive=True, real=True)
term1 = a/3
term2 = 4*sp.sqrt(2)
term3 = 6*a
ratio1 = term2 / term1
ratio2 = term3 / term2
eq = sp.Eq(ratio1, ratio2)
sol = sp.solve(eq, a)
print(f'Solutions: {sol}')
if 4 in sol:
  a_val = 4
  t1 = a_val/3
  t2 = 4*sp.sqrt(2)
  t3 = 6*a_val
  r1 = t2/t1
  r2 = t3/t2
  if sp.simplify(r1 - r2) == 0:
    print('VERIFY_PASS')
  else:
    print('VERIFY_FAIL')
else:
  print('VERIFY_FAIL')