from fractions import Fraction
A = Fraction(-5)
B = Fraction(1)
m, n = 3, 1
P = Fraction(4)
# 외분점 정의: P = (m*B - n*A)/(m-n)
expected = (m*B - n*A) / (m - n)
# 또한 AP:PB = m:n (외분이므로 P는 선분 바깥)
AP = abs(P - A)
PB = abs(P - B)
ratio_ok = AP * n == PB * m
# P가 선분 AB 바깥에 있는지 (외분 조건): P > max(A,B) 또는 P < min(A,B)
is_external = (P > max(A, B)) or (P < min(A, B))
if P == expected and ratio_ok and is_external:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')