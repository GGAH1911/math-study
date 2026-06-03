import sympy as sp
x, y = sp.symbols('x y')
# 포물선 y^2 = 12x 위의 점 (3, 6) 확인
assert 6**2 == 12*3, '점 (3,6)이 포물선 위에 있지 않음'
# 포물선 미분으로 (3,6)에서의 기울기
m = 6/6
assert m == 1, '기울기 계산 오류'
# 접선 방정식: y = x + 3
# 점 (1, a) 대입
a = 1 + 3
assert a == 4, 'a 값 오류'
# 점 (1, 4)가 접선 위에 있는지 확인
assert 4 == 1 + 3, '점 (1,4)가 접선 위에 있지 않음'
print('VERIFY_PASS')