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

# 적분을 이용한 부피

## 정확한 진술

곡선 $y = f(x)$ (단, $f(x) \geq 0$, $a \leq x \leq b$)을 $x$축 중심으로 회전시킨 회전체의 부피는

$$V = \pi \int_a^b \{f(x)\}^2 \, dx$$

로 정의합니다. 더 일반적으로, $x$에 수직인 단면의 넓이가 $S(x)$인 입체도형의 부피는

$$V = \int_a^b S(x) \, dx$$

입니다.

## 직관과 기하적 의미

회전체를 아주 얇은 원판들(높이 $dx$)로 잘게 쌓는다고 생각해봅시다. $x$ 위치에서 원판의 반지름이 $f(x)$이면, 그 원판의 부피는 $\pi \{f(x)\}^2 dx$입니다. 이를 $a$부터 $b$까지 모두 더하면(적분하면) 전체 회전체의 부피가 됩니다.

더 넓은 관점에서, 어떤 입체도형이든 각 위치에서 수직 단면의 넓이 $S(x)$를 알면, 그걸 적분해서 부피를 구할 수 있습니다. 이것이 정적분이 부피 계산에 쓰이는 핵심 원리입니다.

## 한 줄 예

$y = \sqrt{x}$ ($0 \leq x \leq 4$)를 $x$축 중심으로 회전시킨 회전체의 부피는 $V = \pi \int_0^4 x \, dx = \pi \cdot 8 = 8\pi$ (sympy: `pi*integrate(x, (x,0,4))` = $8\pi$)
