---
sources: []
created: 2026-05-17
updated: 2026-05-17
concept_type: definition
domain: 함수
grade: 미적분
prerequisites: [docs/concepts/functions/calculus/정적분의_활용.md]
enables: []
mastery: unknown
---

# 적분을 이용한 넓이

곡선과 직선으로 둘러싸인 평면 영역의 넓이를 정적분으로 계산하는 방법입니다. 미적분 정적분의 활용 단원의 대표 응용입니다.

## 정의

구간 $[a, b]$에서 연속인 함수 $f(x), g(x)$가 $f(x) \ge g(x)$를 만족할 때, 두 곡선 $y = f(x)$, $y = g(x)$와 두 직선 $x = a$, $x = b$로 둘러싸인 영역의 넓이는
$$S = \int_a^b \{f(x) - g(x)\}\, dx.$$
일반적으로 $f, g$의 대소가 구간에서 바뀌면 절댓값을 사용해 $S = \displaystyle\int_a^b |f(x) - g(x)|\, dx$로 두고 부호가 바뀌는 점을 기준으로 적분 구간을 나눕니다.

## 예시

곡선 $y = x^2$와 직선 $y = x$로 둘러싸인 영역의 넓이를 구해 봅니다. 교점은 $x^2 = x$에서 $x = 0, 1$. 구간 $[0, 1]$에서 $x \ge x^2$이므로
$$S = \int_0^1 (x - x^2)\, dx = \left[\frac{x^2}{2} - \frac{x^3}{3}\right]_0^1 = \frac{1}{2} - \frac{1}{3} = \frac{1}{6}.$$

## 관련 개념

- [정적분의 활용](docs/concepts/functions/calculus/정적분의_활용.md)
