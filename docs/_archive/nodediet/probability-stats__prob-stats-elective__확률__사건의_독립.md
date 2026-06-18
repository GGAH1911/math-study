---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 확률통계
grade: 확률과통계
prerequisites: [docs/concepts/probability-stats/prob-stats-elective/확률.md]
enables: []
mastery: unknown
---

# 사건의 독립

## 정확한 진술

두 사건 $A$, $B$에 대해 다음이 성립할 때, **사건 $A$와 $B$는 독립**이라 합니다:

$$P(A \cap B) = P(A) \cdot P(B)$$

더 일반적으로, 사건 $A$가 독립이려면 $P(B|A) = P(B)$와 $P(A|B) = P(A)$를 동시에 만족해야 합니다. 즉, 한 사건의 발생이 다른 사건의 확률을 변화시키지 않습니다.

## 직관과 의미

"독립"은 **두 사건이 서로 영향을 주지 않는다**는 뜻입니다. 예를 들어 주사위를 두 번 던질 때, 첫 번째 결과는 두 번째 결과에 영향을 주지 않습니다. 조건부 확률의 정의에서 $P(A \cap B) = P(B|A) \cdot P(A)$인데, 만약 $P(B|A) = P(B)$라면 "사건 $A$가 일어났다는 정보"가 사건 $B$의 확률을 바꾸지 않는다는 뜻입니다. 이것이 두 사건이 독립인 상황입니다.

반대로 **종속**인 경우는 한 사건이 다른 사건의 확률을 변화시킵니다. 예: 카드를 복원 없이 뽑는 경우.

## 한 줄 예

주사위 한 번 던지기에서 $A$ = "짝수", $B$ = "3의 배수"라 하면, $P(A) = \frac{1}{2}$, $P(B) = \frac{1}{3}$, $P(A \cap B) = \frac{1}{6}$이므로 $P(A \cap B) = P(A) \cdot P(B)$를 만족하여 독립입니다.

```python
# sympy로 검증: P(A∩B) = 1/6 = (1/2)(1/3)
from fractions import Fraction
P_A = Fraction(1, 2)  # 짝수: 2, 4, 6
P_B = Fraction(1, 3)  # 3의 배수: 3, 6
P_A_and_B = Fraction(1, 6)  # 6만 해당
print(P_A_and_B == P_A * P_B)  # True
```
