# q: 5 ≤ x ≤ 9
# p: x ≥ a
# ¬p: x < a
# q ⟹ ¬p 확인

a = 10

# q의 범위에서 모든 x가 ¬p를 만족하는가?
q_left, q_right = 5, 9

# ¬p를 만족하려면 x < a
# q의 최댓값이 a보다 작은가?
if q_right < a:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')