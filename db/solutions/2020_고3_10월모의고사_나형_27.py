# a+b+c=14 (음 아닌 정수), (a-2)(b-2)(c-2)≠0. 순서쌍 개수?
CANDIDATE = 84
count = sum(1 for a in range(15) for b in range(15-a)
            if (14-a-b) >= 0 and a != 2 and b != 2 and (14-a-b) != 2)
print('VERIFY_PASS' if count == CANDIDATE else 'VERIFY_FAIL')
