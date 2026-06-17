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

# 조건의 집합 표현

변수에 관한 조건을 그 조건이 참이 되도록 하는 원소들의 집합(진리집합)으로 옮겨 다루는 관점입니다. 고1 집합과 명제 단원에서 명제와 집합을 연결하는 핵심 도구입니다.

## 정의

전체집합 $U$ 위의 조건 $p(x)$에 대하여 $p(x)$가 참이 되도록 하는 모든 $x$의 집합을 $p$의 **진리집합**이라 하고 $P = \{x \in U \mid p(x)\}$로 씁니다.

조건명제·논리연산은 진리집합으로 다음과 같이 옮겨집니다.
- $\sim p$의 진리집합: $P^c$ (여집합).
- $p \text{ 또는 } q$의 진리집합: $P \cup Q$.
- $p \text{ 그리고 } q$의 진리집합: $P \cap Q$.
- $p \to q$가 참 $\iff P \subseteq Q$.

## 예시

전체집합을 실수 $\mathbb{R}$로 두고 조건 $p(x): x^2 < 4$, $q(x): -2 < x < 3$의 진리집합을 봅니다.
- $P = \{x \mid -2 < x < 2\}$,
- $Q = \{x \mid -2 < x < 3\}$.

$P \subseteq Q$이므로 명제 $p \to q$, 즉 "$x^2 < 4$이면 $-2 < x < 3$이다"는 참입니다. 반대로 $q \to p$의 진위는 $Q \subseteq P$여야 하는데 $2.5 \in Q \setminus P$이므로 거짓입니다.

## 관련 개념

- [조건명제](docs/concepts/logic/high-1/집합과_명제/조건명제.md)
- [집합의 관계](docs/concepts/logic/high-1/집합과_명제/집합의_관계.md)
- [집합과 명제](docs/concepts/logic/high-1/집합과_명제.md)
