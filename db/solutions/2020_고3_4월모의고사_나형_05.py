from sympy import symbols, Sum, summation
Sa = 10  # given sum of a_k
Sb = 3   # given sum of b_k
# linearity: sum(2a_k - b_k) = 2*sum(a_k) - sum(b_k)
result = 2*Sa - Sb
# cross-check with a concrete sequence satisfying the constraints
import sympy
# choose a_k constant = 1 (sum=10), b_k constant = 3/10 (sum=3)
k = symbols('k')
Sa_check = summation(sympy.Rational(1,1), (k,1,10))
Sb_check = summation(sympy.Rational(3,10), (k,1,10))
val_check = summation(2*sympy.Rational(1,1) - sympy.Rational(3,10), (k,1,10))
assert Sa_check == 10 and Sb_check == 3
print('VERIFY_PASS' if result == 17 and val_check == 17 else 'VERIFY_FAIL')