# 검증: 임의의 상수 c에 대해 g(3) + h(1) = 6인지 확인
c = 2  # 임의의 상수값 선택

# f는 항등함수
def f(x):
    return x

# g는 상수함수
def g(x):
    return c

# 조건 (나)에서 h(x) = 7 - f(x) - g(x)
def h(x):
    return 7 - f(x) - g(x)

# 조건 (나) 검증: 모든 x에 대해 f(x) + g(x) + h(x) = 7
for x in [1, 2, 3, 4, 5]:
    result = f(x) + g(x) + h(x)
    assert result == 7, f'x={x}에서 f(x)+g(x)+h(x)={result}'

# 답 계산
answer = g(3) + h(1)
assert answer == 6, f'g(3)+h(1)={answer}'

print('VERIFY_PASS')