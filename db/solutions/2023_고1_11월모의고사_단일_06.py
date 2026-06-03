# 주어진 조건: f(x) = 2x + 1, (g∘g)(x) = 3x - 1
# ((f∘g)∘g)(a) = a 확인

def f(x):
    return 2*x + 1

def g_compose_g(x):
    """(g∘g)(x) = 3x - 1"""
    return 3*x - 1

# 우리가 구한 답
a = 1/5

# ((f∘g)∘g)(a) = f((g∘g)(a)) 계산
result = f(g_compose_g(a))

# 검증
if abs(result - a) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')