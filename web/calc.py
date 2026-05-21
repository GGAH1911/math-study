from sympy import *

print("="*70)
print("타원 문제 SymPy 정확 계산")
print("="*70)

# 단계 1: 초점 c 값 계산
print()
print("[단계 1] 초점 c 값 계산")
print("-"*70)
a_sq = 16
b_sq = 12
c_sq = a_sq - b_sq
c = sqrt(c_sq)
print(f"a² = {a_sq}, b² = {b_sq}")
print(f"c² = a² - b² = {a_sq} - {b_sq} = {c_sq}")
print(f"c = √{c_sq} = {c}")
print(f"c (수치) = {float(c):.6f}")

# 단계 2: 점 P(2, 3)에서의 접선 방정식
print()
print("[단계 2] 점 P(2, 3)에서의 접선 ℓ 방정식")
print("-"*70)
x, y = symbols("x y", real=True)

print("타원 접선 공식: (x₀·x)/a² + (y₀·y)/b² = 1")
print("P(2, 3)에서: (2·x)/16 + (3·y)/12 = 1")
print("정리: x/8 + y/4 = 1")
print("또는: x + 2y = 8")

slope_l = -Rational(1, 2)
print(f"접선 기울기: {slope_l}")

# 단계 3: F를 지나고 ℓ과 평행한 직선
print()
print("[단계 3] F를 지나고 ℓ과 평행한 직선 방정식")
print("-"*70)
print(f"F({c}, 0)을 지나고 기울기 {slope_l}:")
print(f"y = {slope_l}(x - {c})")

# 단계 4: 평행선과 타원의 교점
print()
print("[단계 4] 평행선과 타원의 교점 → Q(제2사분면)")
print("-"*70)

ellipse_eq = x**2/16 + y**2/12 - 1
line_y = -Rational(1, 2)*(x - c)

ellipse_with_line = ellipse_eq.subs(y, line_y)
x_solutions = solve(ellipse_with_line, x)

print("x의 해:")
for i, sol in enumerate(x_solutions):
    print(f"  x_{i+1} = {sol}")

intersection_points = []
for x_sol in x_solutions:
    y_sol = simplify(line_y.subs(x, x_sol))
    intersection_points.append((x_sol, y_sol))
    x_num = float(x_sol.evalf())
    y_num = float(y_sol.evalf())
    print(f"  ({x_num:.4f}, {y_num:.4f})")

# 제2사분면 점 찾기
Q = None
for x_sol, y_sol in intersection_points:
    x_num = float(x_sol.evalf())
    y_num = float(y_sol.evalf())
    if x_num < 0 and y_num > 0:
        Q = (x_sol, y_sol)

Q_x, Q_y = Q
print()
print(f"✓ Q = ({Q_x}, {Q_y})")
print(f"  수치: ({float(Q_x.evalf()):.6f}, {float(Q_y.evalf()):.6f})")

# 단계 5: 직선 F'Q의 기울기
print()
print("[단계 5] 직선 F'Q의 기울기")
print("-"*70)
F_prime_x = -c
slope_F_Q = (Q_y - 0) / (Q_x - F_prime_x)
slope_F_Q = simplify(slope_F_Q)
print(f"F'({-c}, 0), Q({Q_x}, {Q_y})")
print(f"기울기 = {slope_F_Q}")

# 단계 6: F'Q와 ℓ의 교점 R
print()
print("[단계 6] F'Q와 ℓ의 교점 R")
print("-"*70)
line_l_eq = x + 2*y - 8
line_FQ_eq = y - slope_F_Q*(x + c)

intersection_R = solve([line_l_eq, line_FQ_eq], [x, y])
R_x = simplify(intersection_R[x])
R_y = simplify(intersection_R[y])

print(f"R = ({R_x}, {R_y})")
print(f"수치: ({float(R_x.evalf()):.6f}, {float(R_y.evalf()):.6f})")

# 단계 7: ℓ과 x축의 교점 S
print()
print("[단계 7] ℓ과 x축의 교점 S")
print("-"*70)
intersection_S = solve([line_l_eq, y], [x, y])
S_x = intersection_S[x]
S_y = 0

print(f"S = ({S_x}, {S_y})")

# 최종 정리
print()
print("="*70)
print("최종 결과 요약")
print("="*70)
print()
print(f"초점: c = {c}, F({c}, 0), F'({-c}, 0)")
print()
print("접선 ℓ: x + 2y = 8 (기울기: -1/2)")
print()
print(f"Q (제2사분면): ({Q_x}, {Q_y})")
print(f"  = ({float(Q_x.evalf()):.6f}, {float(Q_y.evalf()):.6f})")
print()
print(f"R (교점): ({R_x}, {R_y})")
print(f"  = ({float(R_x.evalf()):.6f}, {float(R_y.evalf()):.6f})")
print()
print(f"S (교점): ({S_x}, {S_y})")

print()
print("="*70)
