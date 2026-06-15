# 2020 6월모평 나형 07 (그래프): lim_{x→-1+}f(x) + lim_{x→1-}f(x)?  (보기 ②=2)
# 그래프 판독: 중앙 선분은 (-1,0)→(1,2) 의 직선 y=x+1 (양 끝 개원).
# x→-1+ 와 x→1- 의 극한은 이 직선의 끝값.
CANDIDATE = 2
def mid(x):
    return x + 1                  # (-1,0),(1,2) 를 지나는 직선
L_left = mid(-1)                  # lim_{x→-1+} f(x) = 0
L_right = mid(1)                  # lim_{x→1-} f(x) = 2
print('VERIFY_PASS' if L_left + L_right == CANDIDATE else 'VERIFY_FAIL')
