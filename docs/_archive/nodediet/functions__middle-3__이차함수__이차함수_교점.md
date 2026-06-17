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

# 이차함수의 교점

이차함수의 그래프가 다른 곡선·직선과 만나는 점을 가리키며, 두 식을 연립하여 구합니다. 중3 이차함수 단원에서 그래프 해석의 핵심 응용입니다.

## 정의

두 함수 $y = f(x), y = g(x)$의 그래프의 교점의 $x$좌표는 방정식 $f(x) = g(x)$의 해입니다. 이차함수 $y = ax^2 + bx + c$와 직선 $y = mx + n$의 교점은
$$ax^2 + bx + c = mx + n$$
의 해이며, 정리하면 이차방정식이 됩니다. 판별식 $D$의 부호로 교점의 개수가 결정됩니다.
- $D > 0$: 서로 다른 두 점에서 만남.
- $D = 0$: 한 점에서 접함.
- $D < 0$: 만나지 않음.

## 예시

$y = x^2$와 $y = 2x + 3$의 교점을 구해 봅니다. 연립하여 $x^2 = 2x + 3$, 즉 $x^2 - 2x - 3 = 0$, $(x-3)(x+1) = 0$이므로 $x = 3$ 또는 $x = -1$.

해당 $y$값은 각각 $9, 1$이므로 교점은 $(3, 9)$와 $(-1, 1)$입니다.

## 관련 개념

- [이차함수의 판별식](docs/concepts/functions/middle-3/이차함수/이차함수의_판별식.md)
- [부등식과 이차함수의 관계](docs/concepts/functions/middle-3/이차함수/부등식과_이차함수의_관계.md)
- [이차함수](docs/concepts/functions/middle-3/이차함수.md)
