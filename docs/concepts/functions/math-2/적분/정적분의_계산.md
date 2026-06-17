---
unit: 적분
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 수학2
prerequisites: [docs/concepts/functions/calculus/도함수의_활용_심화.md]
enables: []
mastery: unknown
---

# 정적분의 계산

## 정확한 진술

정적분 $\int_a^b f(x)dx$를 **계산**한다는 것은 구간 $[a,b]$에서 함수 $f(x)$의 그래프 아래 넓이를 수치로 구하는 과정입니다. 이때 핵심은 **부정적분**(원시함수)을 이용하는 것입니다.

$f(x)$의 부정적분을 $F(x)$라 하면, 즉 $F'(x) = f(x)$를 만족하면:

$$\int_a^b f(x)dx = F(b) - F(a) = [F(x)]_a^b$$

이것이 **미적분학의 기본정리(Fundamental Theorem of Calculus)**입니다.

## 직관 및 기하적 의미

정적분은 곡선 아래 넓이의 합을 직접 계산하려면 극한 과정이 필요해 복잡합니다. 하지만 미적분학의 기본정리는 이 과정을 우회합니다. 도함수의 역과정인 부정적분만 찾으면, 구간의 양 끝점에서 함수값의 **차**만 구하면 된다는 뜻입니다.

기하학적으로는 $F(x)$가 누적 변화량을 나타내므로, $F(b) - F(a)$는 $a$에서 $b$까지의 총변화량입니다. 예를 들어 속도함수를 적분하면 이동거리를, 가속도함수를 적분하면 속도 변화를 얻게 되는 원리입니다.

## 한 줄 예

$$\int_0^3 (3x^2 + 2)dx = [x^3 + 2x]_0^3 = (27 + 6) - 0 = 33$$

여기서 $x^3 + 2x$는 $3x^2 + 2$의 부정적분입니다. (검산: `sympy.integrate(3*x**2 + 2, (x, 0, 3))` 결과 33)
