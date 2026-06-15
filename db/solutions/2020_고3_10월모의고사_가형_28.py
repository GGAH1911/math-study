# 빵3·우유4 → A,B,C. 빵만 받는 학생 없음(빵>0⟹우유>0), A 빵>=1. 경우의수?
CANDIDATE = 37
count = 0
for aA in range(1, 4):
    for aB in range(4):
        aC = 3-aA-aB
        if aC < 0: continue
        bread = [aA, aB, aC]
        for mA in range(5):
            for mB in range(5):
                mC = 4-mA-mB
                if mC < 0: continue
                milk = [mA, mB, mC]
                if all(milk[i] >= 1 for i in range(3) if bread[i] >= 1):
                    count += 1
print('VERIFY_PASS' if count == CANDIDATE else 'VERIFY_FAIL')
