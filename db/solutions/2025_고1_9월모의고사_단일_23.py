x_values = [6, 7, 8]
for x in x_values:
    cond1 = 3*x <= x + 16
    cond2 = x + 8 <= 4*x - 10
    if not (cond1 and cond2):
        print('VERIFY_FAIL')
        exit()
answ = sum(x_values)
if answ == 21:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')