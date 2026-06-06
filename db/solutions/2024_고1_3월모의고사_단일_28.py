import math
from sympy import sqrt, Rational

A = (5, 4)
B = (0, 0)
C = (4, 0)
G = (3, Rational(4, 3))
D = (2, 0)

AB = math.sqrt((A[0] - B[0])**2 + (A[1] - B[1])**2)
assert abs(AB - math.sqrt(41)) < 1e-9, f'AB check failed: {AB}'

BC = 4
assert BC == 4, 'BC check failed'

CA = (A[0] - C[0], A[1] - C[1])
CB = (B[0] - C[0], B[1] - C[1])
dot_prod = CA[0] * CB[0] + CA[1] * CB[1]
assert dot_prod < 0, 'angle C > 90 check failed'

ADC_area = 0.5 * abs((D[0] - A[0]) * (C[1] - A[1]) - (C[0] - A[0]) * (D[1] - A[1]))
assert abs(ADC_area - 4) < 1e-9, f'ADC area check failed: {ADC_area}'

DG_dist = math.sqrt((float(G[0]) - D[0])**2 + (float(G[1]) - D[1])**2)
expected_DG = 5.0 / 3.0
assert abs(DG_dist - expected_DG) < 1e-9, f'DG check failed: {DG_dist}'

DC = (C[0] - D[0], C[1] - D[1])
DA = (A[0] - D[0], A[1] - D[1])
cos_CDA = (DC[0] * DA[0] + DC[1] * DA[1]) / (math.sqrt(DC[0]**2 + DC[1]**2) * math.sqrt(DA[0]**2 + DA[1]**2))
tan_CDA = math.sqrt(1 - cos_CDA**2) / cos_CDA
expected_tan = 4.0 / 3.0
assert abs(tan_CDA - expected_tan) < 1e-9, f'tan(CDA) check failed: {tan_CDA}'

result = DG_dist * tan_CDA
expected_result = 20.0 / 9.0
assert abs(result - expected_result) < 1e-9, f'DG*tan(CDA) check failed: {result}'

p, q = 9, 20
assert p + q == 29, 'Final answer check failed'
print('VERIFY_PASS')