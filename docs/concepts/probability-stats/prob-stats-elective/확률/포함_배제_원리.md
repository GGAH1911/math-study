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

# 포함 배제 원리

## 정확한 진술

포함배제 원리는 여러 사건의 합집합의 확률을 구할 때 사용합니다. 두 사건 $A$, $B$에 대해:

$$P(A \cup B) = P(A) + P(B) - P(A \cap B)$$

세 사건 $A$, $B$, $C$에 대해:

$$P(A \cup B \cup C) = P(A) + P(B) + P(C) - P(A \cap B) - P(B \cap C) - P(C \cap A) + P(A \cap B \cap C)$$

일반적으로 $n$개 사건에서는 **1개씩 더하고, 2개씩 교집합을 빼고, 3개씩 교집합을 더하는** 식으로 부호가 번갈아 나타납니다.

## 직관과 기하적 의미

단순히 $P(A) + P(B)$로 계산하면, 두 사건이 겹치는 부분 $P(A \cap B)$를 두 번 센 오류가 발생합니다. 따라서 한 번 빼야 합니다.

벤다이어그램으로 생각하면: 두 원이 겹칠 때, 합집합 영역의 넓이는 "두 원의 넓이 합 − 겹치는 부분"입니다. 확률도 동일한 원리로, 중복된 부분을 정확히 보정해야 전체 사건의 확률을 올바르게 계산할 수 있습니다.

## 한 줄 예

주사위를 던질 때, "3의 배수 또는 짝수가 나올 확률"을 구하면:

- $A$ = {3, 6} (3의 배수), $P(A) = \frac{2}{6}$
- $B$ = {2, 4, 6} (짝수), $P(B) = \frac{3}{6}$
- $A \cap B$ = {6}, $P(A \cap B) = \frac{1}{6}$

따라서 $P(A \cup B) = \frac{2}{6} + \frac{3}{6} - \frac{1}{6} = \frac{4}{6} = \frac{2}{3}$

실제로 조건을 만족하는 경우는 {2, 3, 4, 6}이므로 답이 맞습니다. (sympy: `from sympy import *; A = {3, 6}; B = {2, 4, 6}; len(A | B) / 6`)
