# 주어진 조건에서 유도한 a_1, b_1 검증
a1 = -1
b1 = 1

# 등차수열: 공차 3
a2 = a1 + 3
a4 = a1 + 3 * 3

# 등비수열: 공비 2
b2 = b1 * 2
b4 = b1 * (2 ** 3)

# 조건 확인
if a2 == b2 and a4 == b4:
    # 답 확인
    answer = a1 + b1
    if answer == 0:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')