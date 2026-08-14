import sympy as sp

# [원문제]
# 두 곡선 y = 2*sqrt(2x)+1, y = sqrt(2x) 와 y축 및 직선 x=2로 둘러싸인 도형을
# 밑면으로 하는 입체도형을 x축에 수직인 평면으로 자르면 단면이 모두 정사각형.
# 이 입체도형의 부피를 V라 할 때 30V의 값을 구하여라.
#
# [수학 구조]
#   윗곡선: y = p*sqrt(k*x) + q   (원문제 p=2)
#   아랫곡선: y = sqrt(k*x)       (원문제 계수 1)
#   y축(x=0) 과 x=L 사이의 영역이 밑면.
#   단면 정사각형의 한 변 h(x) = (윗곡선 - 아랫곡선) = (p-1)*sqrt(k*x) + q
#   단면적 A(x) = h(x)^2
#   부피 V = ∫_0^L A(x) dx
#   최종 답 = M * V
#
# 답을 바꾸는 파라미터: p, q, k, L, M (전부 답에 영향을 준다. 아래에서 개별 확인함)

CANDIDATE = 340  # ★ 원문제 정답, 절대 변경 금지

PARAMS = dict(
    p=2,   # 윗곡선 y = p*sqrt(k*x)+q 의 계수 (원문제: 2)
    q=1,   # 윗곡선의 상수항 (원문제: 1)
    k=2,   # 곡선 내부 x 계수, y = sqrt(k*x) 형태 (원문제: 2)
    L=2,   # 밑면의 x 범위 [0, L] (원문제: 2)
    M=30,  # 최종적으로 곱하는 배수, "MV의 값" (원문제: 30)
)


def solve(prm):
    p, q, k, L, M = [sp.nsimplify(prm[key]) for key in ("p", "q", "k", "L", "M")]

    if not (p > 1 and q > 0 and k > 0 and L > 0 and M > 0):
        # p<=1 이면 두 곡선이 뒤바뀌거나 겹쳐 "둘러싸인 도형"이 성립하지 않음
        raise ValueError("유효하지 않은 파라미터 조합: 도형이 성립하지 않음")

    x = sp.symbols("x", positive=True)

    top = p * sp.sqrt(k * x) + q      # 윗곡선
    bottom = sp.sqrt(k * x)           # 아랫곡선
    h = sp.simplify(top - bottom)     # 단면 정사각형의 한 변

    A = h ** 2                        # 단면적 (정사각형)
    V = sp.integrate(A, (x, 0, L))    # 입체도형의 부피

    answer = sp.simplify(M * V)

    # 정수라면 int로, 아니면 sympy 값 그대로 반환 (변형 파라미터는 정수가 아닐 수도 있음)
    if answer.is_Rational and answer.q == 1:
        return int(answer)
    if answer.is_Integer:
        return int(answer)
    return answer


def statement(prm):
    p, q, k, L, M = (prm["p"], prm["q"], prm["k"], prm["L"], prm["M"])
    return (
        f"그림과 같이 두 곡선 y={p}\\sqrt{{{k}x}}+{q}, y=\\sqrt{{{k}x}} 와 y축 및 "
        f"직선 x={L}로 둘러싸인 도형을 밑면으로 하는 입체도형이 있다. 이 입체도형을 "
        f"x축에 수직인 평면으로 자른 단면이 모두 정사각형일 때, 이 입체도형의 부피를 "
        f"V라 하자. {M}V의 값을 구하시오."
    )


if __name__ == "__main__":
    result = solve(PARAMS)
    print(statement(PARAMS))
    print("solve(PARAMS) =", result)
    print('VERIFY_PASS' if result == CANDIDATE else 'VERIFY_FAIL')

    # 파라미터별 변경 확인 (답이 실제로 달라지는지)
    for key, delta in [("p", 1), ("q", 1), ("k", 1), ("L", 1), ("M", 5)]:
        prm2 = dict(PARAMS)
        prm2[key] = prm2[key] + delta
        try:
            r2 = solve(prm2)
        except Exception as e:
            r2 = f"오류: {e}"
        print(f"  {key} 변경 -> {r2} (원래 {result})")
