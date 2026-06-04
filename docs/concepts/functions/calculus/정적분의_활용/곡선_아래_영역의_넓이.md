---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 미적분
prerequisites: [docs/concepts/functions/calculus/정적분의_활용.md]
enables: []
mastery: unknown
---

# 곡선 아래 영역의 넓이

## 정확한 진술

함수 $f(x)$가 폐구간 $[a, b]$에서 연속이고 $f(x) \geq 0$일 때, 곡선 $y = f(x)$와 $x$축 사이의 영역의 넓이는 정적분으로 정의된다:

$$S = \int_a^b f(x) \, dx$$

## 직관/기하적 의미

정적분의 기본 아이디어는 곡선 아래 영역을 무한히 많은 얇은 직사각형으로 분할하여 넓이를 계산하는 것이다. $x$축을 폭 $\Delta x$의 작은 구간들로 나누고, 각 구간에서 함수값을 높이로 하는 직사각형을 그린다. 이 직사각형들의 넓이 합 $\sum f(x_i) \Delta x$을 구하면, $\Delta x \to 0$일 때 정적분 $\int_a^b f(x) \, dx$로 수렴한다. 따라서 정적분은 단순한 계산 기호가 아니라, 곡선과 $x$축 사이에 둘러싸인 영역의 기하학적 크기를 정확히 나타내는 수이다. 이것이 정적분을 배우는 가장 중요한 이유이다.

## 한 줄 예

$f(x) = x$일 때 구간 $[0, 2]$에서의 넓이는 $\int_0^2 x \, dx = \left[\frac{x^2}{2}\right]_0^2 = 2$이다. (sympy: `integrate(x, (x, 0, 2))`)
