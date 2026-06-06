from math import factorial, comb

# 선택: A, B 포함하여 5명 선택
select = comb(6, 3)
assert select == 20, f'선택 오류: {select}'

# 5명 중 A, B 이웃하는 원탁 배치
# A, B를 하나로 묶으면 4개 단위
units = factorial(3)  # (4-1)!
ab_order = factorial(2)
adjacent = units * ab_order
assert adjacent == 12, f'이웃 배치 오류: {adjacent}'

# 전체
total = select * adjacent
assert total == 240, f'전체 오류: {total}'

print('VERIFY_PASS')