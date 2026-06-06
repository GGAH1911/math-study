import sympy as sp
from sympy import sqrt, cos, sin, pi, simplify

# 각도 정의
angle_DAB = 2*pi/3
angle_BCD = 3*pi/4

# 삼각형 ABD에서 코사인 법칙
AB, AD = 2, 1
BD_squared = AB**2 + AD**2 - 2*AB*AD*cos(angle_DAB)
BD = sqrt(BD_squared)

# (나) 계산
na = 2*AB*AD*cos(angle_DAB)

# (가) 계산 - 삼각형 ABD에서 사인법칙
gA = 1/(2*sin(angle_DAB))
R2 = gA * BD

# (다) 계산 - R1 × R2
sqrt2_half = sqrt(2)/2
R1 = sqrt2_half * BD
da = R1 * R2
da_simplified = simplify(da)

# p, q, r 값
p = sqrt(3)/3
q = na
r = da_simplified

# 최종 계산
product = p * q * r
product_squared = simplify(product**2)
final_answer = 9 * product_squared

print(f"BD^2 = {BD_squared}")
print(f"(나) = {q}")
print(f"(가) = {p}")
print(f"(다) = {r}")
print(f"p*q*r = {simplify(product)}")
print(f"(p*q*r)^2 = {product_squared}")
print(f"9*(p*q*r)^2 = {final_answer}")

if final_answer == 98:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")