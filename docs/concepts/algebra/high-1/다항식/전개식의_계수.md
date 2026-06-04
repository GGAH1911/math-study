---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 수와식
grade: 고1
prerequisites: [docs/concepts/algebra/high-1/다항식.md]
enables: []
mastery: unknown
---

# 전개식의 계수

## 정확한 진술
전개식의 계수란, 다항식을 전개했을 때 특정 항의 앞에 붙는 수입니다. 예를 들어 $(x+2)^3$을 전개하면
$$x^3 + 6x^2 + 12x + 8$$
이 되는데, 이 식에서 $x^2$항의 계수는 6입니다.

일반적으로 $(a+b)^n$을 이항정리로 전개할 때, $a^{n-k}b^k$ 형태의 항의 계수는 조합 기호 $\binom{n}{k}$로 주어집니다.

## 직관/기하적 의미
전개식의 계수는 **조합론적 의미**를 담고 있습니다. $(x+y)^n$을 전개한다는 것은 $(x+y)$를 $n$번 곱한다는 뜻이므로, 각 인수마다 $x$ 또는 $y$ 중 하나를 선택하여 곱하는 과정입니다. 따라서 $x^{n-k}y^k$항이 몇 개나 만들어지는지는, $n$개 중에서 $y$를 선택할 위치 $k$개를 고르는 방법의 수와 같습니다. 이것이 바로 $\binom{n}{k}$인 것입니다.

## 한 줄 예
$(x+1)^4$에서 $x^2$의 계수는 $\binom{4}{2} = 6$입니다.

(검산: `from sympy import binomial; binomial(4, 2)` → `6`)
