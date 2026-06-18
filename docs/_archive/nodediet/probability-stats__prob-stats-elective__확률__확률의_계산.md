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

# 확률의 계산

## 정확한 진술

두 사건 $A$, $B$에 대해 다음 세 가지 기본 법칙이 성립합니다.

**합사건의 확률 (덧셈 법칙)**
$$P(A \cup B) = P(A) + P(B) - P(A \cap B)$$
특히 $A$와 $B$가 배반사건이면 $P(A \cup B) = P(A) + P(B)$입니다.

**곱사건의 확률 (곱셈 법칙)**
$$P(A \cap B) = P(A) \cdot P(B|A)$$
$A$와 $B$가 독립이면 $P(A \cap B) = P(A) \cdot P(B)$입니다.

**여사건의 확률**
$$P(A^c) = 1 - P(A)$$

## 직관/기하적 의미

합의 법칙을 벤 다이어그램으로 생각하면, $P(A)$와 $P(B)$를 단순히 더하면 교집합 부분이 두 번 계산됩니다. 따라서 중복을 제거하기 위해 $P(A \cap B)$를 한 번 빼는 것입니다. 곱의 법칙은 "먼저 $A$가 일어나고, 그 조건에서 $B$가 일어날 확률"처럼 순차적으로 일어나는 상황을 계산합니다. 여사건은 "전체 확률의 합은 1이므로, 어떤 사건이 일어나지 않을 확률은 전체에서 일어날 확률을 빼면 된다"는 보수 개념입니다.

## 한 줄 예

주머니에 빨간 공 3개, 파란 공 5개, 노란 공 2개가 있을 때, 빨간 공 또는 파란 공을 뽑을 확률은 배반사건이므로 $P = \dfrac{3}{10} + \dfrac{5}{10} = \dfrac{4}{5}$입니다. (검산: `from fractions import Fraction; Fraction(3,10) + Fraction(5,10)`)
