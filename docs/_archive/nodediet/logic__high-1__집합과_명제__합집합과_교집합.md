---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 논리
grade: 고1
prerequisites: [docs/concepts/logic/high-1/집합과_명제.md]
enables: []
mastery: unknown
---

# 합집합과 교집합

## 정확한 진술

두 집합 $A$, $B$에 대해:
- **합집합** $A \cup B$는 $A$에 속하거나 $B$에 속하는 모든 원소로 이루어진 집합입니다.
$$A \cup B = \{x \mid x \in A \text{ 또는 } x \in B\}$$
- **교집합** $A \cap B$는 $A$에도 속하고 $B$에도 속하는 모든 원소로 이루어진 집합입니다.
$$A \cap B = \{x \mid x \in A \text{ 그리고 } x \in B\}$$

여기서 "또는"은 '배타적' 또는가 아닙니다. $A$와 $B$ 모두에 속하는 원소도 합집합에 포함됩니다.

## 직관과 기하적 의미

벤 다이어그램으로 시각화하면 명확합니다. 합집합 $A \cup B$는 두 원을 칠한 **전체 영역**이고, 교집합 $A \cap B$는 두 원이 **겹치는 부분**입니다. 

합집합은 "적어도 하나에는 속하는" 원소들이므로 일반적으로 크기가 더 큽니다. 교집합은 "둘 다 만족하는" 원소들이므로 공통성이 있어야 하며, 공통 원소가 없으면 **공집합** $\emptyset$입니다. 예를 들어 $A = \{1, 2\}$, $B = \{3, 4\}$이면 $A \cap B = \emptyset$입니다.

## 한 줄 예

$A = \{1, 2, 3\}$, $B = \{2, 3, 4\}$일 때, $A \cup B = \{1, 2, 3, 4\}$ (합집합)이고 $A \cap B = \{2, 3\}$ (교집합)입니다.

```python
# 검산: A = {1, 2, 3}, B = {2, 3, 4}
A = {1, 2, 3}
B = {2, 3, 4}
print(A | B)  # {1, 2, 3, 4}
print(A & B)  # {2, 3}
```
