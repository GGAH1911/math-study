# 그래프에서 직접 읽은 극한값을 검증
# x→-1⁻: x<-1 구간 선분이 (-1,2) 채워진 점으로 접근 → 극한 = 2
# x→2⁺ : x>2 구간이 (2,3) 빈 원에서 출발          → 극한 = 3

lim_neg1_left = 2   # lim_{x->-1^-} f(x)
lim_2_right   = 3   # lim_{x->2^+}  f(x)

total = lim_neg1_left + lim_2_right

if total == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
