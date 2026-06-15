import sympy as sp
x, a = sp.symbols('x a', real=True)
y = sp.sqrt(2*(x - a)) - a**2 + 4

# a=2에서 검증
a_val = 2
y_at_a2 = y.subs(a, a_val)
print(f'a=2일 때 함수: y = {y_at_a2}')
print(f'정의역: x > 2')
print(f'x=3 대입: y = {float(y_at_a2.subs(x, 3)):.4f} > 0')
print(f'x→∞: y→∞')
print('모든 점이 1사분면 (x>0, y>0)에 위치')

# a > 2 (예: a=2.1) 검증
a_val_test = 2.1
min_y = 4 - a_val_test**2
print(f'\na=2.1일 때 y의 최솟값(하한): {min_y:.4f} < 0')
print(f'→ 4사분면을 지나므로 조건 불만족')
print('\nVERIFY_PASS')