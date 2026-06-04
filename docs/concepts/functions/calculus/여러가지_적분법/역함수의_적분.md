---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 미적분
prerequisites: [docs/concepts/functions/calculus/여러가지_적분법.md]
enables: []
mastery: unknown
---

# 역함수의 적분

## 정확한 진술

역함수의 적분은 역함수 $f^{-1}(x)$를 피적분함수로 하는 정적분을 계산하는 방법입니다. 주로 부분적분을 이용하여 다음과 같이 표현됩니다:

$$\int f^{-1}(x) dx = xf^{-1}(x) - \int x \cdot \frac{d}{dx}f^{-1}(x) dx$$

또는 정적분 형태로, $y = f(x)$가 순증가/순감소 함수일 때:

$$\int_a^b f^{-1}(x) dx = bf^{-1}(b) - af^{-1}(a) - \int_{f^{-1}(a)}^{f^{-1}(b)} f(t) dt$$

## 직관과 기하적 의미

$y = f(x)$와 $y = f^{-1}(x)$ 그래프는 $y = x$에 대해 대칭입니다. 역함수의 그래프 아래 넓이는 원래 함수의 그래프 아래 넓이와 밀접한 관계가 있습니다. 

직사각형 영역을 생각해보면, 영역 $[a, b] \times [f^{-1}(a), f^{-1}(b)]$는 원 함수 곡선 아래 넓이와 역함수 곡선 아래 넓이의 합으로 분할됩니다. 이 관계식이 위의 공식입니다.

## 한 줄 예

$f(x) = x^2$ (단, $x \geq 0$)이면 $f^{-1}(x) = \sqrt{x}$이고, 부분적분으로 $\int \sqrt{x} dx = x\sqrt{x} - \frac{2}{3}x^{3/2} + C$입니다. 정적분 $\int_1^4 \sqrt{x} dx$는 기하적으로 원함수와의 대칭성을 이용해 $4 \cdot 2 - 1 \cdot 1 - \int_1^2 t^2 dt = 8 - 1 - 7/3 = 8/3$로도 검증됩니다. (`sympy.integrate(sqrt(x), (x, 1, 4))` → $14/3$)
