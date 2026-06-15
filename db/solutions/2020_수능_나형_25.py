# 2020 수능 나형 25: 2x^2-3x+1 을 (x-n)으로 나눈 나머지 a_n. sum_{n=1}^{7}(a_n - n^2 + n)?
# 나머지정리: a_n = p(n), p(x)=2x^2-3x+1.
CANDIDATE = 91
def p(x):
    return 2 * x**2 - 3 * x + 1
total = sum(p(n) - n**2 + n for n in range(1, 8))
print('VERIFY_PASS' if total == CANDIDATE else 'VERIFY_FAIL')
