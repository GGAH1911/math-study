from sympy import symbols, simplify, Rational

d = -4
# S_12 = 0 조건으로 a1 결정
a1 = symbols('a1')
S12 = 12*a1 + Rational(12*11,2)*d
sol = simplify(S12)
# S12 = 12*a1 - 264 = 0 -> a1 = 22
a1_val = 22
assert 12*a1_val + (12*11//2)*d == 0, 'a1 condition fails'

# a_n 정의
def a(n):
    return a1_val + (n-1)*d

def S(n):
    return sum(a(k) for k in range(1, n+1))

# 모든 n에 대해 최대값 탐색 (수열이 결국 음의 무한대로 가므로 충분히 큰 범위)
values = [S(n) for n in range(1, 100)]
max_S = max(values)

ans = 72
if S(12) == 0 and max_S == ans:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
