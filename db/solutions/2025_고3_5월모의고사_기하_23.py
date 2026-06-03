import math

# 정사각형 좌표
A = (0, 3)
B = (0, 0)
C = (3, 0)
D = (3, 3)

# 벡터 AC
AC = (C[0] - A[0], C[1] - A[1])

# 벡터 CD
CD = (D[0] - C[0], D[1] - C[1])

# 스칼라배
CD_third = (CD[0]/3, CD[1]/3)

# 벡터 합
result = (AC[0] + CD_third[0], AC[1] + CD_third[1])

# 크기
magnitude = math.sqrt(result[0]**2 + result[1]**2)
expected = math.sqrt(13)

if abs(magnitude - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')