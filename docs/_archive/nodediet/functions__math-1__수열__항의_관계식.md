---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 수학1
prerequisites: [docs/concepts/functions/math-1/수열.md]
enables: []
mastery: unknown
---

# 항의 관계식

## 정확한 진술

수열 $\{a_n\}$의 부분합을 $S_n = a_1 + a_2 + \cdots + a_n$이라 할 때, 일반항 $a_n$과 부분합 $S_n$ 사이에는 다음 관계식이 성립합니다:

$$a_n = \begin{cases} S_1 & (n=1) \\ S_n - S_{n-1} & (n \geq 2) \end{cases}$$

이를 **항의 관계식** 또는 **항과 부분합의 관계식**이라 부릅니다.

## 직관/기하적 의미

부분합 $S_n$은 처음 $n$개 항을 모두 더한 누적 합입니다. 따라서 $n$번째 항 $a_n$은 "전체 누적 합에서 한 단계 전 누적 합을 뺀 것"—즉, 그 단계에서 새로 추가된 값입니다. 적금에 비유하면 $S_n$은 $n$개월 후 통장 잔액이고, $a_n$은 $n$번째 달에 입금한 금액입니다. 그러므로 $a_n = S_n - S_{n-1}$은 자연스럽게 도출됩니다. $n=1$일 때는 이전 합이 존재하지 않으므로 $a_1 = S_1$입니다.

## 한 줄 예

$S_n = n^2 + 2n$이면 $a_1 = S_1 = 3$이고, $n \geq 2$일 때 $a_n = (n^2 + 2n) - ((n-1)^2 + 2(n-1)) = 2n + 1$입니다. 즉 일반항은 $a_n = \begin{cases}3 & (n=1) \\ 2n+1 & (n \geq 2)\end{cases}$입니다.
