import numpy as np

p = 6

# 포물선 y^2 = 4px, 점 A의 x좌표
a = 4 * p / 3
b_sq = 4 * p * a
b = np.sqrt(b_sq)  # 제1사분면 → 양수

# 1) A가 포물선 위에 있는지
cond1 = np.isclose(b**2, 4 * p * a)

# 2) 접선 기울기 × OA 기울기 = 3/2
tangent_slope = 2 * p / b
oa_slope = b / a
prod = tangent_slope * oa_slope
cond2 = np.isclose(prod, 3 / 2)

# 3) AF = a + p = 14 (포물선 초점 거리)
AF = a + p
cond3 = np.isclose(AF, 14)

if cond1 and cond2 and cond3:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: cond1={cond1}, cond2={cond2} (prod={prod}), cond3={cond3} (AF={AF})')
