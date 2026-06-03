import sympy as sp

# a^2+b^2=4, ab=3/2 => (a-b)^2=4-3=1 => a-b=1
# a+b=sqrt(7) (positive root), a-b=1
s = sp.sqrt(7)
d = sp.Integer(1)
a_val = (s + d) / 2
b_val = (s - d) / 2

# 1. 두 점이 원 위에 있는지 확인
assert sp.simplify(a_val**2 + b_val**2 - 4) == 0, 'circle check failed'

# 2. a != b
assert sp.simplify(a_val - b_val) != 0, 'a==b'

# P, Q: y=x와 원의 교점
P = (sp.sqrt(2), sp.sqrt(2))
Q = (-sp.sqrt(2), -sp.sqrt(2))
A = (a_val, b_val)
B = (b_val, a_val)

# AP = BP 확인
AP2 = (P[0]-A[0])**2 + (P[1]-A[1])**2
BP2 = (P[0]-B[0])**2 + (P[1]-B[1])**2
assert sp.simplify(AP2 - BP2) == 0, 'AP!=BP'

# AQ = BQ 확인
AQ2 = (Q[0]-A[0])**2 + (Q[1]-A[1])**2
BQ2 = (Q[0]-B[0])**2 + (Q[1]-B[1])**2
assert sp.simplify(AQ2 - BQ2) == 0, 'AQ!=BQ'

# 신발끈 공식으로 사각형 APBQ 넓이 계산
pts = [A, P, B, Q]
n = len(pts)
area_sum = sp.Integer(0)
for i in range(n):
    j = (i+1) % n
    area_sum += pts[i][0]*pts[j][1] - pts[j][0]*pts[i][1]
area = sp.Abs(area_sum) / 2
area_simplified = sp.simplify(area)

# 넓이가 2*sqrt(2)인지 확인
if sp.simplify(area_simplified - 2*sp.sqrt(2)) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL, area =', area_simplified)
