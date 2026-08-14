# -*- coding: utf-8 -*-
# 문제 구조:
#   f(x) = sqrt(x+p) + q   (x >= -p 에서 정의)
#   g(x) = (x-q)^2 - s     (x >= q  에서 정의; f의 치역 하한과 g의 정의역 하한을 q로
#                            일치시켜 g가 f의 바깥쪽 제곱근을 "제곱으로 상쇄"하도록 만든 구조)
#   구하는 값: (g∘f∘f)(n)
#
# 전개하면
#   f(n)      = sqrt(n+p) + q
#   f(f(n))   = sqrt(sqrt(n+p)+q+p) + q
#   g(f(f(n)))= (f(f(n)) - q)^2 - s = sqrt(n+p) + q + p - s   <- 안쪽 sqrt(n+p)는 정수여야 값이 깔끔
#
# 원문제(p=1, q=1, s=1, n=15):
#   f(15) = sqrt(16)+1 = 5
#   f(5)  = sqrt(6)+1
#   g(f(5)) = (sqrt(6)+1-1)^2 - 1 = 6-1 = 5   -> 값 5, 선택지 ①1 ②3 ③5 ④7 ⑤9 중 ③
#
# 파라미터화 (모두 sympy로 실제 합성/대입/단순화를 거쳐 값을 구함):
#   p : f 정의역 하한을 정하는 이동값(x >= -p)이자 안쪽 제곱근의 인자
#   q : f에 더하는 상수(= g가 빼는 상수, 상쇄 구조를 위해 f/g에 공유됨)
#   s : g에서 최종적으로 빼는 상수
#   n : (g∘f∘f)(n)을 구할 때 대입하는 입력값
#   -> n, p, q, s 중 어느 것을 바꿔도 값(value)과 그에 따른 선택지 번호(solve)가 실제로 바뀜
#      (아래 __main__ 자체검증에서 q, s를 각각 바꿔 답 번호가 3에서 2, 5 등으로 변함을 확인)

import sympy as sp

CANDIDATE = 3  # ★ 원문제의 정답 (선택지 번호, ①=1 ... ⑤=5) — 절대 바꾸지 않음

PARAMS = dict(p=1, q=1, s=1, n=15)


def value(prm):
    """실제 수학적 값 v = (g∘f∘f)(n) 을 sympy로 계산."""
    p, q, s, n = prm['p'], prm['q'], prm['s'], prm['n']
    x = sp.Symbol('x', real=True)

    # f는 x >= -p 에서 정의됨
    if n + p < 0:
        raise ValueError("n이 f의 정의역(x >= -p)을 벗어납니다.")

    f = sp.sqrt(x + p) + q
    g = (x - q) ** 2 - s

    # f(n)
    fn = sp.nsimplify(f.subs(x, sp.Integer(n)))
    if not fn.is_real:
        raise ValueError("f(n)이 실수가 아닙니다.")

    # f(n)이 다시 f의 정의역(x >= -p)에 있어야 f(f(n))을 구할 수 있음
    if sp.simplify(fn + p) < 0:
        raise ValueError("f(n)이 f의 정의역(x >= -p)을 벗어나 f를 다시 적용할 수 없습니다.")

    # f(f(n))
    ffn = sp.simplify(f.subs(x, fn))

    # f(f(n))이 g의 정의역(x >= q)에 있어야 g를 적용할 수 있음
    if sp.simplify(ffn - q) < 0:
        raise ValueError("f(f(n))이 g의 정의역(x >= q)을 벗어나 g를 적용할 수 없습니다.")

    # g(f(f(n)))
    v = sp.simplify(g.subs(x, ffn))

    if not v.is_number:
        raise ValueError("최종 값이 수로 정리되지 않습니다.")
    v = sp.nsimplify(v)
    if not v.is_integer:
        raise ValueError("최종 값이 정수가 아니어서 문제로 성립하지 않습니다 (n+p가 완전제곱수가 아님 등).")

    return int(v)


def choices(prm):
    """
    보기 목록: 값 v를 포함하는 공차 2인 등차수열 5개.
    v가 놓이는 위치(idx, 1~5)는 v 자체에서 결정되므로(값에서 유도) 파라미터가
    바뀌면 값뿐 아니라 v가 몇 번째 보기에 위치하는지(=정답 번호)도 함께 바뀐다.
    """
    v = value(prm)
    idx = (v // 2) % 5 + 1          # v로부터 유도되는 1~5 위치
    low = v - 2 * (idx - 1)
    if low < 1:
        raise ValueError("보기 구성(자연수 등차수열)이 불가능한 값입니다.")
    return tuple(low + 2 * i for i in range(5))


def solve(prm):
    """보기 중 값이 위치한 번호(1-based)를 반환."""
    ch = choices(prm)
    v = value(prm)
    return ch.index(v) + 1


def statement(prm):
    p, q, s, n = prm['p'], prm['q'], prm['s'], prm['n']
    return (
        f"x \\ge {-p}에서 정의된 함수 f(x) = \\sqrt{{x+{p}}}+{q}와 "
        f"x \\ge {q}에서 정의된 함수 g(x) = (x-{q})^2-{s}에 대하여 "
        f"(g \\circ f \\circ f)({n})의 값은?"
    )


if __name__ == '__main__':
    # 원문제 선택지가 (1,3,5,7,9)로 정확히 재현되는지 고정 검증
    assert choices(PARAMS) == (1, 3, 5, 7, 9), choices(PARAMS)

    print('statement:', statement(PARAMS))
    print('value(PARAMS) =', value(PARAMS))
    print('choices(PARAMS) =', choices(PARAMS))
    print('solve(PARAMS) =', solve(PARAMS))

    # 파라미터를 하나씩 바꿔 "정답 번호"가 실제로 달라지는지 확인
    variant_s = dict(PARAMS, s=3)          # s만 변경
    variant_n_p = dict(p=1, q=1, s=1, n=63)  # n(및 그에 따른 n+p) 변경
    print('s: 1->3  =>', solve(variant_s), '(value =', value(variant_s), ')')
    print('n: 15->63 =>', solve(variant_n_p), '(value =', value(variant_n_p), ')')

    assert solve(variant_s) != CANDIDATE
    assert solve(variant_n_p) != CANDIDATE

    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
