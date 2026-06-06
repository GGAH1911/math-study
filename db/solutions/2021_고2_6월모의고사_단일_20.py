import math

def f(n):
    t = math.log2(n)
    return abs(5 - t) / (1 + t)

# ㄱ: f(2)==2
assert abs(f(2) - 2) < 1e-12, 'ㄱ FAIL'

# ㄴ: f(n)>=1을 만족하는 자연수 n의 개수 == 4
count_nL = sum(1 for n in range(1, 10000) if f(n) >= 1)
assert count_nL == 4, f'ㄴ FAIL: count={count_nL}'

# ㄷ: |f(n)-1| >= 2/3 만족하는 자연수 n의 개수
count_nD = sum(1 for n in range(1, 10000) if abs(f(n) - 1) >= 2/3)
# 이론값 247; 문항은 245라고 주장 → 거짓이어야 함
if count_nD == 245:
    print('VERIFY_FAIL')  # ㄷ이 참이면 안 됨
elif count_nD == 247:
    # ㄷ은 거짓, ㄱ·ㄴ 참 → 답 ③
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: unexpected count {count_nD}')
