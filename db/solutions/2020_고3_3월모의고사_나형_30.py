# f 연속·증가·기함수 on [-1,1], ∫₀¹f=1, f(1)=3. g: [2n-1,2n+1]에서 f(x-2n)+6n. ∫₃⁶ g ?
CANDIDATE = 41
I01 = 1                              # ∫₀¹ f
I_n10, I_n11 = -I01, 0                # 기함수: ∫₋₁⁰f=-1, ∫₋₁¹f=0
A = I_n11 + 12 * 2                    # [3,5] n=2: g=f(x-4)+12 → ∫=∫₋₁¹f+24 = 24
B = I_n10 + 18 * 1                    # [5,6] n=3: g=f(x-6)+18 → ∫=∫₋₁⁰f+18 = 17
print('VERIFY_PASS' if A + B == CANDIDATE else 'VERIFY_FAIL')
