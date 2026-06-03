import numpy as np
A, B, C = np.array([2,3]), np.array([7,1]), np.array([4,5])
t1, t2 = 0.5, -0.5
D1 = A + t1*(B-A)
D2 = A + t2*(B-A)
E1 = A + t1*(C-A)
E2 = A + t2*(C-A)
area_ABC = 0.5*abs((B[0]-A[0])*(C[1]-A[1]) - (C[0]-A[0])*(B[1]-A[1]))
area_ADE1 = 0.5*abs((D1[0]-A[0])*(E1[1]-A[1]) - (E1[0]-A[0])*(D1[1]-A[1]))
area_ADE2 = 0.5*abs((D2[0]-A[0])*(E2[1]-A[1]) - (E2[0]-A[0])*(D2[1]-A[1]))
if abs(area_ABC/area_ADE1 - 4) < 0.001 and abs(area_ABC/area_ADE2 - 4) < 0.001:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')