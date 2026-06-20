from sympy import symbols, Rational, solve, Eq

# P(A)를 구하는 문제
# 조건: A, B 독립, P(A|B) = P(B), P(A∩B) = 1/9

pa, pb = symbols('pa pb', positive=True, real=True)

# 조건 1: A, B 독립 → P(A∩B) = P(A)·P(B)
# 조건 2: P(A|B) = P(B) → P(A∩B)/P(B) = P(B) → P(A∩B) = [P(B)]²
# 조건 3: P(A∩B) = 1/9

# 독립 조건과 조건2 결합
eq1 = Eq(pa * pb, pb**2)  # P(A)·P(B) = [P(B)]²
eq2 = Eq(pa * pb, Rational(1, 9))  # P(A∩B) = 1/9

# eq1에서 P(A) = P(B)
pa_value = pb  # pa = pb

# eq2에 대입
eq3 = Eq(pa_value * pb, Rational(1, 9))
eq3_substituted = eq3.subs(pa, pb)
# pb² = 1/9

sol = solve(pb**2 - Rational(1, 9), pb)
print(f"P(B) solutions: {sol}")

pb_val = Rational(1, 3)  # positive solution
pa_val = pb_val

print(f"P(A) = {pa_val}")
print(f"P(B) = {pb_val}")

# 검증
pa_times_pb = pa_val * pb_val
print(f"P(A)·P(B) = {pa_times_pb}")

cond_prob = pa_times_pb / pb_val
print(f"P(A|B) = P(A∩B)/P(B) = {cond_prob}")

if cond_prob == pb_val and pa_times_pb == Rational(1, 9):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')