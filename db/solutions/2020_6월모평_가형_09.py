import math
from sympy import *

# g(2) = log_2(5)
g_2 = log(5) / log(2)
print(f'g(2) = {g_2} = {float(g_2):.6f}')

# g'(2) = 2
g_prime_2 = 2

# f'(x) = 2^x이므로 f'(g(2)) = 2^(log_2(5)) = 5
f_prime_g2 = 2**g_2
print(f'f\'(g(2)) = 2^(log_2(5)) = {simplify(f_prime_g2)}')

# (f∘g)'(2) = f'(g(2)) * g'(2)
composition_derivative = f_prime_g2 * g_prime_2
print(f'(f∘g)\'(2) = {simplify(composition_derivative)}')

# 조건 확인
if simplify(composition_derivative) == 10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')