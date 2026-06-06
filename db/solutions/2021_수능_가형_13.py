import math

# 검증: a = 1/2일 때 직사각형인지
a = 0.5

# 점 좌표
A = (a, 1)
B = (4*a, 1)
C = (1/a, -1)
D = (1/(4*a), -1)

print(f"A={A}, B={B}, C={C}, D={D}")

# 벡터
vec_AB = (B[0]-A[0], B[1]-A[1])
vec_BC = (C[0]-B[0], C[1]-B[1])
vec_CD = (D[0]-C[0], D[1]-C[1])
vec_DA = (A[0]-D[0], A[1]-D[1])

# 길이 확인
len_AB = math.sqrt(vec_AB[0]**2 + vec_AB[1]**2)
len_BC = math.sqrt(vec_BC[0]**2 + vec_BC[1]**2)
len_CD = math.sqrt(vec_CD[0]**2 + vec_CD[1]**2)
len_DA = math.sqrt(vec_DA[0]**2 + vec_DA[1]**2)

print(f"AB={len_AB}, BC={len_BC}, CD={len_CD}, DA={len_DA}")
print(f"AB==CD: {abs(len_AB-len_CD)<1e-10}, BC==DA: {abs(len_BC-len_DA)<1e-10}")

# 수직 확인
dot_AB_BC = vec_AB[0]*vec_BC[0] + vec_AB[1]*vec_BC[1]
dot_BC_CD = vec_BC[0]*vec_CD[0] + vec_BC[1]*vec_CD[1]
print(f"AB·BC={dot_AB_BC}, BC·CD={dot_BC_CD}")

if abs(len_AB-len_CD)<1e-10 and abs(len_BC-len_DA)<1e-10 and abs(dot_AB_BC)<1e-10:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")