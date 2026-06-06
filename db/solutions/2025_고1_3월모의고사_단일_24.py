deviations = [-1, 7, 3, -4, -5]
deviation_sum = sum(deviations)
assert deviation_sum == 0, f'편차의 합이 0이어야 하는데 {deviation_sum}'
variance = sum(d**2 for d in deviations) / len(deviations)
assert variance == 20, f'분산이 20이어야 하는데 {variance}'
print('VERIFY_PASS')