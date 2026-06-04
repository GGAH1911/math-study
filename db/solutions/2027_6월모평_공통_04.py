import sympy as sp

x = sp.symbols('x')

# 그래프 조각을 식으로 표현
# 왼쪽 직선: (-2, 0)과 (-1, -1)을 지남 -> 기울기 -1, y = -x - 2 (x < -1)
left_line = -x - 2
# 가운데 곡선: (-1, 2)에서 (1, 0)까지 부드럽게 (-1 < x < 1)
# 형태에 상관없이 극한만 검사하므로 한 예: 1 - x - (x^3 빠진 형태)... 
# 더 안전: 좌극한/우극한은 각 조각의 끝점값 (○ 표시)
# 오른쪽 직선: (1, 1)과 (2, 0)을 지남 -> 기울기 -1, y = -x + 2 (x > 1)
right_line = -x + 2

# lim_{x -> -1-} f(x) = 왼쪽 직선의 x=-1에서 값
lim_left = sp.limit(left_line, x, -1, '-')
# lim_{x -> 1+} f(x) = 오른쪽 직선의 x=1에서 값
lim_right = sp.limit(right_line, x, 1, '+')

total = lim_left + lim_right
print('lim_left =', lim_left)
print('lim_right =', lim_right)
print('sum =', total)

if total == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
