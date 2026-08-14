import sympy as sp

CANDIDATE = sp.Rational(65, 8)          # 외접원의 반지름 R (검증된 정답)

PARAMS = dict(
    AB=4,      # (가) 변 AB의 길이
    AC=15,     # (가) 변 AC의 길이
    area=24,   # (나) 삼각형 ABC의 넓이
)


def solve(prm):
    """조건(가) AB, AC / 조건(나) 넓이 → 각 A가 예각인 삼각형 ABC의 외접원 반지름 R."""
    AB = sp.Rational(prm['AB'])
    AC = sp.Rational(prm['AC'])
    area = sp.Rational(prm['area'])

    # 넓이 공식 S = (1/2)*AB*AC*sinA 로부터 sinA
    sinA = area / (sp.Rational(1, 2) * AB * AC)
    if not (0 < sinA <= 1):
        raise ValueError(f'sinA={sinA} 는 유효한 사인 값이 아님 (조건 불일치)')

    # 각 A가 예각이므로 cosA > 0
    cosA = sp.sqrt(1 - sinA**2)

    # 코사인 법칙으로 BC
    BC2 = AB**2 + AC**2 - 2 * AB * AC * cosA
    if BC2 <= 0:
        raise ValueError('BC^2 <= 0 (삼각형이 성립하지 않음)')
    BC = sp.sqrt(BC2)

    # 사인 법칙으로 외접원의 반지름 R = BC / (2 sinA)
    R = sp.simplify(BC / (2 * sinA))
    return R


def statement(prm):
    return (
        f"각 A가 예각인 삼각형 ABC가 다음 조건을 만족시킬 때, "
        f"삼각형 ABC의 외접원의 반지름의 길이는?\n"
        f"(가) AB={prm['AB']}, AC={prm['AC']}\n"
        f"(나) 삼각형 ABC의 넓이는 {prm['area']}이다."
    )


print('VERIFY_PASS' if sp.simplify(solve(PARAMS) - CANDIDATE) == 0 else 'VERIFY_FAIL')
