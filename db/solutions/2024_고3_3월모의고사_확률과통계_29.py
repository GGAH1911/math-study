from itertools import combinations, product

count = 0

# 초콜릿 분배: 3개의 서로 다른 초콜릿을 3명에게 배분
# 각 초콜릿이 어느 학생에게 가는지: {0,1,2}로 표현
for choco_assignment in product(range(3), repeat=3):
    # 학생별 초콜릿 개수 계산
    c = [choco_assignment.count(i) for i in range(3)]
    
    # 조건 (가): 적어도 한 명은 초콜릿을 받지 못함
    if min(c) > 0:  # 모두 받으면 제외
        continue
    
    # 사탕 분배: 5개를 3명에게 배분
    for candy_dist in [(s1, s2, s3) for s1 in range(6) for s2 in range(6) for s3 in range(6) if s1+s2+s3==5]:
        s = candy_dist
        
        # 조건 (나): 각 학생이 받는 (초콜릿 + 사탕) >= 2
        if all(c[i] + s[i] >= 2 for i in range(3)):
            count += 1

if count == 117:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: {count}')