from sympy import sqrt, Rational, simplify

CANDIDATE = 2

# 선택지 정의 (문제에서 주어진 선택지)
choices = {
    1: Rational(26, 3),
    2: Rational(28, 3),
    3: 10,
    4: Rational(32, 3),
    5: Rational(34, 3),
}

# 함수 f(x) 정의 (검증된 풀이에서 도출된 형태)
def f(x):
    """정육각형 변을 따라 움직이는 점 P에 대한 삼각형 PFA의 넓이"""
    if 0 < x <= 2:
        return (sqrt(3) / 4) * x
    elif 2 < x <= 3:
        return sqrt(3) / 2
    elif 3 < x < 5:
        return (sqrt(3) * (5 - x)) / 4
    else:
        raise ValueError(f"x={x} is out of range (0, 5)")

# 원 문제 조건: f의 최댓값 (가) = p
p = sqrt(3) / 2

# 원 문제 조건: f(b) = 9/32를 만족하는 b (나) = q
# 경우 1 (0 < b ≤ 2): (√3/4)b = 9/32 → b = 3√3/8
b = 3 * sqrt(3) / 8
q = b

# 검증 1: f(b) = 9/32 확인
f_b = simplify(f(b))
target_fb = Rational(9, 32)
verify_f_b = simplify(f_b - target_fb) == 0

# 원 문제 조건: f(a) = (나) = q를 만족하는 모든 a
# 경우 1 (0 < a ≤ 2): (√3/4)a = 3√3/8 → a = 3/2
a1 = Rational(3, 2)
# 경우 3 (3 < a < 5): (√3(5-a))/4 = 3√3/8 → a = 7/2
a2 = Rational(7, 2)

# 검증 2, 3: f(a1) = q, f(a2) = q 확인
f_a1 = simplify(f(a1))
f_a2 = simplify(f(a2))
verify_f_a1 = simplify(f_a1 - q) == 0
verify_f_a2 = simplify(f_a2 - q) == 0

# 검증 4, 5: (f∘f)(a1) = 9/32, (f∘f)(a2) = 9/32 확인
f_of_f_a1 = simplify(f(simplify(f(a1))))
f_of_f_a2 = simplify(f(simplify(f(a2))))
verify_composition_a1 = simplify(f_of_f_a1 - Rational(9, 32)) == 0
verify_composition_a2 = simplify(f_of_f_a2 - Rational(9, 32)) == 0

# 원 문제 조건: 모든 a의 값의 곱 (다) = r
r = a1 * a2  # = 3/2 × 7/2 = 21/4

# 원 문제에서 요구: r/(p×q)의 값
result = simplify(r / (p * q))
expected = choices[CANDIDATE]

# 최종 검증
if (verify_f_b and verify_f_a1 and verify_f_a2 and 
    verify_composition_a1 and verify_composition_a2 and
    simplify(result - expected) == 0):
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")