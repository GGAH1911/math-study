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

# 수열의 합과 일반항

## 정확한 진술
수열 $\{a_n\}$의 처음 $n$항까지의 합을 부분합(partial sum)이라 하고 $S_n$으로 나타낸다:
$$S_n = a_1 + a_2 + \cdots + a_n$$

수열의 일반항 $a_n$과 부분합 $S_n$ 사이에는 다음과 같은 관계가 성립한다:
- $n \geq 2$일 때: $a_n = S_n - S_{n-1}$
- $n = 1$일 때: $a_1 = S_1$

## 직관과 의미
$S_n$을 '누적 합계'로 생각하면, $a_n$은 $n$번째 항이 전체 합에 얼마나 추가되는지를 나타낸다. 즉, $S_n$에서 한 단계 이전의 합 $S_{n-1}$을 빼면 정확히 $n$번째 항만 남는다. 

이 관계의 중요한 점은 **부분합이 주어지면 수열을 완전히 복원할 수 있다**는 것이다. 역으로 수열이 주어지면 부분합을 구할 수 있고, 부분합이 주어지면 수열을 되찾을 수 있다는 뜻이다.

## 한 줄 예
수열 $1, 2, 3, 4, \ldots$에서 $S_3 = 6$, $S_2 = 3$이므로, $a_3 = S_3 - S_2 = 6 - 3 = 3$이다. 또는 부분합이 $S_n = \frac{n(n+1)}{2}$로 주어졌을 때, $n \geq 2$이면 $a_n = \frac{n(n+1)}{2} - \frac{(n-1)n}{2} = n$이고, $a_1 = S_1 = 1$이므로 일반항은 $a_n = n$이다.
