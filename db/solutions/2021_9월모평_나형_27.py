CANDIDATE = 121

import numpy as np
from sympy import symbols, solve, simplify

# E(X) = 2, E(X²) = 5 조건으로부터 a, b, c, d 결정
# a + b + c + d = 1
# a + 2b + 3c + 4d = 2
# a + 4b + 9c + 16d = 5

# Y = 10X + 1 이므로:
# E(Y) = 10*E(X) + 1 = 10*2 + 1 = 21
# V(X) = E(X²) - [E(X)]² = 5 - 4 = 1
# V(Y) = 100*V(X) = 100*1 = 100
# E(Y) + V(Y) = 21 + 100 = 121

EX = 2
EX2 = 5
VX = EX2 - EX**2
assert VX == 1, f'V(X) = {VX}, expected 1'

EY = 10 * EX + 1
assert EY == 21, f'E(Y) = {EY}, expected 21'

VY = 100 * VX
assert VY == 100, f'V(Y) = {VY}, expected 100'

result = EY + VY
assert result == CANDIDATE, f'E(Y) + V(Y) = {result}, expected {CANDIDATE}'

print('VERIFY_PASS')