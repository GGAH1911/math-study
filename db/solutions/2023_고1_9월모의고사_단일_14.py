from fractions import Fraction
a = Fraction(3)
s_perp = (Fraction(9,5), Fraction(18,5))
s_tang = (Fraction(18,5), Fraction(-9,5))
A = (a, Fraction(6))
B = (A[0]-s_perp[0], A[1]-s_perp[1])
C = (B[0]+s_tang[0], B[1]+s_tang[1])
D = (A[0]+s_tang[0], A[1]+s_tang[1])
assert a > 0
assert B[0]+2*B[1] == 6
assert C[0]+2*C[1] == 6
assert D[0] > 0 and D[1] > 0
AB=(B[0]-A[0],B[1]-A[1]); BC=(C[0]-B[0],C[1]-B[1]); CD=(D[0]-C[0],D[1]-C[1]); DA=(A[0]-D[0],A[1]-D[1])
AB2=AB[0]**2+AB[1]**2; BC2=BC[0]**2+BC[1]**2; CD2=CD[0]**2+CD[1]**2; DA2=DA[0]**2+DA[1]**2
assert AB2==BC2==CD2==DA2
assert AB[0]*BC[0]+AB[1]*BC[1]==0
assert AB2==Fraction(81,5)
print('VERIFY_PASS')