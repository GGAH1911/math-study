"""
2025 고1 3월모의고사 단일 27번
외심·내심 성질과 이등변삼각형: 각도 계산

조건:
- AC = BC인 예각삼각형 ABC
- 외심 O, ∠BAO = 28°
- BC 연장선상의 점 D로 ∠ADC = 40°
- 삼각형 ACD의 내심 I
- ∠OAI = x°

풀이:
1. AC = BC → ∠BAC = ∠ABC (이등변)
2. OA = OB (외접원 반지름) → ∠OBA = ∠OAB = 28° (이등변)
3. ∠AOB = 180° - 28° - 28° = 124°
4. 원주각 = 중심각/2 → ∠ACB = 124°/2 = 62°
5. ∠BAC = ∠ABC = (180° - 62°)/2 = 59°
6. ∠AOC = 2∠ABC = 118°
7. ∠OAC = (180° - 118°)/2 = 31°
8. D는 BC 연장선상 → ∠ACD = 180° - 62° = 118°
9. ∠CAD = 180° - 118° - 40° = 22°
10. 내심 I → AI는 ∠CAD의 이등분선 → ∠CAI = 11°
11. ∠OAI = ∠OAC + ∠CAI = 31° + 11° = 42°
"""

def solve():
    # 외심 각도 계산
    angle_BAO = 28  # 주어진 조건
    angle_OAB = 28  # OA = OB인 이등변삼각형
    angle_AOB = 180 - angle_OAB - angle_BAO

    # 원주각과 중심각 관계
    angle_ACB = angle_AOB / 2

    # 이등변삼각형 ABC
    angle_BAC = angle_ABC = (180 - angle_ACB) / 2

    # 외심의 다른 중심각
    angle_AOC = 2 * angle_ABC

    # 이등변삼각형 OAC
    angle_OAC = (180 - angle_AOC) / 2

    # D의 위치 (BC 연장선상, C 너머)
    angle_ACD = 180 - angle_ACB

    # 삼각형 ACD의 각도
    angle_CAD = 180 - angle_ACD - 40

    # 내심 I의 성질 (AI는 ∠CAD의 이등분선)
    angle_CAI = angle_CAD / 2

    # 최종 답
    x = angle_OAC + angle_CAI

    return int(x)

if __name__ == '__main__':
    print(f"답: {solve()}")
