import sympy as sp

a = 2
x_pt, y_pt = 2*a, sp.sqrt(3)

# 점이 쌍곡선 위에 있는지 확인
hyperbola_check = x_pt**2 / a**2 - y_pt**2 - 1
print(f"쌍곡선 검증: {hyperbola_check} = {sp.simplify(hyperbola_check)}")

# 접선의 기울기
slope_tangent = x_pt / (a**2 * y_pt)
slope_tangent_simplified = sp.simplify(slope_tangent)
print(f"접선 기울기: {slope_tangent_simplified}")

# 주어진 직선의 기울기
slope_line = -sp.sqrt(3)
print(f"직선 기울기: {slope_line}")

# 수직 조건 검증
product = slope_tangent_simplified * slope_line
product_simplified = sp.simplify(product)
print(f"기울기 곱: {product_simplified}")

if product_simplified == -1 and hyperbola_check == 0:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")