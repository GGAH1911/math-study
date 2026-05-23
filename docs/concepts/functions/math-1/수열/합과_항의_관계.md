---
sources: []
created: 2026-05-17
updated: 2026-05-17
concept_type: definition
domain: 함수
grade: 수학1
prerequisites: [docs/concepts/functions/math-1/수열.md]
enables: []
mastery: unknown
---

# 합과 항의 관계

수열의 부분합 $S_n$과 일반항 $a_n$ 사이의 변환 공식입니다. 수학1 수열 단원에서 $S_n$이 주어졌을 때 일반항을 구하는 표준 도구입니다.

## 정의

수열 $\{a_n\}$의 첫째항부터 제 $n$항까지의 합을 $S_n = a_1 + a_2 + \cdots + a_n$이라 하면,
$$a_n = \begin{cases} S_1, & n = 1, \\ S_n - S_{n-1}, & n \ge 2. \end{cases}$$
$n = 1$과 $n \ge 2$의 경우가 자동으로 같은 식으로 표현되는지(=등비 또는 등차로 일관되는지)는 별도로 확인해야 합니다.

## 예시

$S_n = n^2 + 2n$일 때 일반항 $a_n$을 구해 봅니다.
- $n \ge 2$일 때: $a_n = S_n - S_{n-1} = (n^2 + 2n) - ((n-1)^2 + 2(n-1)) = (n^2 + 2n) - (n^2 - 1) = 2n + 1.$
- $n = 1$일 때: $a_1 = S_1 = 1 + 2 = 3$이고, 위 식 $2n+1$에 $n=1$을 넣으면 $3$이므로 일치.

따라서 모든 자연수 $n$에 대해 $a_n = 2n + 1$입니다.

## 관련 개념

- [수열](docs/concepts/functions/math-1/수열.md)
