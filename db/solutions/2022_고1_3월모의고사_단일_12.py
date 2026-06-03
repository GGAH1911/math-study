# 구입한 구슬 개수 x = 1300
x = 1300
n = 5

# 조건 1: 250개씩 n개 상자에 담으면 50개 남음
condition1 = (x == 250 * n + 50)

# 조건 2: 200개씩 (n+1)개 상자에 담으면 100개 남음
condition2 = (x == 200 * (n + 1) + 100)

if condition1 and condition2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')