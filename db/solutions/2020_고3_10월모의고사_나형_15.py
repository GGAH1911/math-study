"""2020 고3 10월 전국연합학력평가(서울시교육청) 나형 15번 — 전항정답(모두 정답) 솔버.

서울시교육청의 2020.10.30 결정으로 **모두 정답 처리**된 문항이다. 따라서 이 솔버는 보기
하나를 재현하는 것이 아니라, **"왜 전항정답인가(전제가 모순)"를 수학적으로 증명**한다.

문제: 이산확률변수 X가 가지는 값은 {1, 2, 3, 4}, Y가 가지는 값은 {1, 4, 9, 16}이고
      P(X=k) = P(Y=k^2) (k=1,2,3,4), E(X)=6, V(X)=1 일 때 E(Y)?
      (보기 ① 33  ② 34  ③ 35  ④ 36  ⑤ 37)

전항정답 사유: 확률변수 X가 가지는 값이 {1,2,3,4} 뿐이면 기댓값은 그 값들의 가중평균이므로
              반드시 min(X)=1 ≤ E(X) ≤ max(X)=4 이어야 한다. 그런데 문제는 E(X)=6 (>4)을
              주므로, 이 조건을 만족하는 X의 확률분포가 **존재하지 않는다**(전제 모순).
              존재하지 않는 확률변수에 대해 E(Y)를 물으므로 어떤 보기도 옳을 수 없어
              모두 정답으로 처리됐다.
출제 의도(참고): P(X=k)=P(Y=k^2) 이면 Y는 X^2 과 분포가 같아 E(Y)=E(X^2)=V(X)+E(X)^2
              = 1 + 6^2 = 37 (보기 ⑤)을 의도한 것으로 보이나, 위 모순으로 무효다.
"""
import sympy as sp

CANDIDATE = '전항정답'                       # 서울시교육청 2020.10.30 모두 정답 처리

xs = [1, 2, 3, 4]                            # 이산확률변수 X가 가지는 값
EX_given, VX_given = 6, 1                    # 문제가 준 조건

# ── 전제 모순 증명 : X∈{1,2,3,4} 인 임의의 확률분포에서 min(xs) ≤ E(X) ≤ max(xs) ──
p = sp.symbols('p1 p2 p3 p4', nonnegative=True)     # 각 값을 가질 확률 (≥ 0)
total = sum(p)                                       # Σ p_k
EX = sum(x * pk for x, pk in zip(xs, p))             # E(X) = Σ x_k p_k

# max(xs)·Σp_k − E(X) = Σ (max−x_k)·p_k. 계수 (max−x_k) ≥ 0 이고 p_k ≥ 0 이므로 항상 ≥ 0.
# 즉 Σp_k = 1 일 때 E(X) ≤ max(xs) = 4. (대칭으로 E(X) ≥ min(xs) = 1.)
upper_slack = sp.Poly(sp.expand(max(xs) * total - EX), *p)
lower_slack = sp.Poly(sp.expand(EX - min(xs) * total), *p)
bounds_proven = (all(c >= 0 for c in upper_slack.coeffs())      # E(X) ≤ 4 증명
                 and all(c >= 0 for c in lower_slack.coeffs()))  # E(X) ≥ 1 증명
infeasible = not (min(xs) <= EX_given <= max(xs))               # 6 ∉ [1,4] → 분포 부존재

# ── 출제 의도(참고) : P(X=k)=P(Y=k^2) ⟹ Y ~ X^2 ⟹ E(Y)=E(X^2)=V(X)+E(X)^2 ──
intended_EY = VX_given + EX_given ** 2                # 1 + 36 = 37 → 보기 ⑤

ok = (CANDIDATE == '전항정답'
      and bounds_proven                              # 1 ≤ E(X) ≤ 4 가 증명되고
      and infeasible                                 # 주어진 E(X)=6 이 그 범위 밖이며
      and max(xs) == 4 and intended_EY == 37)        # 의도 답 37(⑤)도 일치
print('VERIFY_PASS' if ok else 'VERIFY_FAIL')
if not ok:
    print('bounds_proven:', bounds_proven, 'infeasible:', infeasible,
          'intended_EY:', intended_EY)
