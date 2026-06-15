# 2020 6월모평 나형 28: 첫째항 2, 공비 정수인 등비수열 {a_n}, 자연수 m.
# (가) 4 < a_2 + a_3 <= 12   (나) sum_{k=1}^m a_k = 122.  a_m?
CANDIDATE = 162
a1 = 2
found = []
for r in range(-12, 13):          # 공비는 정수
    a2, a3 = a1 * r, a1 * r**2
    if not (4 < a2 + a3 <= 12):   # 조건 (가)
        continue
    for m in range(1, 40):        # 조건 (나): 부분합 = 122
        s = sum(a1 * r**(k - 1) for k in range(1, m + 1))
        if s == 122:
            found.append(a1 * r**(m - 1))   # a_m
ans = found[0] if len(set(found)) == 1 and found else None
print('VERIFY_PASS' if ans == CANDIDATE else 'VERIFY_FAIL')
