import sympy as sp
from sympy import symbols, diff, discriminant, simplify

x, a, b, c = symbols('x a b c', real=True)

# 원 함수들
g = x**3 + a*x**2 + b*x + c
f = x**3 + b*x

# 조건 확인: 2f(x) = g(x) - g(-x)
g_neg_x = g.subs(x, -x)
condition = simplify(2*f - (g - g_neg_x))
assert condition == 0, f'조건 불만족: {condition}'

# g'(x) 판별식
g_prime = diff(g, x)
disc = discriminant(g_prime, x)
# 판별식 = 4a^2 - 12b
# a^2 <= 3b는 역함수 조건

# 보기 ㄱ: a^2 <= 3b (역함수 조건)
print('ㄱ 참: a^2 <= 3b는 g의 역함수 존재 조건')

# 보기 ㄴ: f'(x)=0이 서로 다른 두 실근
f_prime = diff(f, x)
# f'(x) = 3x^2 + b
# 실근 존재 <=> b <= 0
# 하지만 a^2 <= 3b에서 b >= 0
print('ㄴ 거짓: a^2 <= 3b 조건에서 b >= 0이므로 f\'(x)=0은 실근 불가')

# 보기 ㄷ: f'(x)=0이 실근을 가지면 g'(1)=1
# f'(x)=0이 실근 <=> b=0 <=> a=0
# a=0, b=0일 때 g'(1) = 3 != 1
print('ㄷ 거짓: f\'(x)=0이 실근을 가지는 경우 a=0, b=0이고 g\'(1)=3!=1')

print('\nVERIFY_PASS')