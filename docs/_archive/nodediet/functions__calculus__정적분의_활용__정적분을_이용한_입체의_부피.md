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

# 정적분을 이용한 입체의 부피

## 정확한 진술

폐구간 $[a, b]$에서 연속이고 $f(x) \geq 0$인 함수 $y = f(x)$의 그래프를 $x$축 중심으로 회전시킨 입체(회전체)의 부피는 다음 정적분으로 정의됩니다:
$$V = \pi \int_a^b [f(x)]^2 \, dx$$

## 직관/기하적 의미

회전체는 $x$축 방향으로 원판들이 촘촘히 쌓여 있는 모습입니다. $x$에서 두께 $dx$인 얇은 원판을 생각하면, 그 원판의 반지름은 $f(x)$이고 넓이는 $\pi[f(x)]^2$입니다. 이 원판 하나의 부피는 (넓이) × (두께) = $\pi[f(x)]^2 \, dx$이고, 이 모든 원판을 $a$부터 $b$까지 더하면 전체 회전체의 부피를 얻습니다. 리만 합의 극한이 정적분이 되는 원리를 입체 도형에 그대로 적용한 것입니다.

## 한 줄 예

$y = \sqrt{x}$를 $x = 0$부터 $x = 1$까지 $x$축 중심으로 회전시킨 회전체의 부피는 $V = \pi \int_0^1 (\sqrt{x})^2 \, dx = \pi \int_0^1 x \, dx = \dfrac{\pi}{2}$입니다.

검증: `sympy.integrate(sympy.pi * sympy.Symbol('x'), (sympy.Symbol('x'), 0, 1))` 

이 개념은 **원판 방법(disk method)**이라 하며, $y$축 중심 회전이나 껍질 방법처럼 더 복잡한 상황으로도 확장됩니다.
