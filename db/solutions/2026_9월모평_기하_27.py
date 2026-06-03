from sympy import sqrt, Rational, simplify, symbols

# 쌍곡선: y^2/16 - x^2/9 = 1
# 초점: F(0,5), F'(0,-5), c=5

x0 = -3*sqrt(3)
y0 = 8

# 1) P가 쌍곡선 위에 있는지 확인
hyp = Rational(1,16)*y0**2 - Rational(1,9)*x0**2
assert simplify(hyp - 1) == 0, 'P not on hyperbola'

# 2) 초점 거리 확인
PF  = sqrt(x0**2 + (y0 - 5)**2)
PFp = sqrt(x0**2 + (y0 + 5)**2)
assert simplify(PF - 6)  == 0, f'|PF| wrong: {simplify(PF)}'
assert simplify(PFp - 14) == 0, f"|PF'| wrong: {simplify(PFp)}"

# 3) 둘레 확인
perimeter = simplify(PF + PFp + 10)
assert simplify(perimeter - 30) == 0, f'Perimeter wrong: {perimeter}'

# 4) 접선 기울기 = 16x/(9y)
slope = Rational(16,1)*x0 / (Rational(9,1)*y0)
slope_s = simplify(slope)

# 5) 정답 보기 ② -2*sqrt(3)/3
answer = -2*sqrt(3)/3
if simplify(slope_s - answer) == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: slope={slope_s}, answer={answer}')
