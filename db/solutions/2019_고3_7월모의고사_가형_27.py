"""2019 고3 7월모의고사 가형 27번 — 파라미터화 솔버.

문제 구조:
  n개의 레인(1..n) 중에서 k명의 학생이 서로 다른 레인을 하나씩 고른다.
  선택된 k개의 번호 중 어느 두 번호도 연속하지 않도록 하는 경우의 수.

수학적 풀이:
  먼저 '레인 번호 집합'만 고른다(학생 구분 없이). 1..n 중 어느 두 수도
  연속하지 않는 k개의 부분집합의 개수는 조합론의 표준 결과로
      C(n - k + 1, k)
  이다(작은 수부터 정렬해 i번째 값에서 (i-1)을 빼면 서로 다른 k개의
  1..(n-k+1) 값과 1대1 대응 — stars and bars 아이디어).
  이후 k명의 학생이 서로 다른 사람이므로 뽑힌 k개의 레인을 학생들에게
  배정하는 순서 k! 을 곱한다.

파라미터:
  n : 레인 개수 (원문제 8)
  k : 학생 수   (원문제 3)
  두 값 모두 답을 바꾼다 — n은 고를 수 있는 레인 풀의 크기를, k는
  뽑는 개수와 순열 배정(k!) 양쪽에 영향을 준다.
"""
import sympy as sp

CANDIDATE = 120                    # ★원문제 정답 — 절대 바꾸지 않는다
PARAMS = dict(n=8, k=3)


def solve(prm):
    n = int(prm['n'])
    k = int(prm['k'])
    if n <= 0 or k <= 0:
        raise ValueError('레인 수와 학생 수는 자연수여야 한다')
    if k > n:
        raise ValueError('학생 수가 레인 수보다 많으면 서로 다른 레인을 고를 수 없다')
    # 1..n 중 어느 두 수도 연속하지 않는 k개짜리 부분집합의 개수
    subset_count = sp.binomial(n - k + 1, k)
    # 서로 다른 학생들에게 뽑힌 레인을 배정 — k!
    return subset_count * sp.factorial(k)


def statement(prm):
    n = prm['n']
    k = prm['k']
    return (
        f"어느 수영장에 1번부터 {n}번까지 {n}개의 레인이 있다.\n"
        f"{k}명의 학생이 서로 다른 레인의 번호를 각각 1개씩 선택할 때, "
        f"{k}명의 학생이 선택한 레인의 번호 중 어느 두 번호도 연속되지 않도록 "
        f"선택하는 경우의 수를 구하시오."
    )


VARIANTS = [
    dict(n=8, k=3),   # 원문제 그대로 — 답 120
    dict(n=9, k=3),   # 레인 수만 늘림 — 답 C(7,3)*3! = 210
    dict(n=10, k=4),  # 레인 수·학생 수 모두 변경 — 답 C(7,4)*4! = 840
]

assert solve(PARAMS) == CANDIDATE
print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
