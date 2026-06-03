count = 0
satisfying = []
for x in range(-100, 101):
    cond1 = (x**2 - 4*x - 12) <= 0
    cond2 = (x**2 - 4*x + 4) > 0
    if cond1 and cond2:
        count += 1
        satisfying.append(x)
expected = 8
if count == expected and satisfying == [-2,-1,0,1,3,4,5,6]:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
