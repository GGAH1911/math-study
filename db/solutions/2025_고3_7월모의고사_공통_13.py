import math

a_val = 3
b_val = 3

def f(x):
    return x*x - 4*x + 5

def g(x):
    return f(x + a_val) + b_val if x < 0 else f(x)

# 연속성 확인 (원 조건)
assert abs(f(0 + a_val) + b_val - f(0)) < 1e-9, 'not continuous at 0'

def h(t):
    """원래 g(x)=t를 만족하는 실수 x의 개수 (원 식 그대로 사용)."""
    count = 0
    # 좌측 분기: f(x+a)+b = t, x<0
    # (x+a-2)^2 = t - 1 - b
    r1 = t - 1 - b_val
    if r1 > 1e-12:
        s = math.sqrt(r1)
        for x in [(2 - a_val) + s, (2 - a_val) - s]:
            if x < -1e-12:
                count += 1
    elif abs(r1) < 1e-12:
        if (2 - a_val) < -1e-12:
            count += 1
    # 우측 분기: (x-2)^2 = t - 1, x>=0
    r2 = t - 1
    if r2 > 1e-12:
        s = math.sqrt(r2)
        for x in [2 + s, 2 - s]:
            if x > -1e-12:
                count += 1
    elif abs(r2) < 1e-12:
        count += 1
    return count

eps = 1e-7
# k=1,4,5에서 점프 크기 정확히 2
ok = True
for k in [1, 4, 5]:
    diff = abs(h(k + eps) - h(k - eps))
    if diff != 2:
        ok = False
        break

# 다른 t에서는 점프 없어야 함 (대표 샘플 확인)
for k in [-1, 0.5, 2, 3, 3.5, 4.5, 5.5, 6, 10]:
    diff = abs(h(k + eps) - h(k - eps))
    if diff != 0:
        ok = False
        break

# g(-4) 값 확인
result = g(-4)
if ok and result == 13:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
