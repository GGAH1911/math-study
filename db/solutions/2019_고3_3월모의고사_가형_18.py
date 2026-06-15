from itertools import product

# f(n): 4 boxes each 0..5, sum = n
def f(n):
    count = 0
    for combo in product(range(6), repeat=4):
        if sum(combo) == n:
            count += 1
    return count

p = f(15)  # (가)
q_raw = f(14)  # actual f(14)
four_H_6 = 84  # 4H6 = C(9,3)
q = four_H_6 - q_raw  # (나) = 4H6 - f(14) ... wait, f(14) = 4H6 - (나), so (나) = 4H6 - f(14)
r = f(13)  # (다)

print(f'f(15)={f(15)}, p={p}')
print(f'f(14)={f(14)}, 4H6={four_H_6}, (나)=q={four_H_6 - f(14)}')
print(f'f(13)={f(13)}, r={r}')

p_val = f(15)
q_val = four_H_6 - f(14)
r_val = f(13)
total = p_val + q_val + r_val
print(f'p+q+r = {p_val}+{q_val}+{r_val} = {total}')

CANDIDATE = 164
if total == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
