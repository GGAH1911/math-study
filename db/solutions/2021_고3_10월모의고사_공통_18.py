import sympy as sp
from sympy import symbols, simplify

n = symbols('n', integer=True, positive=True)

# 각 점의 좌표
# A(1, n), B(1, 2), C(2, n^2), D(2, 4)
# 사다리꼴 ABDC의 넓이
area = (n**2 + n - 6) / 2

# 조건: 넓이 ≤ 18
for test_n in [3, 4, 5, 6, 7]:
    area_val = float(area.subs(n, test_n))
    if area_val <= 18:
        result = f'n={test_n}: area={area_val} ≤ 18'
    else:
        result = f'n={test_n}: area={area_val} > 18'
    print(result)

# 조건을 만족하는 n의 합
valid_n = [n_val for n_val in range(3, 10) if float(area.subs(n, n_val)) <= 18]
sum_n = sum(valid_n)
print(f'\nValid n values: {valid_n}')
print(f'Sum: {sum_n}')

if sum_n == 18:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')