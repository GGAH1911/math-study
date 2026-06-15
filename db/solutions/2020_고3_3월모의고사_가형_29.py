# 삼각형 O(0,0),A(0,n+5),B(n+4,0) 내부의 단위정사각형(정수 꼭짓점) 개수 a_n. Σ_{n=1}^8 a_n?
CANDIDATE = 164
total = 0
for n in range(1, 9):
    A, B, C = n+5, n+4, (n+4)*(n+5)            # 빗변 (n+5)x+(n+4)y=(n+4)(n+5)
    for i in range(1, 30):
        for j in range(1, 30):
            if A*(i+1) + B*(j+1) < C:           # 최외곽 꼭짓점 (i+1,j+1) 내부 ⟹ 정사각형 내부
                total += 1
print('VERIFY_PASS' if total == CANDIDATE else 'VERIFY_FAIL')
