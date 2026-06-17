---
sources: []
created: 2026-05-17
updated: 2026-05-17
concept_type: definition
domain: 함수
grade: 중3
prerequisites: [docs/concepts/functions/middle-3/이차함수.md]
enables: []
mastery: unknown
---

# 정점(꼭짓점)

이차함수 그래프에서 곡선의 방향이 바뀌는 한 점, 즉 꼭짓점입니다. 중3 이차함수 단원에서 최댓값·최솟값과 직접 연결됩니다.

## 정의

이차함수 $f(x) = ax^2 + bx + c$ ($a \neq 0$)는 표준형 $f(x) = a(x - p)^2 + q$로 변형할 수 있으며, 이때 점 $(p, q)$를 그래프의 **꼭짓점**(정점)이라 합니다.
- $a > 0$이면 꼭짓점에서 최솟값 $q$.
- $a < 0$이면 꼭짓점에서 최댓값 $q$.

일반형에서 꼭짓점 좌표는
$$\left(-\frac{b}{2a},\ c - \frac{b^2}{4a}\right)$$
로 직접 계산할 수 있고, 축은 $x = -\dfrac{b}{2a}$입니다.

## 예시

$f(x) = x^2 - 6x + 8$의 꼭짓점을 구해 봅니다. 완전제곱식으로 정리하면
$$f(x) = (x - 3)^2 - 1.$$
꼭짓점은 $(3, -1)$이며, $a = 1 > 0$이므로 이 점에서 최솟값 $-1$을 갖습니다.

## 관련 개념

- [이차함수의 최값](docs/concepts/functions/middle-3/이차함수/이차함수의_최댓값과_최솟값.md)
- [이차함수](docs/concepts/functions/middle-3/이차함수.md)
