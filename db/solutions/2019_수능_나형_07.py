import sympy as sp

x = sp.symbols('x')

# 그림을 충실히 반영한 piecewise 모델
# x < -1: 왼쪽 위에서 내려와 (-1,2) 빈 점으로 접근
left_branch = -3*x - 1            # x->-1- 일 때 -> 2
# -1 <= x < 1: y = -1 수평선분 (그래프상 채움/빈 점)
mid_branch = sp.Integer(-1)
# x >= 1: (1,1)에서 시작해 약간 위로 솟았다 내려가는 하향 곡선
right_branch = 1 + (x - 1) - 2*(x - 1)**2   # x->1+ 일 때 -> 1

# 좌극한(x->-1-)은 왼쪽 가지, 우극한(x->1+)은 오른쪽 가지 사용
L1 = sp.limit(left_branch, x, -1, dir='-')
L2 = sp.limit(right_branch, x, 1, dir='+')

result = sp.simplify(L1 - L2)

ok = (sp.simplify(L1 - 2) == 0) and (sp.simplify(L2 - 1) == 0) and (sp.simplify(result - 1) == 0)
print('VERIFY_PASS' if ok else 'VERIFY_FAIL')
