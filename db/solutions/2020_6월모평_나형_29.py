# 2020 6월모평 나형 29: 음이 아닌 정수 x1,x2,x3 의 순서쌍 개수.
# (가) n=1,2 일 때 x_{n+1}-x_n >= 2   (나) x3 <= 10.
CANDIDATE = 84
count = 0
for x1 in range(0, 11):
    for x2 in range(0, 11):
        for x3 in range(0, 11):
            if x2 - x1 >= 2 and x3 - x2 >= 2 and x3 <= 10:   # (가)+(나)
                count += 1
print('VERIFY_PASS' if count == CANDIDATE else 'VERIFY_FAIL')
