# log_3(x+4) ≤ 3 + log_{1/3}(x-2) 를 만족하는 정수 x 의 합.
# 밑변환 log_{1/3}(x-2) = -log_3(x-2) → log_3((x+4)(x-2)) ≤ 3 → (x+4)(x-2) ≤ 27.
# ★진수조건 x>2 를 반드시 함께 건다(빠뜨리면 음수 정수가 딸려 들어온다).
CANDIDATE = 12
import sympy as sp

x = sp.symbols('x', real=True)
lhs = sp.log(x + 4, 3)
rhs = 3 + sp.log(x - 2, sp.Rational(1, 3))
ints = []
for n in range(3, 200):                       # 진수조건 x>2 → 정수는 3 이상
    ok = sp.simplify(sp.nsimplify(rhs.subs(x, n) - lhs.subs(x, n)))
    if sp.N(ok) >= 0:                          # 부등식을 실제 값으로 판정
        ints.append(n)
    elif ints:
        break                                  # (x+4)(x-2) 는 증가 → 한 번 깨지면 끝
print('VERIFY_PASS' if sp.Integer(sum(ints)) == CANDIDATE else 'VERIFY_FAIL')
