# 5분야×10권, 24권 선택. (가) 철학·사회·자연 각 4권 이상. (나) 문학·역사는 0 또는 4권 이상. 경우의수?
CANDIDATE = 396
v123 = range(4, 11)              # 철학·사회·자연: 4~10
v45 = [0] + list(range(4, 11))   # 문학·역사: 0 또는 4~10
count = 0
for x1 in v123:
    for x2 in v123:
        for x3 in v123:
            for x4 in v45:
                for x5 in v45:
                    if x1+x2+x3+x4+x5 == 24:
                        count += 1
print('VERIFY_PASS' if count == CANDIDATE else 'VERIFY_FAIL')
