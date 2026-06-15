# 2020 9월모평 나형 29: (가형 28과 동일 문제) 연필 7·볼펜 4 → 여3·남2 분배.
# (가) 여학생 연필 a 동일, 남학생 볼펜 b 동일.  (나) a>=1  (다) b>=1.
CANDIDATE = 49
count = 0
for a in range(0, 8):
    for b1 in range(0, 8):
        for b2 in range(0, 8):
            if 3 * a + b1 + b2 != 7 or a < 1:
                continue
            for pb in range(0, 5):
                for c1 in range(0, 5):
                    for c2 in range(0, 5):
                        for c3 in range(0, 5):
                            if 2 * pb + c1 + c2 + c3 != 4 or pb < 1:
                                continue
                            count += 1
print('VERIFY_PASS' if count == CANDIDATE else 'VERIFY_FAIL')
