# 파라미터화: a_n 등차(첫항 자연수, 공차 음의정수), b_n 등비(첫항 자연수, 공비 음의정수).
# (가) Σ(a_n+b_n)=S1, (나) Σ(a_n+|b_n|)=S2, (다) Σ(|a_n|+|b_n|)=S3 (n=1..5) → a_7+b_7.
S1, S2, S3 = 27, 67, 81
CANDIDATE = 117
ans = set()
for a in range(1, 80):
    for d in range(-40, 0):
        an = [a + n*d for n in range(5)]
        Sa, SAa = sum(an), sum(abs(x) for x in an)
        if SAa - Sa != S3 - S2:      # (다)-(나): Σ|a_n|-Σa_n
            continue
        for b in range(1, 80):
            for r in range(-6, 0):
                bn = [b * r**n for n in range(5)]
                Sb, SAb = sum(bn), sum(abs(x) for x in bn)
                if Sa + Sb != S1:            # (가)
                    continue
                if SAb - Sb != S2 - S1:      # (나)-(가): Σ|b_n|-Σb_n
                    continue
                ans.add((a + 6*d) + b * r**6)   # a_7 + b_7
print('VERIFY_PASS' if ans == {CANDIDATE} else 'VERIFY_FAIL')
