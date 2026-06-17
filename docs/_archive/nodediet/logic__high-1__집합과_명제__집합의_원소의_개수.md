---
sources: []
created: 2026-05-17
updated: 2026-05-17
concept_type: definition
domain: 논리
grade: 고1
prerequisites: [docs/concepts/logic/high-1/집합과_명제.md]
enables: []
mastery: unknown
---

# 집합의 원소의 개수

유한집합이 가지는 원소의 총 개수를 다루는 개념으로, 포함과 배제의 원리의 출발점입니다. 고1 집합과 명제 단원의 핵심입니다.

## 정의

유한집합 $A$에 속한 원소의 개수를 $n(A)$로 표기합니다. 주요 성질은 다음과 같습니다.
- $n(\varnothing) = 0$.
- $A \subseteq B$이면 $n(A) \le n(B)$.
- 합집합: $n(A \cup B) = n(A) + n(B) - n(A \cap B)$.
- 여집합: 전체집합 $U$에 대해 $n(A^c) = n(U) - n(A)$.

원소가 $n$개인 집합의 부분집합의 개수는 $2^n$, 진부분집합의 개수는 $2^n - 1$입니다.

## 예시

$U = \{1, 2, \ldots, 10\}$, $A = \{1, 2, 3, 4, 5\}$, $B = \{4, 5, 6, 7\}$. 그러면
$$n(A) = 5,\ n(B) = 4,\ n(A \cap B) = 2$$
이고 $n(A \cup B) = 5 + 4 - 2 = 7$, $n(A^c) = 10 - 5 = 5$입니다.

## 관련 개념

- [원소의 개수](docs/concepts/logic/high-1/집합과_명제/원소의_개수.md)
- [원소](docs/concepts/logic/high-1/집합과_명제/집합과_원소.md)
- [집합의 관계](docs/concepts/logic/high-1/집합과_명제/집합의_관계.md)
- [집합과 명제](docs/concepts/logic/high-1/집합과_명제.md)
