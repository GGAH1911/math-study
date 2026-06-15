# 2020 9월모평 가형 28: 연필 7(동일)·볼펜 4(동일)을 여3·남2에게 남김없이 분배.
# (가) 여학생 각자 연필 a개로 동일, 남학생 각자 볼펜 b개로 동일.
# (나) a>=1 (여학생 볼펜은 0 가능)  (다) b>=1 (남학생 연필은 0 가능).
CANDIDATE = 49
count = 0
for a in range(0, 8):                     # 여학생 각자 받는 연필 수
    for b1 in range(0, 8):                # 남학생1 연필
        for b2 in range(0, 8):            # 남학생2 연필
            if 3 * a + b1 + b2 != 7 or a < 1:        # 연필 합 7, 여학생>=1
                continue
            for pb in range(0, 5):        # 남학생 각자 받는 볼펜 수
                for c1 in range(0, 5):    # 여학생1 볼펜
                    for c2 in range(0, 5):
                        for c3 in range(0, 5):
                            if 2 * pb + c1 + c2 + c3 != 4 or pb < 1:   # 볼펜 합 4, 남학생>=1
                                continue
                            count += 1
print('VERIFY_PASS' if count == CANDIDATE else 'VERIFY_FAIL')
