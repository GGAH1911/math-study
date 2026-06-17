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

# 합성함수 미분

## 정확한 진술

두 함수 $f$, $g$에 대해 합성함수 $f(g(x))$의 도함수는 다음과 같습니다.

$$\frac{d}{dx}[f(g(x))] = f'(g(x)) \cdot g'(x)$$

또는 $u = g(x)$, $y = f(u)$로 놓으면:

$$\frac{dy}{dx} = \frac{dy}{du} \cdot \frac{du}{dx}$$

이를 **연쇄 미분법(chain rule)**이라 하며, 합성함수 미분의 핵심입니다.

## 직관과 기하적 의미

합성함수의 미분을 이해하려면 '변화율의 곱셈'을 생각해야 합니다. $y = f(g(x))$에서:

- $x$가 작은 양만큼 변할 때, 먼저 $u = g(x)$가 $g'(x)$의 비율로 변합니다.
- 그러면 $y = f(u)$는 그 변한 $u$의 크기에 따라 $f'(u)$의 비율로 다시 변합니다.

결국 $x$의 변화가 $y$에 미치는 최종 영향은 이 두 변화율을 **곱한 것**입니다. 

기하학적으로는 합성함수의 그래프 상의 점에서 접선의 기울기가 바깥 함수와 안쪽 함수의 기울기의 곱으로 결정된다는 의미입니다.

## 구체적 예시

$y = (2x + 1)^3$을 미분해봅시다.

$u = 2x + 1$, $y = u^3$으로 놓으면:
- $\frac{du}{dx} = 2$
- $\frac{dy}{du} = 3u^2 = 3(2x+1)^2$

따라서:
$$\frac{dy}{dx} = 3(2x+1)^2 \cdot 2 = 6(2x+1)^2$$

$x = 1$일 때: $\frac{dy}{dx} = 6(3)^2 = 54$

**검산**: `sympy.diff((2*x + 1)**3, x)` → $6(2x+1)^2$ ✓
