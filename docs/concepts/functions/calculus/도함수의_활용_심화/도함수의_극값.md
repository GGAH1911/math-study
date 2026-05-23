---
sources: []
created: 2026-05-17
updated: 2026-05-17
concept_type: definition
domain: 함수
grade: 미적분
prerequisites: [docs/concepts/functions/calculus/도함수의_활용_심화.md]
enables: []
mastery: unknown
---

# 도함수의 극값

도함수의 부호 변화를 통해 함수의 극대·극소를 판정하는 방법입니다. 미적분 도함수의 활용 단원의 중심 기법입니다.

## 정의

미분가능한 함수 $f(x)$가 $x = a$에서 극값을 가지면 $f'(a) = 0$입니다(필요조건). 역으로, $f'(a) = 0$일 때 $f'(x)$의 부호가
- $x = a$의 좌우에서 양에서 음으로 바뀌면 $f$는 $x = a$에서 **극대**값 $f(a)$,
- 음에서 양으로 바뀌면 **극소**값 $f(a)$를 가집니다.

부호가 바뀌지 않으면 극값이 아닙니다(예: 변곡점).

## 예시

$f(x) = x^3 - 3x$의 극값을 구해 봅니다. $f'(x) = 3x^2 - 3 = 3(x-1)(x+1)$이므로 $f'(x) = 0$의 해는 $x = \pm 1$입니다.

부호를 살피면 $x < -1$에서 $f' > 0$, $-1 < x < 1$에서 $f' < 0$, $x > 1$에서 $f' > 0$이므로 $x = -1$에서 극대, $x = 1$에서 극소입니다. 극댓값 $f(-1) = -1 + 3 = 2$, 극솟값 $f(1) = 1 - 3 = -2$.

## 관련 개념

- [함수의 극값 조건](docs/concepts/functions/calculus/도함수의_활용_심화/함수의_극값_조건.md)
- [도함수의 활용 심화](docs/concepts/functions/calculus/도함수의_활용_심화.md)
