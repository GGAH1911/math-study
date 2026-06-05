import sympy as sp
x = sp.Symbol('x')

# 원래 주어진 조건식 검증
A = x**3 + 4*x**2 + 5*x - 10
B = x**2 + x - 2
Q = x**2 + 5*x + 10

# 조건 (가): A(x)B(x)는 (x-1)^2으로 나누어떨어진다
AB = A * B
quotient_a, remainder_a = sp.div(AB, (x-1)**2)
assert remainder_a == 0, f"조건 (가) 실패: 나머지={remainder_a}"

# 조건 (나): (B(x))^2를 x^2-3x+2로 나눈 몫이 Q(x), 나머지가 16x-16
B_squared = B**2
quotient_b, remainder_b = sp.div(B_squared, x**2 - 3*x + 2)
assert quotient_b == Q, f"조건 (나) 몫 실패: {quotient_b}"
assert remainder_b == 16*x - 16, f"조건 (나) 나머지 실패: {remainder_b}"

# 조건 (다): B(2) > 0
B_at_2 = B.subs(x, 2)
assert B_at_2 > 0, f"조건 (다) 실패: B(2)={B_at_2}"

# A(x)가 Q(x)로 나누어떨어지는지 확인
quotient_A_by_Q, remainder_A_by_Q = sp.div(A, Q)
assert remainder_A_by_Q == 0, f"A(x)가 Q(x)로 나누어떨어지지 않음: 나머지={remainder_A_by_Q}"

# A(3) 계산
result = A.subs(x, 3)
assert result == 68, f"A(3) 계산 오류: {result}"

print('VERIFY_PASS')