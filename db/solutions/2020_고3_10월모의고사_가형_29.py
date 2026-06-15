# a<b<c<=20, 세 변 a,b,c 삼각형 존재(a+b>c). 순서쌍 (a,b,c) 개수?
CANDIDATE = 525
count = sum(1 for c in range(1, 21) for b in range(1, c) for a in range(1, b) if a+b > c)
print('VERIFY_PASS' if count == CANDIDATE else 'VERIFY_FAIL')
