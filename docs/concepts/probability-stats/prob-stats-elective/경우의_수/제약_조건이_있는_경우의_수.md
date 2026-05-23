---
sources: []
created: 2026-05-17
updated: 2026-05-17
concept_type: definition
domain: 확률통계
grade: 확률과통계
prerequisites: [docs/concepts/probability-stats/prob-stats-elective/경우의_수.md]
enables: []
mastery: unknown
---

# 제약 조건이 있는 경우의 수

특정 원소나 자리에 부가 조건이 붙은 상태에서 경우의 수를 세는 문제 유형입니다. 확률과 통계 경우의 수 단원의 빈출 응용입니다.

## 정의

제약 조건이 있는 문제는 보통 다음 두 전략 중 하나로 환원됩니다.
- **이웃 묶음:** 이웃해야 하는 원소들을 한 덩어리로 묶어 배열한 후, 묶음 내부의 배열을 곱함.
- **여사건:** "어떤 조건을 만족하지 않는" 경우의 수를 전체에서 빼서 구함. 예: $n($조건 만족$) = n($전체$) - n($조건 위반$)$.

또한 특정 자리에 특정 원소가 와야 하는 경우는 그 자리를 고정한 뒤 남은 자리·원소로 부분 문제를 푼다.

## 예시

서로 다른 $5$명 $A, B, C, D, E$를 일렬로 세울 때 $A$와 $B$가 이웃하는 경우의 수를 구해 봅니다. $A, B$를 한 덩어리로 묶으면 $4$개를 일렬로 세우는 $4! = 24$가지가 있고, 묶음 내부의 두 가지 배열 $AB,\ BA$를 곱하여
$$24 \times 2 = 48.$$

또한 $5$명 중 적어도 한 명이 특정한 자리($1$번)를 차지하는 사람이 $A$인 경우의 수는 $A$를 $1$번에 고정한 후 남은 $4$명을 배열하는 $4! = 24$입니다.

## 관련 개념

- [경우의 수 기초](docs/concepts/probability-stats/prob-stats-elective/경우의_수/경우의_수_기초.md)
- [곱셈 원리](docs/concepts/probability-stats/prob-stats-elective/경우의_수/곱셈_원리.md)
- [경우의 수](docs/concepts/probability-stats/prob-stats-elective/경우의_수.md)
