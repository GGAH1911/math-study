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

# 확률의 덧셈법칙

## 정확한 진술

두 사건 $A$와 $B$에 대하여 다음이 성립합니다.

$$P(A \cup B) = P(A) + P(B) - P(A \cap B)$$

**특수한 경우:** $A$와 $B$가 **상호배타적**(서로소, 즉 $A \cap B = \emptyset$)이면
$$P(A \cup B) = P(A) + P(B)$$

## 직관과 기하적 의미

'또는'으로 표현되는 합집합 $A \cup B$의 확률을 구할 때, 단순히 $P(A) + P(B)$하면 교집합 부분이 두 번 세어집니다. 벤다이어그램에서 보면 $A$와 $B$가 겹치는 부분을 빼야 전체 넓이를 올바르게 구할 수 있습니다. 이것이 $-P(A \cap B)$ 항이 필요한 이유입니다.

상호배타적 사건(동시에 일어날 수 없는 경우)이면 교집합이 공집합이므로 $P(A \cap B) = 0$이 되어 식이 단순해집니다. 예를 들어, 주사위를 한 번 던질 때 '3의 배수가 나올 확률'과 '2가 나올 확률'은 동시에 일어날 수 없으므로 상호배타적입니다.

## 한 줄 예

주사위 한 개를 던질 때, '3 이상이 나올 확률' 또는 '짝수가 나올 확률'을 구하면:
- $A$: 3 이상 → $P(A) = \frac{4}{6}$ (3, 4, 5, 6)
- $B$: 짝수 → $P(B) = \frac{3}{6}$ (2, 4, 6)
- $A \cap B$: 3 이상인 짝수 → $P(A \cap B) = \frac{2}{6}$ (4, 6)

$$P(A \cup B) = \frac{4}{6} + \frac{3}{6} - \frac{2}{6} = \frac{5}{6}$$

(`sympy.S(4,6) + sympy.S(3,6) - sympy.S(2,6)` 검산 가능)
