import math

a = 2 * math.sqrt(2)
k = 2
t = 4

# A 좌표
p = a ** (k / 3)
y_A = k / 3

# B, C 좌표
log_a_t = math.log(t) / math.log(a)
y_B = log_a_t
y_C = -2 * log_a_t + k

# 조건 1: 직선 AB가 원점 통과
slope_OA = y_A / p
y_B_via_line = slope_OA * t
cond1 = abs(y_B_via_line - y_B) < 1e-9

# 조건 2: 삼각형 ACB 넓이 = 2
base_BC = y_B - y_C
height_ACB = t - p
area_ACB = 0.5 * base_BC * height_ACB
cond2 = abs(area_ACB - 2) < 1e-9

# 조건 3: 삼각형 OCA 넓이 = 2
area_OCA = 0.5 * abs(0*(y_C - y_A) + t*(y_A - 0) + p*(0 - y_C))
cond3 = abs(area_OCA - 2) < 1e-9

# 조건 4: a > 1, k > 0, t > p (t는 A의 x좌표보다 큼)
cond4 = a > 1 and k > 0 and t > p

# a*k*t 값 확인
product = a * k * t
cond5 = abs(product - 16 * math.sqrt(2)) < 1e-9

if cond1 and cond2 and cond3 and cond4 and cond5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', cond1, cond2, cond3, cond4, cond5)
