#!/usr/bin/env python3
"""유사문제 무한생성 PoC — '검증기를 파라미터화하면 무한 생성된다'를 #18 유형으로 증명.

#18 검증기(db/solutions/2026_고2_6월모의고사_단일_18.py)는 AB=2, R=3√3/5 를 '하드코딩'한
1회용 체크다. 그 안의 수학 구조(사인법칙→p, 코사인법칙→QA²)를 상수→파라미터로 들어올리면
generate(AB, p, ratio) 가 되고, sympy가 답을 '구성적으로' 계산하므로 LLM 신뢰 없이 정답이 보장된다.

핵심: 답을 '코사인법칙 경로'로 만들고, '사인법칙 경로(다른 유도)'로 독립 재계산해 일치를 확인 →
      자가-검증(self-verifying) 생성. 두 경로가 우연히 같을 수 없으므로 통과=정답.
"""
import sympy as sp


def generate(AB, p, a, b):
    """두 원+공통접선+접선현각 유형 한 인스턴스. ratio sinθ1:sinθ2 = √a:√b, p=sin(θ1+θ2)=AB/2R.
    well-posed 조건: 0<p<1 (∠APB<∠AQB ⇒ θ1+θ2 예각). 반환 None = 무효 파라미터(스킵)."""
    AB, p = sp.nsimplify(AB), sp.nsimplify(p)
    if not (0 < p < 1):
        return None
    R = sp.simplify(AB / (2 * p))            # 외접원 반지름 (사인법칙 역산)
    cos_sum = sp.sqrt(1 - p**2)              # cos(θ1+θ2), 예각이라 +
    q = sp.sqrt(sp.Rational(a, b))           # sinθ1/sinθ2
    # 코사인법칙 경로: ∠AQB=π-(θ1+θ2) → AB² = QA²(1+q²+2q·cos_sum)
    QA2 = sp.simplify(AB**2 / (1 + q**2 + 2 * q * cos_sum))
    answer = sp.simplify(p * q * QA2)        # p×q×r²  (원문이 묻는 값)
    return dict(AB=AB, R=sp.nsimplify(R), ratio=f'√{a}:√{b}', p=p, q=q, QA2=QA2, answer=answer)


def independent_check(v):
    """사인법칙 경로(코사인 경로와 독립)로 답을 재계산 + 도형 제약 수치 검증."""
    p, q, AB = v['p'], v['q'], v['AB']
    S = sp.asin(p)                                   # θ1+θ2
    th2 = sp.atan(sp.sin(S) / (q + sp.cos(S)))       # tanθ2 = sinS/(q+cosS)
    th1 = S - th2
    # (1) 비율 제약 재확인: sinθ1/sinθ2 == q ?
    ratio_ok = abs(float(sp.N(sp.sin(th1) / sp.sin(th2) - q))) < 1e-12
    # (2) 외접원 제약: R == AB/(2 sinS) ?
    R_ok = abs(float(sp.N(AB / (2 * sp.sin(S)) - v['R']))) < 1e-12
    # (3) 답 독립 재계산: 사인법칙 QA = AB·sinθ2/sinS  (코사인법칙 안 씀)
    QA = AB * sp.sin(th2) / sp.sin(S)
    ans2 = p * q * QA**2
    ans_ok = abs(float(sp.N(ans2 - v['answer']))) < 1e-12
    return ratio_ok and R_ok and ans_ok


# ── 무한 생성: 파라미터만 바꾸면 끝. (AB, p, a, b) 5종 + 원문 재현 ──
PARAMS = [
    (2, sp.Rational(5, 9) * sp.sqrt(3), 3, 2),   # ← 원문 #18 재현 (답 20√2/19 나와야)
    (3, sp.Rational(3, 4), 5, 3),
    (4, sp.Rational(2, 3), 2, 1),
    (6, sp.Rational(3, 5), 7, 4),
    (5, sp.Rational(1, 2), 5, 2),
    (2, sp.Rational(9, 5), 3, 2),                # ← p>1 무효 (AB>2R): 스킵돼야 정상
]

print("═══ #18 유형 파라미터화 생성 + 독립검증 ═══\n")
ok = skip = 0
for i, (AB, p, a, b) in enumerate(PARAMS, 1):
    v = generate(AB, p, a, b)
    if v is None:
        print(f"  [{i}] AB={AB}, p={p}  → 무효 파라미터(p∉(0,1)) 스킵 ✓")
        skip += 1
        continue
    passed = independent_check(v)
    tag = 'VERIFY_PASS ✅' if passed else 'VERIFY_FAIL ❌'
    print(f"  [{i}] AB={v['AB']}, R={v['R']}, ratio={v['ratio']}")
    print(f"        → 답 p×q×r² = {v['answer']}   [{tag}]")
    ok += passed
print(f"\n생성·검증 통과 {ok} · 무효스킵 {skip}  (각 답은 sympy 구성적 계산 + 사인↔코사인 2경로 교차검증)")
