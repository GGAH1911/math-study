import sympy as sp
x = sp.symbols('x')
# 그래프를 piecewise로 표현 (이미지의 원래 조건)
# 왼쪽 포물선: -2 <= x <= 0, x != -1, x != 0 ; 정점 (-1,-1), 양 끝 (-2,0),(0,0) 열린점
# f(-1) = 0 (별개 점)
# 0 <= x < 1 : y = x+1 (x=0 닫힘, x=1 열림)
# x >= 1 : y = x-2 (x=1 닫힘 -> -1)
f_para = (x+1)**2 - 1
f_line1 = x + 1   # 0<=x<1

# lim x->-1 (양쪽 모두 포물선)
L1 = sp.limit(f_para, x, -1)
# lim x->1- (왼쪽에서 접근, 직선 y=x+1)
L2 = sp.limit(f_line1, x, 1, '-')

total = L1 + L2
print('L1=', L1, 'L2=', L2, 'sum=', total)
if sp.simplify(total - 1) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
