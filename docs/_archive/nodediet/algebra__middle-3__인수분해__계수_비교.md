---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 수와식
grade: 중3
prerequisites: [docs/concepts/algebra/middle-3/인수분해.md]
enables: []
mastery: unknown
---

# 계수 비교

## 정확한 진술

두 다항식이 모든 $x$에 대해 같으면(**항등식**), 같은 차수의 계수가 모두 같습니다.

$$f(x) = a_n x^n + a_{n-1} x^{n-1} + \cdots + a_1 x + a_0$$
$$g(x) = b_n x^n + b_{n-1} x^{n-1} + \cdots + b_1 x + b_0$$

에서 $f(x) = g(x)$ (모든 $x$)이면, 각 차수의 계수가 일치합니다:
$$a_n = b_n, \quad a_{n-1} = b_{n-1}, \quad \ldots, \quad a_1 = b_1, \quad a_0 = b_0$$

## 직관/기하적 의미

다항식을 계수의 수열로 생각하면, 두 다항식이 항등적으로 같다는 것은 "모든 위치의 계수가 정확히 일치"한다는 뜻입니다. 즉, 몇 가지 $x$ 값만 대입해서 확인하는 대신, 계수를 한꺼번에 비교하여 미지수를 한 번에 결정할 수 있습니다. 이는 특히 **부분분수 분해**, **복소수 등식**, **다항식의 나머지 정리** 등에서 강력합니다.

## 한 줄 예

$x^2 + 3x - 2 = ax^2 + bx + c$에서 계수를 비교하면 $a = 1$, $b = 3$, $c = -2$입니다.

## 자주 만나는 활용

**부분분수 분해**: $\displaystyle\frac{5x + 3}{(x-1)(x+2)} = \frac{A}{x-1} + \frac{B}{x+2}$에서 우변을 통분한 후 분자의 계수를 비교하여 $A$, $B$를 구합니다.

**복소수 등식**: $(a + bi)(c + di) = 3 + 4i$에서 실부와 허부의 계수를 각각 비교합니다.

**검산 예시** (sympy): `sympy.symbols('a b c'); sympy.solve([a-1, b-3, c+2], [a, b, c])` → `{a: 1, b: 3, c: -2}`
