# 그래프: lim_{x→-1-}f + lim_{x→1+}f? 좌측 직선 y=x+2 (-2,0 통과)→(-1,1)개원; 우측 곡선→(1,2)개원. (보기⑤=3)
CANDIDATE = 3
mid = lambda x: x + 2           # 좌측 직선
L = mid(-1)                     # lim_{x→-1-} = 1
R = 2                           # lim_{x→1+} = 2 (우측 곡선 개원값)
print('VERIFY_PASS' if L + R == CANDIDATE else 'VERIFY_FAIL')
