def f(val):
    if val >= 1:
        return -2*val + 3
    else:
        return (3 - val) / 2

# 조건2 검증: f(x^2+1) == -2x^2+1
for xv in [-3,-2,-1,0,1,2,3]:
    lhs = f(xv**2 + 1)
    rhs = -2*xv**2 + 1
    assert abs(lhs - rhs) < 1e-10, f'Cond2 fail x={xv}'

# 대합(involution) 검증: f(f(x)) == x
for v in [-5, -2, 0, 0.5, 1.0, 2.5, 3.0]:
    assert abs(f(f(v)) - v) < 1e-10, f'Involution fail v={v}'

# f(-2) == 5/2 검증
result = f(-2)
assert abs(result - 2.5) < 1e-10, f'f(-2)={result} != 5/2'
print('VERIFY_PASS')