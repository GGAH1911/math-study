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

# 확률의 덧셈 공식

## 정확한 진술

임의의 두 사건 $A$와 $B$에 대하여, **확률의 덧셈 공식**은 다음과 같습니다.

$$P(A \cup B) = P(A) + P(B) - P(A \cap B)$$

특히 $A$와 $B$가 **배반사건**(즉, $A \cap B = \emptyset$)이면:

$$P(A \cup B) = P(A) + P(B)$$

## 직관과 기하적 의미

$A$ 또는 $B$가 일어날 확률을 구할 때, 단순히 $P(A) + P(B)$로 더하면 $A$와 $B$가 동시에 일어나는 부분 $P(A \cap B)$이 **중복으로 계산**됩니다. 따라서 한 번 빼 주어야 합니다.

벤 다이어그램으로 보면, 두 원 $A$와 $B$의 합집합 영역의 넓이는 각 원의 넓이를 더한 후 겹치는 부분을 한 번 빼는 것과 같습니다. 이는 중복을 제거하는 **포함-배제 원리**(inclusion-exclusion principle)의 기초입니다.

## 한 줄 예

주사위를 한 번 던질 때, 짝수($A$: {2, 4, 6})가 나올 확률은 $\frac{1}{2}$, 3의 배수($B$: {3, 6})가 나올 확률은 $\frac{1}{3}$입니다. 짝수 또는 3의 배수가 나올 확률은:

$$P(A \cup B) = \frac{1}{2} + \frac{1}{3} - P(A \cap B) = \frac{1}{2} + \frac{1}{3} - \frac{1}{6} = \frac{2}{3}$$

실제로 {2, 3, 4, 6}이 해당하므로 $\frac{4}{6} = \frac{2}{3}$입니다. (`sympy.Rational(1,2) + sympy.Rational(1,3) - sympy.Rational(1,6)` = $\frac{2}{3}$)
