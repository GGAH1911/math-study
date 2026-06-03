from math import comb

# A에 넣을 3개 선택
ways_choose_A = comb(6, 3)
print(f'A에 3개 선택: {ways_choose_A}')

# 남은 3개를 B, C에 배치
ways_distribute_BC = 2**3
print(f'남은 3개를 B,C에 배치: {ways_distribute_BC}')

# 전체 경우의 수
total = ways_choose_A * ways_distribute_BC
print(f'전체 경우의 수: {total}')

if total == 160:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')