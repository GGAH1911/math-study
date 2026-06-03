import math
from itertools import combinations, permutations

# 전체 원순열
total_circular = math.factorial(6)
print(f'전체 원순열: {total_circular}')

# B학생이 이웃하는 경우
# B 2명을 한 단위로 보면 6명 원순열
adjacent_units = math.factorial(5) * math.factorial(2)
print(f'B학생이 이웃하는 경우: {adjacent_units}')

# B학생이 이웃하지 않는 경우
not_adjacent = total_circular - adjacent_units
print(f'B학생이 이웃하지 않는 경우: {not_adjacent}')

# 검증: A학생 5명 배치 후 B학생을 간격에 배치
a_circular = math.factorial(4)
gaps = 5
b_selections = math.comb(5, 2)
b_permutations = math.factorial(2)
verify_result = a_circular * b_selections * b_permutations
print(f'검증 (A배치 후 간격선택): {verify_result}')

if not_adjacent == 480 and verify_result == 480:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')