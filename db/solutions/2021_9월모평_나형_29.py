from itertools import combinations_with_replacement

count = 0
for wa in range(5):
    for wb in range(5 - wa):
        wc = 4 - wa - wb
        for ba in range(7):
            for bb in range(7 - ba):
                bc = 6 - ba - bb
                if wa + ba >= 2 and wb + bb >= 2 and wc + bc >= 2:
                    count += 1

if count == 168:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')