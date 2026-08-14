"""2019 고3 10월모의고사 나형 25번 — 파라미터화 솔버.

원문제: 전체집합 U={1,...,9}의 부분집합 A는
  "m이 A의 원소이면, m^2의 일의 자릿수(=mod 10 나머지)와 n^2의 일의 자릿수가
   같아지는 m이 아닌 자연수 n이 A에 존재한다"
를 만족한다. 공집합이 아닌 A의 개수를 구하시오. (답 15)

[수학 구조]
  1..N을 "m^power를 mod로 나눈 나머지" 값으로 그룹화하면, 같은 그룹끼리는 서로 '짝'이 되어
  조건을 만족시켜줄 수 있다. 어떤 그룹(크기 s)에서 A에 포함되는 원소 수가
  1이면 그 원소는 짝이 없어 조건을 위반하므로 불가능하고, 0이거나 2 이상이면
  포함된 원소끼리 서로 짝이 되어줄 수 있어 항상 가능하다. 즉 크기 s인 그룹에서
  "크기 1을 제외한" 부분집합 개수는 2^s - s (전체 2^s개 중 크기 정확히 1인
  s개를 뺌; 원문제의 {5}처럼 s=1이면 2^1-1=1, 즉 공집합만 허용).
  그룹들은 서로 독립이므로 전체 개수는 각 그룹의 (2^s - s)를 모두 곱한 값이고,
  거기서 전부 공집합인 경우(공집합 A) 1가지를 빼면 답이 된다:
      답 = ∏_그룹 (2^{s_i} - s_i) - 1

  파라미터로 뽑은 것: N(전체집합의 최댓값), mod(모듈러스, "일의 자릿수"→10),
  power(거듭제곱 지수, 원문제는 제곱→2). N과 mod가 그룹 구성(각 그룹의 크기
  s_i)을 실제로 바꾸어 답을 바꾼다.
"""
import sympy
from collections import defaultdict

CANDIDATE = 15  # ★원문제 정답, 절대 변경 금지

PARAMS = dict(
    N=9,      # 전체집합 U = {1, 2, ..., N}
    mod=10,   # "일의 자릿수" == mod 10 나머지
    power=2,  # m^power (원문제는 제곱)
)


def solve(prm):
    N = prm['N']
    mod = prm['mod']
    power = prm['power']
    if N < 1 or mod < 1:
        raise ValueError("N, mod는 1 이상이어야 함")

    U = list(range(1, N + 1))

    # sympy로 각 m에 대해 m^power mod mod 값을 실제로 계산하여 그룹화한다.
    groups = defaultdict(list)
    for m in U:
        r = sympy.Mod(sympy.Integer(m) ** power, mod)
        groups[int(r)].append(m)

    # 각 그룹(크기 s)에서 "그 그룹에서 정확히 1개만 뽑는" 경우만 금지된다.
    # 유효한 부분집합 수 = 2^s - s (sympy로 실제 계산)
    prod = sympy.Integer(1)
    for v in groups.values():
        s = len(v)
        prod *= (sympy.Integer(2) ** s - s)

    # 모든 그룹에서 공집합을 뽑는 경우(=전체 A가 공집합)는 제외
    total = prod - 1

    if total <= 0:
        raise ValueError("조건을 만족하는 공집합이 아닌 A가 존재하지 않음")

    # 전수검증: 실제로 모든 부분집합을 순회하며 조건을 확인해 공식과 일치하는지 대조
    import itertools
    cnt = 0
    for r in range(1, len(U) + 1):
        for A in itertools.combinations(U, r):
            S = set(A)
            ok = True
            for m in A:
                if not any(n != m and (n ** power) % mod == (m ** power) % mod for n in S):
                    ok = False
                    break
            if ok:
                cnt += 1

    result = int(total)
    assert cnt == result, (cnt, result)
    return result


def statement(prm):
    N = prm['N']
    mod = prm['mod']
    power = prm['power']
    return (
        f"전체집합 U = {{x | x는 {N} 이하의 자연수}}의 부분집합 A는 다음 조건을 만족시킨다.\n"
        f"  m이 집합 A의 원소이면, m^{power}을 {mod}로 나눈 나머지와 n^{power}을 {mod}로 나눈 나머지가 "
        f"같아지는 m이 아닌 자연수 n이 집합 A에 존재한다.\n"
        f"공집합이 아닌 집합 A의 개수를 구하시오."
    )


# 원문제 파라미터로 답이 그대로 재현되는지 확인
assert solve(PARAMS) == CANDIDATE

# N만 바꿔도 답이 달라짐 (그룹 구성이 바뀌어 k가 바뀜)
_variant_N = dict(PARAMS, N=15)
assert solve(_variant_N) != CANDIDATE

# mod만 바꿔도 답이 달라짐
_variant_mod = dict(PARAMS, mod=6)
assert solve(_variant_mod) != CANDIDATE

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
