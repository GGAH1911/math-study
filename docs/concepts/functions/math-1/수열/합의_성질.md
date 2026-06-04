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

# 합의 성질

## 정확한 진술

수열 $\{a_n\}$, $\{b_n\}$과 상수 $c$에 대해 다음 성질들이 성립합니다.

$$\sum_{k=1}^{n} (a_k + b_k) = \sum_{k=1}^{n} a_k + \sum_{k=1}^{n} b_k$$

$$\sum_{k=1}^{n} c \cdot a_k = c \sum_{k=1}^{n} a_k$$

$$\sum_{k=1}^{n} c = nc \quad (c\text{는 상수})$$

이들은 **합의 선형성(linearity of summation)**으로 불리며, 합 기호의 근본적 성질입니다. 즉, 덧셈과 스칼라배에 대해 합 기호가 "분배"된다는 뜻입니다.

## 직관/기하적 의미

첫 번째 성질은 간단합니다: $(a_1 + b_1) + (a_2 + b_2) + \cdots + (a_n + b_n)$을 계산할 때, 먼저 $a$들을 모두 더하고 나중에 $b$들을 더하나, 아니면 각 항마다 묶어서 더하나 결과는 같다는 뜻입니다(덧셈의 결합법칙).

두 번째 성질도 직관적입니다: $c \cdot a_1 + c \cdot a_2 + \cdots + c \cdot a_n = c(a_1 + a_2 + \cdots + a_n)$ ← 공통인수로 빼내기입니다.

세 번째 성질은 같은 상수 $c$를 $n$번 더하면 $nc$가 된다는 곱셈의 정의입니다.

이 성질들 덕분에 복잡한 수열의 합도 체계적으로 계산할 수 있습니다.

## 한 줄 예

$\sum_{k=1}^{5} (2k + 3) = 2\sum_{k=1}^{5} k + \sum_{k=1}^{5} 3 = 2 \cdot 15 + 3 \cdot 5 = 30 + 15 = 45$ (확인: $5 + 7 + 9 + 11 + 13 = 45$ ✓)
