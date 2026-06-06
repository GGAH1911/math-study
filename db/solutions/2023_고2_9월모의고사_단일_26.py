from sympy import symbols, diff

CANDIDATE = '20'

# 검증된 풀이의 관계식들로부터 f, g 구성
# 조건: p - a = 1, g(3) = 0, g'(3) = 8, g(x) - f(x) = x^2 + 2x - 15

# 구체적 f, g 설정 (정규화: a=1)
a, b, c = 1, -6, 9
p, q, r = 2, -4, -6

x = symbols('x')
f = a * x**2 + b * x + c
g = p * x**2 + q * x + r

# 극한 조건 2: lim_{x→3} g(x)/(x-3) = 8 검증
# g(3) = 0 확인
g_at_3 = g.subs(x, 3)
assert g_at_3 == 0, f'g(3)={g_at_3}, expected 0'

# g'(3) = 8 확인
g_prime = diff(g, x)
g_prime_at_3 = g_prime.subs(x, 3)
assert g_prime_at_3 == 8, f'g\'(3)={g_prime_at_3}, expected 8'

# 극한 조건 1에서 도출된 관계식 검증
# H(x) = g(x) - f(x) = x^2 + 2x - 15
H = g - f
assert H.coeff(x, 2) == 1, f'H x^2 coeff={H.coeff(x, 2)}'
assert H.coeff(x, 1) == 2, f'H x coeff={H.coeff(x, 1)}'
assert H.coeff(x, 0) == -15, f'H const={H.coeff(x, 0)}'
assert p - a == 1, f'p-a={p-a}'
assert q - b == 2, f'q-b={q-b}'
assert r - c == -15, f'r-c={r-c}'

# 문제 조건에서 도출된 g(x) - f(x) 값을 x=5에서 계산
# g(5) - f(5) = 5^2 + 2(5) - 15 = 25 + 10 - 15 = 20
H_at_5 = H.subs(x, 5)
expected = int(CANDIDATE)

if H_at_5 == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')