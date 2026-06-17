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

# 연속함수의 정의

## 정확한 진술

함수 $f$가 정의역의 어떤 점 $x = a$에서 **연속**(continuous)이라는 것은 다음 세 조건을 모두 만족할 때입니다:

1. $f(a)$가 정의되어 있다.
2. $\lim_{x \to a} f(x)$가 존재한다.
3. $\lim_{x \to a} f(x) = f(a)$이다.

달리 말해, 극한값과 함수값이 정확히 같아야 합니다. 함수 $f$가 어떤 구간의 **모든 점에서 연속**이면, 그 구간에서 연속이라고 합니다.

## 직관/기하적 의미

연속함수는 그래프를 **펜을 떼지 않고 그릴 수 있는 함수**입니다. 점 $x = a$ 근처에서 $x$가 $a$에 아주 가까워질 때, 함수값 $f(x)$도 $f(a)$에 아주 가까워진다는 뜻이죠. 

반대로 연속이 아닌 함수(불연속함수)는 특정 점에서 "점프"하거나 "구멍"이 생기는 함수입니다. 예를 들어, 부호함수 $\text{sgn}(x) = \begin{cases} -1 & (x < 0) \\ 0 & (x = 0) \\ 1 & (x > 0) \end{cases}$는 $x = 0$에서 좌극한, 우극한, 함수값이 모두 다르므로 불연속입니다.

## 한 줄 예

함수 $f(x) = 2x + 1$은 모든 점에서 연속입니다. 왜냐하면 임의의 점 $a$에서 $\lim_{x \to a} (2x + 1) = 2a + 1 = f(a)$이기 때문입니다. 반면 $g(x) = \begin{cases} x & (x \neq 1) \\ 2 & (x = 1) \end{cases}$는 $x = 1$에서 불연속입니다($\lim_{x \to 1} g(x) = 1 \neq 2 = g(1)$).
