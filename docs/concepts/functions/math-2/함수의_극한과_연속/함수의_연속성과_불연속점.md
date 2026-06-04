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

# 함수의 연속성과 불연속점

## 정확한 진술

함수 $f(x)$가 $x=a$에서 **연속**(continuous)이라는 것은 다음 세 조건을 **모두** 만족하는 경우입니다:

1. $f(a)$가 정의되어 있음
2. $\lim_{x \to a} f(x)$가 존재함
3. $\lim_{x \to a} f(x) = f(a)$

이 세 조건 중 **하나라도 만족하지 않으면** $x=a$는 **불연속점**(point of discontinuity)입니다.

## 직관과 기하적 의미

연속성은 "그래프가 끊어지지 않는다"는 뜻입니다. 여기서 "끊어진다"는 세 가지 경우를 포함합니다:

- **구멍(hole)**: $f(a)$가 정의되지 않음. 예를 들어 $f(x) = \frac{x^2-1}{x-1}$는 $x=1$에서 정의되지 않습니다.
- **진동**: 극한값이 존재하지 않음. $x$가 특정 값에 가까워질 때 함수값이 계속 진동합니다.
- **점프(jump)**: 극한값은 존재하지만 함수값과 다름. $x$의 왼쪽과 오른쪽에서 다른 값으로 수렴합니다.

손가락으로 그래프를 따라가면서 연필을 떨어뜨리지 않고 그릴 수 있다면 그 구간에서 연속이고, 어딘가 끊어지는 부분이 있으면 불연속점이 있는 것입니다.

## 한 줄 예

$f(x) = \begin{cases} x+1 & (x \neq 2) \\ 5 & (x=2) \end{cases}$ 에서 $x=2$는 불연속점입니다. ($\lim_{x \to 2} f(x) = 3 \neq 5 = f(2)$)
