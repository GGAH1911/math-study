---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 수와식
grade: 중3
prerequisites: [docs/concepts/algebra/middle-3/실수와_그_계산.md]
enables: []
mastery: unknown
---

# 무리수의 계산

## 정확한 진술

무리수는 유리수로 나타낼 수 없는 실수입니다. 즉, $\frac{p}{q}$ (단, $p, q$는 정수, $q \neq 0$) 형태로 표현 불가능한 수를 무리수라 합니다. 무리수의 계산이란 제곱근, 세제곱근 등 근호를 포함한 무리수들 간의 덧셈, 뺄셈, 곱셈, 나눗셈을 의미합니다.

제곱근의 기본 계산 법칙은 다음과 같습니다:
- $\sqrt{a} \cdot \sqrt{b} = \sqrt{ab}$ (단, $a, b \geq 0$)
- $\frac{\sqrt{a}}{\sqrt{b}} = \sqrt{\frac{a}{b}}$ (단, $a \geq 0, b > 0$)

분모에 무리수가 있을 때는 분모를 유리화하여 계산합니다.

## 직관/기하적 의미

유리수만으로는 수직선을 완전히 채울 수 없습니다. 예를 들어 한 변의 길이가 1인 정사각형의 대각선 길이 $\sqrt{2}$는 어떤 유리수로도 정확히 표현되지 않습니다. 무리수의 계산은 이러한 "틈새"에 있는 수들을 다루는 체계적 방법을 제공하여, 실수의 완전성을 보장합니다.

근호 안의 수를 간단히 하거나 분모를 유리화하는 것은 무리수를 더 다루기 쉬운 형태로 변환하되, 그 값은 보존하는 과정입니다.

## 한 줄 예

$\sqrt{12} \times \sqrt{3} = \sqrt{36} = 6$이고, $\frac{1}{\sqrt{2}} = \frac{\sqrt{2}}{2}$ (유리화)입니다. (`sympy.simplify(sqrt(12) * sqrt(3))`, `sympy.simplify(1/sqrt(2))`)
