CANDIDATE = '7'

from sympy import symbols, diff

x = symbols('x')
f = x**3 - 5*x + 8

f_prime = diff(f, x)
f_prime_at_2 = f_prime.subs(x, 2)

candidate_value = int(CANDIDATE)

if f_prime_at_2 == candidate_value:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")