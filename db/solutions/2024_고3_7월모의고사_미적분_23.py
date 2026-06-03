import math

# 원래 함수: (5^(2x) - 1) / (e^(3x) - 1)
# x -> 0 수치 극한으로 확인
def f(x):
    return (5**(2*x) - 1) / (math.exp(3*x) - 1)

# 작은 x 값들로 수치 극한 계산
results = [f(x) for x in [1e-7, 1e-8, 1e-9, 1e-10]]
numerical_limit = results[-1]
expected = 2 * math.log(5) / 3

if abs(numerical_limit - expected) < 1e-6:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: numerical={numerical_limit}, expected={expected}')
