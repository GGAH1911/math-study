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

# 경우의수분할

## 정확한 진술

유한집합의 모든 원소를 공집합이 아닌 부분집합들로 나누되, 다음 조건을 만족하도록 하는 경우의 수입니다:
- 모든 부분집합이 서로 겹치지 않음 (서로소)
- 모든 부분집합을 합치면 원래 집합 전체가 됨

$n$개의 서로 다른 원소를 정확히 $k$개의 비어있지 않은 그룹으로 나누는 경우의 수를 **스털링 제2종수**(Stirling number of the second kind)라 하며, 기호로 $S(n, k)$ 또는 $\begin{Bmatrix}n\\k\end{Bmatrix}$로 나타냅니다.

## 직관: 배치와의 차이

분할은 조합 문제에서 **순서가 없는** 상황을 다룹니다. 예를 들어 학생 5명을 2개 팀으로 나누는 것은 분할입니다. {철수, 영희} vs {민준, 수진, 지은}과 {민준, 수진, 지은} vs {철수, 영희}는 같은 분할입니다. 반면 "A조와 B조"처럼 팀이 구별되면 배치(배열)가 되어 경우의 수가 달라집니다.

또한 분할은 각 그룹이 **비어있지 않아야** 합니다. "아무도 없는 팀"은 만들 수 없다는 뜻입니다.

## 한 줄 예와 검산

집합 $\{1, 2, 3\}$을 2개 그룹으로 나누는 모든 방법:
$$\{\{1\}, \{2,3\}\}, \quad \{\{2\}, \{1,3\}\}, \quad \{\{3\}, \{1,2\}\}$$

따라서 $S(3, 2) = 3$입니다. 이는 재귀 공식 $S(n, k) = k \cdot S(n-1, k) + S(n-1, k-1)$로도 검증 가능합니다.

```python
# sympy로 확인
from sympy.utilities.iterables import multiset_partitions
list(multiset_partitions([1,2,3], 2))  # 길이 3인 집합을 2부분 분할 → 3가지
```
