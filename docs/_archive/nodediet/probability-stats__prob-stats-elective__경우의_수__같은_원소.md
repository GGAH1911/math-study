---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 확률통계
grade: 확률과통계
prerequisites: [docs/concepts/probability-stats/prob-stats-elective/경우의_수.md]
enables: []
mastery: unknown
---

# 같은 원소

## 정확한 진술

같은 원소(또는 동일 원소)는 **서로 구별될 수 없는 특성을 가진 원소들**을 말합니다. 즉, 어떤 두 원소를 위치나 순서에서 바꾸어도 그 결과가 달라지지 않으면, 이 두 원소는 같은 원소입니다.

예를 들어, 빨간 공 3개는 색깔과 모양이 완벽히 같으므로 모두 같은 원소이며, 숫자 1이 적힌 카드 2장도 마찬가지입니다.

## 직관 및 기하적 의미

경우의 수를 셀 때, **같은 원소가 있으면 경우의 수가 줄어듭니다.** 

구체적으로, 서로 다른 $n$개 원소를 나열하는 경우의 수는 $n!$이지만, 그 중 $k_1$개가 같은 원소이고 $k_2$개가 또 다른 같은 원소이면:

$$\frac{n!}{k_1! \cdot k_2! \cdot \cdots}$$

왜냐하면 같은 것끼리 바꾸는 모든 경우를 중복으로 센 것을 제거해야 하기 때문입니다. 예를 들어, 빨간 공과 파란 공의 순서는 중요하지만, "빨간 공 1번을 빨간 공 2번과 바꾸는 것"은 눈에 띄지 않으므로 하나로 취급합니다.

## 한 줄 예

빨간 공 2개, 파란 공 3개를 일렬로 나열하는 경우의 수는 $\displaystyle\frac{5!}{2! \cdot 3!} = 10$이며, 여기서 같은 색 공들이 같은 원소입니다. (검산: `from math import factorial; factorial(5)//(factorial(2)*factorial(3))` → 10)
