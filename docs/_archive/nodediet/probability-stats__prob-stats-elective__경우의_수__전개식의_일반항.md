---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 확률통계
grade: 확률과통계
prerequisites: [docs/concepts/probability-stats/prob-stats-elective/경우의_수.md]
enables: []
mastery: unknown
---

# 전개식의 일반항

## 정확한 진술

$(a+b)^n$을 전개했을 때, 일반항(general term)은 다음과 같습니다:

$$\binom{n}{r}a^{n-r}b^r \quad (r = 0, 1, 2, \ldots, n)$$

여기서 $\binom{n}{r} = \frac{n!}{r!(n-r)!}$는 이항계수(조합)이고, $r$은 항의 위치를 나타냅니다.

## 직관과 의미

$(a+b)^n = (a+b)(a+b) \cdots (a+b)$ (n번)를 전개할 때를 생각해 봅시다. 각 괄호에서 $a$ 또는 $b$ 중 하나를 선택해야 합니다.

- $a$를 $(n-r)$번 선택하고 $b$를 $r$번 선택하면, 곱의 결과는 $a^{n-r}b^r$입니다.
- 이렇게 선택하는 **경우의 수**가 바로 $\binom{n}{r}$입니다. (n개 중에서 $b$를 뽑을 위치 $r$개를 고르는 방법의 수)

따라서 $a^{n-r}b^r$ 항의 **계수**가 $\binom{n}{r}$이 되는 것입니다.

## 예제

$(2+x)^3$의 전개식에서:
- 일반항: $\binom{3}{r}2^{3-r}x^r$
- $r=0$: $\binom{3}{0}2^3 x^0 = 8$
- $r=1$: $\binom{3}{1}2^2 x^1 = 12x$
- $r=2$: $\binom{3}{2}2^1 x^2 = 6x^2$
- $r=3$: $\binom{3}{3}2^0 x^3 = x^3$

따라서 $(2+x)^3 = 8 + 12x + 6x^2 + x^3$ ✓

`from sympy import symbols, expand; x = symbols('x'); print(expand((2+x)**3))`
