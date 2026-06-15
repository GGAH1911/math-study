"""2019 고3 4월모의고사 나형 7번 — 파라미터 솔버 (수동 작성).
문제: y=f(x) 그래프(그림). f(0) + lim_{x→2+} f(x). (답 ④ 8)
그림 판독: f(0)=3 (채워진 점 (0,3)); x→2+ 의 오른쪽 가지는 빈 점 (2,5)에서 시작 → lim=5.
구조: 3 + 5 = 8.
재생산: 그래프 핵심값(점값·편측극한) 파라미터화.
"""


def solve(f0, right_lim_at2):
    return f0 + right_lim_at2


F0 = 3                  # 채워진 점 (0,3)
RLIM = 5                # x→2+ : 빈 점 (2,5)서 시작하는 가지
CANDIDATE = 8           # 보기 ④
assert solve(F0, RLIM) == CANDIDATE
print('VERIFY_PASS')
