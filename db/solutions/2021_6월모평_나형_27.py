from math import comb

# 전체: a+b+c+d=6, a,b,c,d >= 0
total = comb(9, 3)
print(f'전체 경우의 수: {total}')

# 모두 양수: a,b,c,d >= 1, a+b+c+d=6
# 치환 후: a'+b'+c'+d'=2, a',b',c',d' >= 0
all_positive = comb(5, 3)
print(f'모두 양수인 경우: {all_positive}')

# 적어도 하나는 0
answer = total - all_positive
print(f'적어도 하나는 0: {answer}')

if answer == 74:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')