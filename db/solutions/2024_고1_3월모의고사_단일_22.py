from sympy import symbols, expand
x = symbols('x')
# 원래 함수
f = x**2 - 2*x + 6
# 꼭짓점 형태로 변형
g = (x - 1)**2 + 5
# 두 형태가 동일한지 확인
assert expand(f - g) == 0
# x=1일 때 y값
y_at_vertex = f.subs(x, 1)
assert y_at_vertex == 5
# 답 검증: a=1, b=5, a+b=6
a, b = 1, 5
assert a + b == 6
print('VERIFY_PASS')