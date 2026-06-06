import sympy as sp
from sympy import sqrt, symbols

a2, b2 = 9, 7
xP, yP = 9, 2*sqrt(14)

# 쌍곡선 방정식 검증
hyperbola_check = xP**2 / a2 - yP**2 / b2 - 1
print('쌍곡선 확인:', sp.simplify(hyperbola_check))

# 포물선 방정식 검증
parabola_check = yP**2 - (8*xP - 16)
print('포물선 확인:', sp.simplify(parabola_check))

# 비율 조건 검증
PH = xP
HF = sqrt(16 + yP**2)
ratio_left = PH / HF
ratio_right = 3 / (2*sqrt(2))
ratio_check = sp.simplify(ratio_left - ratio_right)
print('비율 확인:', sp.simplify(ratio_check))

# 초점 조건 검증
focus_check = a2 + b2 - 16
print('초점 조건 확인:', focus_check)

if hyperbola_check == 0 and parabola_check == 0 and ratio_check == 0 and focus_check == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')