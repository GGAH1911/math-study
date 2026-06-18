---
unit: 집합과 명제
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 논리
grade: 고1
prerequisites: [docs/concepts/probability-stats/prob-stats-elective/경우의_수.md]
enables: []
mastery: unknown
---

# 집합의 교집합

## 정확한 진술

두 집합 $A$, $B$에 대해, $A$에도 속하고 동시에 $B$에도 속하는 모든 원소들로 이루어진 집합을 $A$와 $B$의 **교집합**(intersection)이라 하며, $A \cap B$로 표기합니다.

기호로 다음과 같이 정의합니다:
$$A \cap B = \{x \mid x \in A \text{ and } x \in B\}$$

구체적인 예: $A = \{1, 2, 3, 4\}$, $B = \{2, 4, 6, 8\}$일 때, $A \cap B = \{2, 4\}$입니다. (공통으로 포함된 원소만)

## 직관 및 기하적 의미

벤다이어그램(Venn diagram)으로 표현하면, 두 집합을 나타내는 두 원이 겹치는 부분이 바로 교집합입니다.

일상적 예시로 이해하면:
- A팀에 속한 선수: {김철수, 이영희, 박민준, 최지은}
- B팀에 속한 선수: {이영희, 박민준, 정재훈, 한수진}
- 둘 다 속한 선수: {이영희, 박민준} ← 이것이 교집합

교집합은 **조건을 동시에 만족해야 하는 경우**에 사용됩니다. 논리 연산자의 AND(그리고)와 같은 개념입니다. 두 조건을 모두 만족하는 원소만 찾는 것이 교집합입니다.

## 한 줄 예

$A = \{1, 2, 3, 5\}$, $B = \{2, 3, 4, 5, 6\}$일 때, $A \cap B = \{2, 3, 5\}$입니다. (`sympy.Set([1,2,3,5]) & sympy.Set([2,3,4,5,6])`)
