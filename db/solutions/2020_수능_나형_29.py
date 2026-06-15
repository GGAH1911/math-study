# 2020 수능 나형 29: 사탕 6(동일)·초콜릿 5(동일)을 A,B,C 에게 남김없이 분배.
# (가) A 사탕>=1  (나) B 초콜릿>=1  (다) C 의 (사탕+초콜릿)>=1.
CANDIDATE = 285
count = 0
for a1 in range(0, 7):           # A,B,C 사탕
    for a2 in range(0, 7):
        for a3 in range(0, 7):
            if a1 + a2 + a3 != 6 or a1 < 1:        # 사탕 6, (가)
                continue
            for b1 in range(0, 6):                 # A,B,C 초콜릿
                for b2 in range(0, 6):
                    for b3 in range(0, 6):
                        if b1 + b2 + b3 != 5 or b2 < 1 or a3 + b3 < 1:  # 초콜릿 5, (나),(다)
                            continue
                        count += 1
print('VERIFY_PASS' if count == CANDIDATE else 'VERIFY_FAIL')
