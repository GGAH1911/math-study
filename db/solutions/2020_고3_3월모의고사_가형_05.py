from sympy import symbols, solve, simplify

n = symbols('n', positive=True, integer=True)

# S_n = (-1)^n + n - 1
def S(k):
    return ((-1)**k) + k - 1

# S_n > 100을 만족하는 최소 n 찾기
for test_n in range(1, 110):
    if S(test_n) > 100:
        print(f'First n where S_n > 100: {test_n}')
        print(f'S_{test_n} = {S(test_n)}')
        if S(test_n - 1) <= 100:
            print('VERIFY_PASS')
        else:
            print('VERIFY_FAIL')
        break