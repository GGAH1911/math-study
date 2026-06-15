# 흰2·빨3·검3 → 3명, 빈 학생 없음, 흰 받은 학생은 빨강·검정도 각 1개 이상. 경우의수?
CANDIDATE = 72
count = 0
for w1 in range(3):
  for w2 in range(3):
    w3 = 2-w1-w2
    if w3 < 0: continue
    W = [w1,w2,w3]
    for r1 in range(4):
      for r2 in range(4):
        r3 = 3-r1-r2
        if r3 < 0: continue
        R = [r1,r2,r3]
        for b1 in range(4):
          for b2 in range(4):
            b3 = 3-b1-b2
            if b3 < 0: continue
            B = [b1,b2,b3]
            if all(W[i]+R[i]+B[i] >= 1 for i in range(3)) and \
               all(W[i] == 0 or (R[i] >= 1 and B[i] >= 1) for i in range(3)):
              count += 1
print('VERIFY_PASS' if count == CANDIDATE else 'VERIFY_FAIL')
