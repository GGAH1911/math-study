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

# 수열의합

## 정확한 진술

수열 $\{a_n\}$의 **수열의합** $S_n$은 첫 $n$항까지의 모든 항을 더한 값입니다. 수식으로는 다음과 같이 정의합니다.

$$S_n = a_1 + a_2 + a_3 + \cdots + a_n = \sum_{k=1}^{n} a_k$$

여기서 $n$은 양의 정수이고, 특히 $S_1 = a_1$입니다. $S_n$을 "제 $n$항까지의 부분합(partial sum)"이라고도 부릅니다.

## 직관과 기하적 의미

수열의합은 수열의 누적된 효과를 나타냅니다. 예를 들어 매달 저축액이 수열을 이룬다면 $S_n$은 $n$개월 후의 총 저축액입니다. 일반적으로 변화하는 양들의 전체 누적량을 계산할 때 수열의합 개념이 필요합니다.

중요한 점은 수열의합 수열 $\{S_n\}$과 원래 수열 $\{a_n\}$이 서로 역의 관계를 가진다는 것입니다. 즉, $S_n$을 알면 원래 수열을 다음과 같이 복원할 수 있습니다:

$$a_n = \begin{cases} S_1 & \text{if } n=1 \\ S_n - S_{n-1} & \text{if } n \geq 2 \end{cases}$$

따라서 부분합으로 수열을 완전히 나타낼 수 있습니다.

## 한 줄 예

수열 $\{1, 2, 3, 4, 5\}$에 대해 $S_3 = 1 + 2 + 3 = 6$입니다.

더 일반적으로, 첫 $n$개의 자연수 합은 $S_n = \frac{n(n+1)}{2}$로 알려져 있습니다. 예를 들어 $n=10$일 때, $S_{10} = \frac{10 \times 11}{2} = 55$입니다. (검산: `sum(range(1, 11))` = 55)
