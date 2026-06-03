from sympy import *
E = Matrix([0, 0])
A = Matrix([0, 4])
C = Matrix([10, 0])
B = Matrix([-6, -8])
D = (2*A + B) / 3
AE = sqrt((A-E).dot(A-E))
BE = sqrt((B-E).dot(B-E))
CE_len = sqrt((C-E).dot(C-E))
AD_len = sqrt((A-D).dot(A-D))
BD_len = sqrt((B-D).dot(B-D))
dot_perp = (A-E).dot(D-C)
cross_check = (E-C)[0]*(D-C)[1] - (E-C)[1]*(D-C)[0]
AB_vec = B-A; AC_vec = C-A
cos_CAB = AB_vec.dot(AC_vec)/(sqrt(AB_vec.dot(AB_vec))*sqrt(AC_vec.dot(AC_vec)))
area = Rational(1,2)*Abs((B[0]-A[0])*(C[1]-A[1])-(C[0]-A[0])*(B[1]-A[1]))
all_pass = (AE==4 and BE==10 and CE_len==10 and simplify(BD_len-2*AD_len)==0 and dot_perp==0 and cross_check==0 and cos_CAB<0 and area==72)
print('VERIFY_PASS' if all_pass else 'VERIFY_FAIL')