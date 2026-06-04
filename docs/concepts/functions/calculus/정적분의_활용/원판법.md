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

# 원판법

## 정확한 진술

$x$축을 회전축으로 하여 곡선 $y = f(x)$ (단, $a \le x \le b$, $f(x) \ge 0$)를 회전시킨 회전체의 부피는 다음과 같습니다:

$$V = \pi \int_a^b [f(x)]^2 \, dx$$

$y$축을 회전축으로 할 때는 $V = \pi \int_c^d [g(y)]^2 \, dy$입니다.

## 직관/기하적 의미

회전체를 상상해봅시다. $x$ 값이 $x$에서 $x + dx$로 조금 변할 때, 회전체의 아주 얇은 조각, 즉 하나의 원판이 생깁니다. 이 원판의:

- **반지름**: $r = f(x)$ (곡선의 높이)
- **넓이**: $\pi [f(x)]^2$
- **두께**: $dx$

따라서 이 원판 하나의 부피는 $\pi [f(x)]^2 \, dx$입니다. 이런 무한히 많은 원판들을 $a$에서 $b$까지 모두 겹쳐놓으면, 전체 회전체의 부피가 됩니다(정적분). 원판 모양의 얇은 조각들로 회전체를 쌓아올린다고 해서 "원판법(disc method)"이라고 부릅니다.

## 한 줄 예

$y = \sqrt{x}$를 $0 \le x \le 4$ 범위에서 $x$축 중심으로 회전시킨 회전체의 부피는:

$$V = \pi \int_0^4 (\sqrt{x})^2 \, dx = \pi \int_0^4 x \, dx = \pi \left[ \frac{x^2}{2} \right]_0^4 = 8\pi$$

검산: `sympy.integrate(x, (x, 0, 4))` → $8$
