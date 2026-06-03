from math import comb

# A에서 P까지: 오른쪽 3, 위 1
path_A_to_P = comb(3 + 1, 1)
print(f'A to P: {path_A_to_P}')

# P에서 B까지: 오른쪽 1, 위 1  
path_P_to_B = comb(1 + 1, 1)
print(f'P to B: {path_P_to_B}')

# 전체 경로
total_paths = path_A_to_P * path_P_to_B
print(f'Total: {total_paths}')

if total_paths == 8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')