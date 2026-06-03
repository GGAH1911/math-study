count = 0
for a in range(1, 7):
    for b in range(1, 7):
        for c in range(1, 7):
            for d in range(1, 7):
                sa = a if a <= 3 else 0
                sb = b if b <= 3 else 0
                sc = c if c <= 3 else 0
                sd = d if d <= 3 else 0
                if sa + sb + sc + sd == 4:
                    count += 1
if count == 199:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {count}')