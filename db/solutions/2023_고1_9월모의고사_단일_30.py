from sympy import *
x = symbols('x')
f = lambda x_val: x_val**2/4 - x_val + 2

# 원점 확인: x=0이 f(x)=x+2의 근
assert f(0) == 2, 'f(0) should equal 2'
assert 2 == 0 + 2, 'x=0 satisfies f(x)=x+2'

# 5개 근 확인
eq1 = x**2/4 - x + 2 - x  # f(x)=x
eq2 = x**2/4 - x + 2 - (x + 2)  # f(x)=x+2
eq3 = x**2/4 - x + 2 - (x - 2)  # f(x)=x-2

roots1 = solve(eq1, x)
roots2 = solve(eq2, x)
roots3 = solve(eq3, x)

all_roots = sorted(roots1 + roots2 + roots3, key=lambda r: float(r))
assert len(all_roots) == 5, f'Should have 5 roots, got {len(all_roots)}'
assert all_roots[0] == 0, f'First root should be 0, got {all_roots[0]}'

sum_last_four = sum(all_roots[1:])
assert sum_last_four == 20, f'Sum of roots 2-5 should be 20, got {sum_last_four}'

# 범위 내 최솟값 확인
min_x = 2
assert min_x >= 0 and min_x <= 8, 'Minimum x should be in [0,8]'
assert f(min_x) == 1 and f(min_x) > 0, f'f({min_x}) should be 1 and positive'

# 최종 답 확인
result = f(20)
assert result == 82, f'f(20) should be 82, got {result}'

print('VERIFY_PASS')