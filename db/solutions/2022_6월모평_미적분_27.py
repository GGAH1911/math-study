import math
import numpy as np

k = math.sqrt(2) * math.exp(9 * math.pi / 4)

def F(x):
    return math.exp(x) - k * math.sin(x)

def Fp(x):
    return math.exp(x) - k * math.cos(x)

# Scan (0, 6pi) for sign changes (transversal roots)
N = 1_000_000
xs = np.linspace(1e-10, 6 * math.pi, N)
ys = np.exp(xs) - k * np.sin(xs)
signs = np.sign(ys)

sign_changes = 0
prev = signs[0]
for s in signs[1:]:
    if s != 0 and prev != 0 and s != prev:
        sign_changes += 1
    if s != 0:
        prev = s

# Tangent point candidate: 2pi + pi/4
tan_x = 2*math.pi + math.pi/4
F_tan = F(tan_x)
Fp_tan = Fp(tan_x)
is_tangent = abs(F_tan) < 1e-6 and abs(Fp_tan) < 1e-6

total = sign_changes + (1 if is_tangent else 0)

print('k =', k)
print('sign_changes (transversal roots) in (0,6pi):', sign_changes)
print('tangent at 2pi+pi/4: F=%.3e, Fp=%.3e, is_tangent=%s' % (F_tan, Fp_tan, is_tangent))
print('total distinct positive roots:', total)

if total == 3 and is_tangent:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
