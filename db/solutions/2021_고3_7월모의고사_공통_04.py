# 구간별 함수 정의 및 극한값 검증
def f_left_of_neg1(x):
    return 2*x + 4

def f_right_of_1(x):
    return 2*x - 3

# 좌극한: x → -1의 좌측에서 f(x) = 2x + 4
lim_left = f_left_of_neg1(-1.0)
print(f'lim_(x→-1⁻) f(x) = {lim_left}')

# 우극한: x → 1의 우측에서 f(x) = 2x - 3
lim_right = f_right_of_1(1.0)
print(f'lim_(x→1⁺) f(x) = {lim_right}')

# 합
result = lim_left + lim_right
print(f'합 = {result}')

if result == 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')