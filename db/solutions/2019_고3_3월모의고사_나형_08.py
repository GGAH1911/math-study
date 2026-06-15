"""2019 고3 3월모의고사 나형 8번 — 검증 (수동 작성).
문제: 자연수 x에 대한 명제 '5≤x≤9 이면 x≤8 이다.' 가 거짓임을 보여 주는 x의 값은?
      ① 6  ② 7  ③ 8  ④ 9  ⑤ 10   (정답 ④, 값 9)
원리: 조건명제 p→q 가 거짓 ⇔ (가정 p 참) ∧ (결론 q 거짓).
      p: 5≤x≤9,  q: x≤8.  → 반례는 5≤x≤9 이면서 x>8 인 자연수 = 9.
      ⑤ x=10 은 p(가정)가 거짓이므로 p→q 는 공허하게 참 → 반례 아님.
검증: 다섯 보기에 대해 (p ∧ ¬q) 를 평가, 참이 되는 유일한 보기가 ④(값 9)인지 확인.
"""
choices = {1: 6, 2: 7, 3: 8, 4: 9, 5: 10}
p = lambda x: 5 <= x <= 9          # 가정 (전건)
q = lambda x: x <= 8               # 결론 (후건)

# 명제 p→q 가 거짓 ⇔ 가정 참 & 결론 거짓
counterexamples = [c for c, x in choices.items() if p(x) and not q(x)]

print('VERIFY_PASS' if counterexamples == [4] else f'VERIFY_FAIL:{counterexamples}')
