f = {1: 5, 2: 3, 3: 4}
g = {3: 1, 4: 3, 5: 2}
gf3 = g[f[3]]
fg3 = f[g[3]]
result = gf3 - fg3
choices = {1: -4, 2: -3, 3: -2, 4: -1, 5: 0}
my_answer = 3
if result == -2 and choices[my_answer] == result:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
