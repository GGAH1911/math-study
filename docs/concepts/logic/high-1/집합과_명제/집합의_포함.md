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

# 집합의 포함

## 정확한 진술

집합 $A$가 집합 $B$에 **포함된다**는 것은 $A$의 모든 원소가 $B$에도 속한다는 의미입니다. 이를 $A \subseteq B$로 나타내고, "$A$는 $B$에 포함된다" 또는 "$A$는 $B$의 부분집합이다"라고 읽습니다.

기호로 정확히 쓰면:
$$A \subseteq B \iff \text{모든 } x \in A \text{에 대해 } x \in B$$

**중요한 사실:** $A = B$인 경우도 포함합니다. 즉, 집합은 자기 자신에 포함되며, 공집합 $\emptyset$은 모든 집합에 포함됩니다.

진정한 부분집합(진부분집합)을 나타내려면 $A \subsetneq B$ 또는 $A \subset B$를 사용하며, 이는 $A \subseteq B$이면서 $A \neq B$를 의미합니다.

## 직관/기하적 의미

벤 다이어그램으로 생각하면 $A \subseteq B$는 집합 $A$가 집합 $B$ 내부에 완전히 들어가 있는 상황입니다. $A$의 어떤 원소도 $B$ 밖으로 나와 있지 않아야 합니다.

포함 관계는 수의 대소관계와 유사합니다. $3 \leq 5$처럼 $A \subseteq B$도 기본적인 순서 관계를 나타내므로, 집합들 사이의 '크기' 비교(원소의 개수가 아닌 포함 정도)를 가능하게 합니다.

이 개념을 이용해 집합의 같음도 정의할 수 있습니다. $A = B$ ⟺ $A \subseteq B$ 그리고 $B \subseteq A$. 즉, 두 집합이 같으려면 서로를 포함해야 합니다.

## 한 줄 예

$A = \{1, 3\}$, $B = \{1, 2, 3, 4\}$일 때, $A$의 모든 원소($1, 3$)가 $B$에 속하므로 $A \subseteq B$입니다. 반대로 $2 \in B$이지만 $2 \notin A$이므로 $B \not\subseteq A$입니다.
