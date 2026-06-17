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

# 함수의 그래프와 넓이

## 정확한 진술

함수 $y = f(x)$가 폐구간 $[a, b]$에서 연속이고 $f(x) \geq 0$일 때, 곡선 $y = f(x)$와 $x$축, 그리고 두 직선 $x = a$, $x = b$로 둘러싸인 영역의 넓이를 정적분으로 정의합니다:
$$S = \int_a^b f(x) \, dx$$

## 직관 및 기하적 의미

정적분이 넓이를 나타내는 이유는 리만 합의 기하학적 해석에서 비롯됩니다. 구간 $[a, b]$를 $n$개의 작은 부분구간으로 나누고, 각 부분구간에서 함숫값을 높이로 하는 직사각형들을 만들면, 이 직사각형들의 넓이 합(리만 합)이 구간의 분할을 세밀하게 할수록 실제 곡선 아래의 넓이에 가까워집니다. $n \to \infty$일 때의 극한값이 바로 정적분입니다.

기하학적으로는 **곡선 아래의 면적을 무수히 많은 얇은 직사각형으로 분해한 후 모두 더하는 과정**이라고 생각할 수 있습니다. 이것이 미분과 적분의 기본정리로 연결되어, 도함수를 알면 넓이를 계산할 수 있게 됩니다.

## 구체적 예

포물선 $y = x^2$과 $x$축, 두 직선 $x = 0$, $x = 2$로 둘러싸인 영역의 넓이는:
$$S = \int_0^2 x^2 \, dx = \left[\frac{x^3}{3}\right]_0^2 = \frac{8}{3}$$

(검산: `from sympy import integrate, symbols; x = symbols('x'); integrate(x**2, (x, 0, 2))` → $\frac{8}{3}$)
