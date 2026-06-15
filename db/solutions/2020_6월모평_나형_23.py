from sympy import Rational

# 2020 6월모평 나형 23: y=2/x 를 y축 방향 +4 평행이동한 그래프가 (2,a)를 지난다. a?
CANDIDATE = 5
def shifted(x):                   # 평행이동: y = 2/x + 4
    return Rational(2, x) + 4
a = shifted(2)                    # 점 (2, a) 통과 → a = shifted(2)
print('VERIFY_PASS' if a == CANDIDATE else 'VERIFY_FAIL')
