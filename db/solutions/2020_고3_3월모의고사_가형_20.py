from sympy import sqrt, simplify, solve, symbols, Rational

b = symbols('b', real=True)
claimed = 2 - sqrt(2)

# 핵심 조건: t=(b^2-4b+2)/(b-1), t->0+ 이면 b^2-4b+2=0
residual = simplify(claimed**2 - 4*claimed + 2)

# 수치 수렴 검증
errors = []
for t_val in [Rational(1,10), Rational(1,100), Rational(1,1000)]:
    sols = solve(b**2 - 4*b + 2 - t_val*(b - 1), b)
    valid = [s for s in sols if 0 < float(s) < 2]
    if valid:
        errors.append(abs(float(valid[0]) - float(claimed)))

converging = all(errors[i] > errors[i+1] for i in range(len(errors)-1))

if residual == 0 and converging:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
