# 3x3 격자, 9색 전단사, 빨강·파랑이 꼭짓점 공유 안 함. 회전(C4) 동일. 경우의수=k×7!. k?
CANDIDATE = 8
cells = [(i, j) for i in range(3) for j in range(3)]
def shares_vertex(p, q):                       # 꼭짓점 공유 ⟺ 체비쇼프 거리 1
    return max(abs(p[0]-q[0]), abs(p[1]-q[1])) == 1
ordered = sum(1 for p in cells for q in cells if p != q and not shares_vertex(p, q))  # 32
k = ordered // 4                               # Burnside C4 (9색 distinct → 비자명회전 고정 0)
print('VERIFY_PASS' if k == CANDIDATE else 'VERIFY_FAIL')
