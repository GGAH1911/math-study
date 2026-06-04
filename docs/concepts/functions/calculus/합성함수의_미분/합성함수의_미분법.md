---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 미적분
prerequisites: [docs/concepts/functions/calculus/합성함수의_미분.md]
enables: []
mastery: unknown
---

# 합성함수의 미분법

## 정확한 진술

$y = f(u)$, $u = g(x)$로 주어진 합성함수 $y = f(g(x))$의 도함수를 구하는 규칙을 **합성함수의 미분법**(chain rule)이라 합니다. 이를 두 가지 표기법으로 나타내면:

$$\frac{dy}{dx} = \frac{dy}{du} \cdot \frac{du}{dx} = f'(g(x)) \cdot g'(x)$$

즉, 합성함수의 도함수는 바깥 함수를 안 함수로 미분한 것에, 안 함수의 도함수를 곱합니다.

## 직관과 의미

합성함수의 미분법의 핵심은 **변화율의 누적**입니다. $x$가 조금 변할 때:
- 먼저 $u = g(x)$가 속도 $g'(x)$로 변합니다.
- 그 다음 $y = f(u)$가 속도 $f'(g(x))$로 변합니다.
- 최종적으로 $y$는 두 변화율을 곱한 속도로 변합니다.

라이프니츠 표기법 $\frac{dy}{dx} = \frac{dy}{du} \cdot \frac{du}{dx}$는 분수처럼 보이지만 실제로는 미분의 연쇄 구조를 나타냅니다. 기하학적으로는 복잡한 곡선의 순간 기울기를 중간 단계들로 분해하는 것입니다. 기어가 톱니를 맞물리듯이, 중간 변수를 통한 연쇄적 변화를 추적합니다.

## 한 줄 예

$y = (2x + 1)^3$을 미분하면, 안 함수 $u = 2x + 1$은 $\frac{du}{dx} = 2$이고 바깥 함수 $y = u^3$은 $\frac{dy}{du} = 3u^2$이므로, $\frac{dy}{dx} = 3(2x+1)^2 \cdot 2 = 6(2x+1)^2$입니다.
