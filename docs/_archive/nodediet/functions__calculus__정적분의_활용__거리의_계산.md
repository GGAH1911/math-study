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

# 거리의 계산

## 정확한 진술

폐구간 $[a, b]$에서 미분가능한 함수 $y = f(x)$의 그래프 위의 두 점 $(a, f(a))$와 $(b, f(b))$를 잇는 곡선의 길이(호의 길이)는 다음 정적분으로 구합니다:

$$L = \int_a^b \sqrt{1 + \{f'(x)\}^2} \, dx$$

매개변수 표현 $x = x(t), y = y(t)$ ($\alpha \le t \le \beta$)로 주어진 곡선의 경우:

$$L = \int_\alpha^\beta \sqrt{\{x'(t)\}^2 + \{y'(t)\}^2} \, dt$$

## 직관/기하적 의미

곡선을 아주 작은 선분들로 잘게 나눈다고 생각해봅시다. 각 선분은 거의 직선에 가까우므로, 가로 길이가 $\Delta x$이고 세로 길이가 $\Delta y$인 직각삼각형의 빗변으로 근사할 수 있습니다. 피타고라스 정리에 의해 각 선분의 길이는 $\sqrt{(\Delta x)^2 + (\Delta y)^2} = \sqrt{1 + (f'(x))^2} \cdot \Delta x$입니다. 이런 선분들을 모두 더하면 정적분이 되는 것입니다. 즉, 곡선의 경사가 가파를수록($|f'(x)|$가 클수록) 같은 가로 거리에서 호의 길이가 더 길어집니다.

## 한 줄 예

$y = \frac{2}{3}x^{3/2}$을 $x = 0$에서 $x = 3$까지 따라 이동한 거리는 $\int_0^3 \sqrt{1 + x} \, dx = \frac{26}{3}$입니다.
(검산: `sympy.integrate(sympy.sqrt(1 + x), (x, 0, 3))` → $\frac{26}{3} \approx 8.667$)
