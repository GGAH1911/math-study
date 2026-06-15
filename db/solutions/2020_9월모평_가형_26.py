# 2020 9월모평 가형 26: f(x)=3 sin(kx)+4x^3 가 변곡점을 오직 하나 갖게 하는 k의 최댓값?
# f''(x) = -3k^2 sin(kx) + 24x.  f''=0 ⟺ 8x = k^2 sin(kx).
# psi(x)=8x - k^2 sin(kx), psi'(x)=8 - k^3 cos(kx).  min psi' = 8 - k^3.
# 유일 변곡점(psi 단조, 근 x=0 뿐) ⟺ 8 - k^3 >= 0 ⟺ k <= 2.  최댓값은 8-k^3=0 → k=2.
CANDIDATE = 2
k = CANDIDATE
mono_at_k = 8 - k ** 3                 # k 에서 단조 경계 (>=0 이어야)
breaks_just_above = 8 - (k + 0.01) ** 3  # k 바로 위에서는 음수 (=k가 최댓값)
print('VERIFY_PASS' if mono_at_k >= 0 and breaks_just_above < 0 else 'VERIFY_FAIL')
