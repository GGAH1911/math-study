---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 수학2
prerequisites: [docs/concepts/functions/math-2/함수의_극한과_연속.md]
enables: []
mastery: unknown
---

# 연속성정의

## 정확한 진술

함수 $f(x)$가 **$x=a$에서 연속**이라는 것은 다음 세 조건을 모두 만족하는 경우입니다:

1. $f(a)$가 정의됨
2. $\lim_{x \to a} f(x)$가 존재함
3. $\lim_{x \to a} f(x) = f(a)$

이 세 조건을 한 식으로 표현하면:
$$\lim_{x \to a} f(x) = f(a)$$

함수 $f(x)$가 **구간 $(a, b)$에서 연속**이려면 그 구간의 모든 점에서 연속이어야 합니다. 폐구간 $[a, b]$에서 연속이려면 $(a, b)$의 모든 점에서 연속이고, 좌끝점 $x=a$에서 우연속($\lim_{x \to a^+} f(x) = f(a)$), 우끝점 $x=b$에서 좌연속($\lim_{x \to b^-} f(x) = f(b)$)이어야 합니다.

## 직관과 기하적 의미

연속성은 "함수의 그래프가 끊어지지 않는다"는 뜻입니다. $x=a$ 근처에서 $x$가 $a$에 가까워질수록 $f(x)$도 $f(a)$에 가까워지며, 정확히 $x=a$일 때 값이 $f(a)$가 되어야 합니다.

반대로 연속이 아닌 점을 **불연속점**이라 합니다. 예를 들어 $\lim_{x \to a} f(x)$가 존재하지 않거나, 극한값이 존재해도 $f(a)$와 다르면 불연속입니다.

## 한 줄 예

$f(x) = x^2 + 1$은 모든 실수에서 연속이지만, $g(x) = \begin{cases} x & (x \neq 0) \\ 1 & (x = 0) \end{cases}$는 $x=0$에서 불연속입니다. ($\lim_{x \to 0} g(x) = 0 \neq 1 = g(0)$)

**검산:** `sympy.limit(x**2 + 1, x, 2)` 결과는 $5 = f(2)$로 연속성 조건 만족.
