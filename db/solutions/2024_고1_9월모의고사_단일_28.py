import math

# 주어진 조건에 따른 함수
c = 0.5
a = 6

def f(x):
    return c * (x - 2) * (x - a)

# 주요 점들
A = (2, 0)
B = (a, 0)
C = (0, 2*a*c)
P = ((2+a)/2, -c*(a-2)**2/4)

# Q: A에서 BC에 내린 수선의 발
# 직선 BC: x + y = 6 (a=6, c=0.5일 때)
Q = (4, 2)
R = (6, 0)

# 정사각형 검증
dist_AQ = math.sqrt((Q[0]-A[0])**2 + (Q[1]-A[1])**2)
dist_QR = math.sqrt((R[0]-Q[0])**2 + (R[1]-Q[1])**2)
dist_RP = math.sqrt((P[0]-R[0])**2 + (P[1]-R[1])**2)
dist_PA = math.sqrt((A[0]-P[0])**2 + (A[1]-P[1])**2)

# 모든 변의 길이가 같은지 확인
if abs(dist_AQ - dist_QR) < 1e-10 and abs(dist_QR - dist_RP) < 1e-10 and abs(dist_RP - dist_PA) < 1e-10:
    # 모든 각이 90도인지 확인
    vec_AP = (P[0]-A[0], P[1]-A[1])
    vec_AQ = (Q[0]-A[0], Q[1]-A[1])
    dot_product = vec_AP[0]*vec_AQ[0] + vec_AP[1]*vec_AQ[1]
    if abs(dot_product) < 1e-10:
        result = f(12)
        if abs(result - 30) < 1e-10:
            print('VERIFY_PASS')
        else:
            print('VERIFY_FAIL')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')