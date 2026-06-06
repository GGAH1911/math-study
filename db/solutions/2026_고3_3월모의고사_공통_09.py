CANDIDATE = 15

from sympy import symbols, diff, solve

x = symbols('x')
a = symbols('a')

# 문제 함수: f(x) = 2x³ - 3x² - 12x + a
# (풀이에서 f'(x) = 6x² - 6x - 12로부터 역산)
f = 2*x**3 - 3*x**2 - 12*x + a
f_prime = diff(f, x)

# Step 1: 도함수 확인
expected_f_prime = 6*x**2 - 6*x - 12
if f_prime != expected_f_prime:
    print("VERIFY_FAIL")
    exit()

# Step 2: 최솟값 조건 f(2) = 4에서 a 구하기
f_at_2 = f.subs(x, 2)
# f(2) = 2*8 - 3*4 - 12*2 + a = 16 - 12 - 24 + a = a - 20
a_solutions = solve(f_at_2 - 4, a)
if not a_solutions or a_solutions[0] != 24:
    print("VERIFY_FAIL")
    exit()

a_value = 24

# Step 3: a = 24를 대입한 구체적 함수
f_concrete = f.subs(a, a_value)

# Step 4: 구간 [1, 3]에서 함수값 계산
f_at_1 = int(f_concrete.subs(x, 1))
f_at_2_check = int(f_concrete.subs(x, 2))
f_at_3 = int(f_concrete.subs(x, 3))

# Step 5: 각 함수값 검증
if f_at_1 != 11 or f_at_2_check != 4 or f_at_3 != 15:
    print("VERIFY_FAIL")
    exit()

# Step 6: 최솟값과 최댓값 확인
all_values = [f_at_1, f_at_2_check, f_at_3]
min_value = min(all_values)
max_value = max(all_values)

# Step 7: 문제 조건과 CANDIDATE 대조
# 조건: 최솟값 = 4, 최댓값 = CANDIDATE
if min_value == 4 and max_value == CANDIDATE:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")