"""
2022 고3 10월모의고사 확률과통계 30번
조건부확률 + 베이즈 정리: 주머니 공 이동 문제

문제: A(흰3검1), B(흰3검1)에서
  [실행1] 동전: 앞(1/2)→A에서2개B로 / 뒷(1/2)→A에서3개B로
  [실행2] B에서5개를 A로 이동

  [실행2 후 B에 흰공 없음] 조건 하에서
  [실행1에서 흰공 2개를 B에 넣었을 확률]을 구하는 조건부확률 문제

답: 5/12 → p=12, q=5 (서로소) → p+q=17
"""

from fractions import Fraction
from math import comb

def solve():
    # 초기 상태
    # A: 흰 3, 검 1 (총 4개)
    # B: 흰 3, 검 1 (총 4개)

    cases = []

    # ==================== 케이스 1: 동전 앞면 (1/2) ====================
    # A에서 2개를 B로 이동
    prob_heads = Fraction(1, 2)

    # 경우 1-1: 흰2검0을 B로 이동
    prob_1_1_heads = Fraction(comb(3, 2) * comb(1, 0), comb(4, 2))  # 3/6 = 1/2
    # B의 상태: 흰 3+2=5, 검 1+0=1 (총 6)
    # [실행2] B에서 5개 꺼내면 1개 남음
    # 남은 1개가 모두 검은공(=흰공 0개)일 확률: P(검 1개 남음) = C(1,1)×C(5,0)/C(6,5) = 1/6
    prob_white2_after_exec2_case1_1 = Fraction(1, 6)
    cases.append({
        'name': '[앞] 흰2검0',
        'prob_coin': prob_heads,
        'prob_white_count': prob_1_1_heads,
        'white_count': 2,
        'prob_no_white_after': prob_white2_after_exec2_case1_1,
        'b_white_before': 5,
        'b_black_before': 1,
        'b_total_before': 6
    })

    # 경우 1-2: 흰1검1을 B로 이동
    prob_1_2_heads = Fraction(comb(3, 1) * comb(1, 1), comb(4, 2))  # 3/6 = 1/2
    # B의 상태: 흰 3+1=4, 검 1+1=2 (총 6)
    # [실행2] B에서 5개 꺼내면 1개 남음
    # 남은 1개가 모두 검은공(=흰공 0개)일 확률: C(2,1)×C(4,0)/C(6,5) = 2/6 = 1/3
    prob_white1_after_exec2_case1_2 = Fraction(2, 6)
    cases.append({
        'name': '[앞] 흰1검1',
        'prob_coin': prob_heads,
        'prob_white_count': prob_1_2_heads,
        'white_count': 1,
        'prob_no_white_after': prob_white1_after_exec2_case1_2,
        'b_white_before': 4,
        'b_black_before': 2,
        'b_total_before': 6
    })

    # ==================== 케이스 2: 동전 뒷면 (1/2) ====================
    # A에서 3개를 B로 이동
    prob_tails = Fraction(1, 2)

    # 경우 2-1: 흰3검0을 B로 이동
    prob_2_1_tails = Fraction(comb(3, 3) * comb(1, 0), comb(4, 3))  # 1/4
    # B의 상태: 흰 3+3=6, 검 1+0=1 (총 7)
    # [실행2] B에서 5개 꺼내면 2개 남음
    # 남은 2개가 모두 검은공(=흰공 0개)일 확률: 검이 1개뿐이므로 불가능 = 0
    prob_white3_after_exec2_case2_1 = Fraction(0, 1)
    cases.append({
        'name': '[뒷] 흰3검0',
        'prob_coin': prob_tails,
        'prob_white_count': prob_2_1_tails,
        'white_count': 3,
        'prob_no_white_after': prob_white3_after_exec2_case2_1,
        'b_white_before': 6,
        'b_black_before': 1,
        'b_total_before': 7
    })

    # 경우 2-2: 흰2검1을 B로 이동
    prob_2_2_tails = Fraction(comb(3, 2) * comb(1, 1), comb(4, 3))  # 3/4
    # B의 상태: 흰 3+2=5, 검 1+1=2 (총 7)
    # [실행2] B에서 5개 꺼내면 2개 남음
    # 남은 2개가 모두 검은공(=흰공 0개)일 확률: C(2,2)×C(5,0)/C(7,2) = 1/21
    prob_white2_after_exec2_case2_2 = Fraction(comb(2, 2) * comb(5, 0), comb(7, 2))
    cases.append({
        'name': '[뒷] 흰2검1',
        'prob_coin': prob_tails,
        'prob_white_count': prob_2_2_tails,
        'white_count': 2,
        'prob_no_white_after': prob_white2_after_exec2_case2_2,
        'b_white_before': 5,
        'b_black_before': 2,
        'b_total_before': 7
    })

    # ==================== 조건부확률 계산 ====================
    # 사건 E: [실행2] 후 B에 흰공 없음
    # 사건 F: [실행1]에서 흰공 2개를 B에 넣음

    # P(E) = 전체 확률의 법칙
    # P(F ∩ E) = 흰공 2개를 넣었으면서 E인 경우들의 확률 합
    # P(F|E) = P(F ∩ E) / P(E)

    p_e = Fraction(0)  # P(E): B에 흰공이 없을 확률
    p_f_and_e = Fraction(0)  # P(F ∩ E): 흰공 2개이면서 B에 흰공이 없을 확률

    for case in cases:
        # 각 케이스의 확률: P(코인) × P(흰공개수|코인)
        prob_case = case['prob_coin'] * case['prob_white_count']

        # P(E|case) = [실행2] 후 B에 흰공 없을 확률
        prob_e_given_case = case['prob_no_white_after']

        # P(case ∩ E) = P(case) × P(E|case)
        prob_case_and_e = prob_case * prob_e_given_case

        p_e += prob_case_and_e

        # 흰공 2개인 경우만 집계
        if case['white_count'] == 2:
            p_f_and_e += prob_case_and_e

        print(f"{case['name']:12} | P(case)={prob_case:>6} | P(E|case)={prob_e_given_case:>6} | "
              f"P(case∩E)={prob_case_and_e:>8}")

    print(f"\nP(E) = {p_e}")
    print(f"P(F ∩ E) = {p_f_and_e}")

    # P(F|E) = P(F ∩ E) / P(E)
    p_f_given_e = p_f_and_e / p_e

    print(f"\nP(F|E) = P(F ∩ E) / P(E) = {p_f_and_e} / {p_e} = {p_f_given_e}")

    # 기약분수 확인
    assert p_f_given_e.numerator > 0 and p_f_given_e.denominator > 0
    from math import gcd
    g = gcd(p_f_given_e.numerator, p_f_given_e.denominator)
    assert g == 1, f"Not in lowest terms: {p_f_given_e}"

    q = p_f_given_e.numerator  # 분자
    p = p_f_given_e.denominator  # 분모

    print(f"\nq/p = {q}/{p} (분자/분모)")
    print(f"p + q = {p} + {q} = {p + q}")

    return p + q

if __name__ == '__main__':
    answer = solve()
    print(f"\n{'='*50}")
    print(f"최종 답: {answer}")
    print(f"{'='*50}")
