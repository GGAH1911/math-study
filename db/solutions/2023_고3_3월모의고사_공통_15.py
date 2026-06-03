import sympy as sp

def compute_sequence(a1, a2, steps):
    a = [a1, a2]
    for _ in range(2, steps):
        s = a[-1] + a[-2]
        if s % 2 == 1:
            a.append(s)
        else:
            a.append(s // 2)
    return a

# Verify both solutions
sol1 = compute_sequence(1, 19, 6)
sol2 = compute_sequence(1, 49, 6)

print(f'a2=19: {sol1}, a6={sol1[5]}')
print(f'a2=49: {sol2}, a6={sol2[5]}')

if sol1[5] == 34 and sol2[5] == 34:
    total = 19 + 49
    print(f'Sum of all a2: {total}')
    if total == 68:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')