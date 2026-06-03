x = 800
day1 = x
day2 = x + 300
day3 = x + 600
days_4to7 = [x + 600] * 4
total = day1 + day2 + day3 + sum(days_4to7)
if total == 8900:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')