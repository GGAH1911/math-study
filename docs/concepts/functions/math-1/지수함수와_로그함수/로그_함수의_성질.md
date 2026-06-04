---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 수학1
prerequisites: [docs/concepts/functions/math-1/지수함수와_로그함수.md]
enables: []
mastery: unknown
---

# 로그 함수의 성질

## 정확한 진술

로그 함수의 성질은 양수 범위에서 로그 계산을 단순화하는 핵심 규칙들입니다. $a > 0, a \neq 1$이고 $x, y > 0$일 때, 다음이 성립합니다:

$$\log_a(xy) = \log_a x + \log_a y \text{ (곱의 로그)}$$
$$\log_a\left(\frac{x}{y}\right) = \log_a x - \log_a y \text{ (몫의 로그)}$$
$$\log_a(x^n) = n\log_a x \text{ (거듭제곱의 로그)}$$
$$\log_a a = 1, \quad \log_a 1 = 0 \text{ (특수값)}$$

## 직관 및 기하적 의미

로그 함수의 성질은 **곱셈·나눗셈을 덧셈·뺄셈으로 변환**하는 데 있습니다. 이는 역함수 관계인 지수 법칙 $a^{m+n} = a^m \cdot a^n$과 정확히 대응됩니다. 즉, 지수에서의 덧셈이 밑수에서의 곱셈으로 나타나는 것처럼, 로그에서는 역으로 곱셈이 덧셈으로 표현됩니다.

이 성질들은 복잡한 곱셈이나 거듭제곱을 포함한 식을 로그로 변환했을 때 비로소 선형 형태가 되므로, 대수 계산이 훨씬 용이해집니다.

## 한 줄 예

$\log_2(16 \times 8) = \log_2 16 + \log_2 8 = 4 + 3 = 7$ (검산: $2^7 = 128 = 16 \times 8$)

## 활용 팁

실제 계산할 때는 먼저 피연산수를 인수분해하여 로그의 성질을 적용하고, 마지막에 로그값(예: $\log_2 2 = 1$)을 대입합니다. 특히 $\log_a(x^n)$ 성질은 지수 형태의 식을 선형으로 변환하므로 미분·적분과 관련된 고급 단원에서도 중요합니다.
