# 조건 (가) 및 (나) 검증
f_vals = {-3: 12, -2: 8, -1: 4, 0: 5, 1: -4, 2: 1}
X = [-3, -2, -1, 0, 1, 2]

# 조건 (가): 각 x에 대해 {f(x)+x^2-5} × {f(x)+4x} = 0
for x in X:
    f_x = f_vals[x]
    eq1 = f_x + x**2 - 5
    eq2 = f_x + 4*x
    product = eq1 * eq2
    assert product == 0, f'조건 (가) 실패: x={x}, product={product}'

# 조건 (나): f(0) × f(1) × f(2) < 0
product_012 = f_vals[0] * f_vals[1] * f_vals[2]
assert product_012 < 0, f'조건 (나) 실패: f(0)×f(1)×f(2)={product_012}'

# 일대일함수 확인
values = [f_vals[x] for x in X]
assert len(values) == len(set(values)), '일대일함수 실패: 중복된 값 존재'

# 최종 답
answer = sum(f_vals.values())
assert answer == 26, f'합계 오류: {answer}'

print('VERIFY_PASS')