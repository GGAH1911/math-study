"""2019 고3 3월모의고사 가형 29번 — 파라미터화 솔버.

문제 구조: 원소가 digits 인 공들이 든 주머니에서 복원추출로 n번 뽑아
순서쌍 (a1, a2, ..., an) 을 얻는다. 원문제는 n=3, digits={0,1,2,3} 이고
a1=a, a2=b, a3=c 라 할 때 (a2*a3*...*an)/a1 = bc/a 가 정수가 되는
순서쌍의 개수를 구한다.

핵심 수학 구조:
  - a1=0 이면 분모가 0이 되어 식 자체가 정의되지 않으므로 제외.
  - 나머지 경우는 a1 이 (a2*...*an) 을 나누어떨어뜨리는지를 판정
    (정수 여부는 sympy.Rational 로 실제 계산해서 확인).

파라미터화 (답을 실제로 바꾸는 것):
  - digits: 공에 적힌 숫자 집합 (원문제: 0,1,2,3)
  - n     : 복원추출 반복 횟수, 즉 순서쌍의 길이 (원문제: 3)
"""
import sympy
from itertools import product

# 원문제: 숫자 0,1,2,3이 적힌 공 4개, 3번 복원추출
PARAMS = dict(digits=(0, 1, 2, 3), n=3)


def solve(prm):
    digits = prm['digits']
    n = prm['n']
    if n < 2:
        raise ValueError('n은 2 이상이어야 함 (분자 항이 최소 1개 필요)')
    if len(set(digits)) != len(digits):
        raise ValueError('digits 에 중복된 값이 있으면 안 됨 (서로 다른 공)')

    count = 0
    for tup in product(digits, repeat=n):
        a1 = tup[0]
        rest = tup[1:]
        if a1 == 0:
            continue  # 분모가 0 → 식이 정의되지 않음
        numerator = sympy.Integer(1)
        for x in rest:
            numerator *= sympy.Integer(x)
        if sympy.Rational(numerator, a1).is_integer:
            count += 1
    return count


CANDIDATE = 40


def statement(prm):
    digits = prm['digits']
    n = prm['n']
    var_names = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'][:n]
    if n > 8:
        var_names = [f'a{i+1}' for i in range(n)]
    nums = ', '.join(str(d) for d in digits)
    denom = var_names[0]
    numer = ''.join(var_names[1:])
    seq = ', '.join(var_names)
    return (
        f"주머니 속에 {len(digits)}개의 숫자 {nums}이 각각 하나씩 적혀 있는 "
        f"공 {len(digits)}개가 들어 있다. 이 주머니에서 1개의 공을 꺼내어 공에 "
        f"적혀 있는 수를 확인한 후 다시 넣는다. 이 과정을 {n}번 반복할 때, 꺼낸 "
        f"공에 적혀 있는 수를 차례로 {seq}라 하자. "
        f"\\frac{{{numer}}}{{{denom}}}가 정수가 되도록 하는 모든 순서쌍 "
        f"({seq})의 개수를 구하시오."
    )


assert solve(PARAMS) == CANDIDATE, solve(PARAMS)
print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
