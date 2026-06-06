import sympy as sp

# 원래 문제식 계산
part1 = sp.sqrt(sp.Rational(2, 3)) * sp.sqrt(sp.Rational(15, 2))
part2 = sp.sqrt(20)
result = part1 + part2

# 단순화
result_simplified = sp.simplify(result)

# 답: 3*sqrt(5)
answer = 3 * sp.sqrt(5)

if sp.simplify(result_simplified - answer) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')