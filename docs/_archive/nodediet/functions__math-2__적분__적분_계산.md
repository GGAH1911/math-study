---
unit: 적분
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 수학2
prerequisites: [docs/concepts/functions/calculus/정적분의_활용.md]
enables: []
mastery: unknown
---

# 적분 계산

## 정확한 진술

정적분 $\displaystyle \int_a^b f(x) \, dx$를 계산하는 기본 방법은 **미적분학의 기본정리**를 이용하는 것입니다. $F(x)$를 $f(x)$의 부정적분(즉, $F'(x) = f(x)$를 만족하는 함수)이라 하면,

$$\int_a^b f(x) \, dx = [F(x)]_a^b = F(b) - F(a)$$

입니다. 여기서 $[F(x)]_a^b$는 $F(b) - F(a)$를 나타내는 기호입니다.

## 직관/기하적 의미

적분 기호 $\int$는 원래 '무한히 많은 것들의 합'을 뜻합니다. 어떤 함수 $f(x)$의 그래프 아래 넓이를 구하려면, 가로 구간을 무한히 잘게 나누어 직사각형 넓이들을 모두 더해야 합니다. 

부정적분 $F(x)$는 이 '누적된 넓이'를 함수로 나타낸 것입니다. 따라서 구간 $[a, b]$에서의 넓이는 $a$부터 누적한 값에서 $b$까지 누적한 값을 빼면—즉, $F(b) - F(a)$를 구하면 됩니다. 이것이 미적분학의 기본정리가 말하는 내용입니다.

## 한 줄 예

$\displaystyle \int_0^2 (3x^2 + 1) \, dx$를 계산하면: 부정적분은 $F(x) = x^3 + x$이므로, $[F(x)]_0^2 = (8 + 2) - (0 + 0) = 10$입니다. (검증: `from sympy import *; x = symbols('x'); integrate(3*x**2 + 1, (x, 0, 2))` → 10)
