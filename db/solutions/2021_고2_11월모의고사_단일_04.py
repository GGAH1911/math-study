import sympy as sp

x = sp.Symbol('x')

# 그래프에서 x<=0 및 x>1 구간: 포물선 f(x) = -x^2 + 2
# 0 < x < 1 구간: 선분 f(x) = -x
# f(1) = 0

parabola = -x**2 + 2
line = -x

# lim_{x->0-}: 포물선 조각의 좌극한
left_limit_0 = sp.limit(parabola, x, 0, '-')

# lim_{x->1+}: 포물선 조각의 우극한
right_limit_1 = sp.limit(parabola, x, 1, '+')

# 좌극한 x->1- (선분): 검증용
left_limit_1 = sp.limit(line, x, 1, '-')

# 우극한 x->0+ (선분): 검증용
right_limit_0 = sp.limit(line, x, 0, '+')

product = left_limit_0 * right_limit_1

# 그래프 일관성 검사
consistency = (
    left_limit_0 == 2 and      # (0,2) 채워진 원
    right_limit_0 == 0 and     # (0,0) 빈 원
    left_limit_1 == -1 and     # (1,-1) 빈 원
    right_limit_1 == 1         # (1,1) 빈 원
)

if product == 2 and consistency:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'product={product}, consistency={consistency}')
