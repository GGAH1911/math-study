from math import comb, factorial

# Step 1: A, B, C 포함하여 5명 선택
# A, B, C는 고정, 나머지 4명 중 2명 선택
select_ways = comb(4, 2)
print(f'선택 경우의 수: {select_ways}')

# Step 2: 5명을 원탁에 배치 (회전 동일 처리)
# 원탁 순열: (5-1)! = 4!
arrange_ways = factorial(4)
print(f'원탁 배치 경우의 수: {arrange_ways}')

# Step 3: 전체 경우의 수
total = select_ways * arrange_ways
print(f'전체 경우의 수: {total}')

if total == 144:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')