from sympy import symbols, Rational, sqrt, solve, simplify, Eq

# 원래 문제의 조건을 그대로 표현
# 표본 1: 크기 100, 95% 신뢰구간 [a, b] = [x1 - 1.96*sigma/sqrt(100), x1 + 1.96*sigma/sqrt(100)]
# 표본 2: 크기 n, 99% 신뢰구간 [c, d] = [x2 - 2.58*sigma/sqrt(n), x2 + 2.58*sigma/sqrt(n)]
# 조건: x1 - x2 = 1.34, a = c
# 추가: n은 양의 정수, sigma는 양의 실수

z95 = Rational(196, 100)  # 1.96
z99 = Rational(258, 100)  # 2.58
diff = Rational(134, 100)  # 1.34

# 후보 답안: b - a = 7.84 => sigma = 7.84 / (2 * 1.96 / 10) = 7.84 / 0.392 = 20
sigma_candidate = Rational(20)
b_minus_a_candidate = Rational(784, 100)  # 7.84

# b - a 계산식으로 sigma 일관성 체크
b_minus_a_formula = 2 * z95 * sigma_candidate / sqrt(100)
assert simplify(b_minus_a_formula - b_minus_a_candidate) == 0, 'b-a inconsistent'

# a = c 와 x1 - x2 = 1.34 로부터 n 결정
# 1.34 = sigma * (1.96/sqrt(100) - 2.58/sqrt(n))
n = symbols('n', positive=True)
lhs = sigma_candidate * (z95 / sqrt(100) - z99 / sqrt(n))
sol = solve(Eq(lhs, diff), n)

# 정수 양의 해가 있어야 함
valid = [s for s in sol if s.is_real and s > 0]
n_val = None
for s in valid:
    if s == int(s):
        n_val = int(s)
        break

if n_val is None:
    print('VERIFY_FAIL')
else:
    # 원식에 sigma=20, n=400 대입해 1.34 재확인
    check = sigma_candidate * (z95 / sqrt(100) - z99 / sqrt(Rational(n_val)))
    if simplify(check - diff) == 0 and n_val == 400 and simplify(b_minus_a_formula - Rational(784, 100)) == 0:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
