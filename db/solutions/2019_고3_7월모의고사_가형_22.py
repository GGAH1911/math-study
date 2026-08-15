import sympy as sp

CANDIDATE = 200

# 문제의 수학 구조: _{n}P_{r1} \times _{n}C_{r2} 형태의 순열·조합 곱
#  - n  : 전체 대상 개수 (원문제: 5)
#  - r1 : 순열(P)에서 뽑는 개수 (원문제: 2)
#  - r2 : 조합(C)에서 뽑는 개수 (원문제: 2)
# 세 값을 바꾸면 nPr1, nCr2 각각의 계산값이 달라지므로 최종 곱(답)도 달라진다.
PARAMS = dict(n=5, r1=2, r2=2)


def solve(prm):
    n, r1, r2 = prm['n'], prm['r1'], prm['r2']
    if not (0 <= r1 <= n and 0 <= r2 <= n):
        raise ValueError('r1, r2 는 0 이상 n 이하여야 한다')
    # nPr = n! / (n-r)!,  nCr = n! / (r! (n-r)!)  — sympy 로 실제 계산
    n_s, r1_s, r2_s = sp.Integer(n), sp.Integer(r1), sp.Integer(r2)
    nPr1 = sp.factorial(n_s) / sp.factorial(n_s - r1_s)
    nCr2 = sp.factorial(n_s) / (sp.factorial(r2_s) * sp.factorial(n_s - r2_s))
    return sp.nsimplify(nPr1 * nCr2)


def statement(prm):
    n, r1, r2 = prm['n'], prm['r1'], prm['r2']
    return f"_{{{n}}}\\mathrm{{P}}_{{{r1}}} \\times _{{{n}}}\\mathrm{{C}}_{{{r2}}}의 값을 구하시오."


if __name__ == '__main__':
    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
