---
sources: []
created: 2026-05-17
updated: 2026-05-17
concept_type: definition
domain: 함수
grade: 수학2
prerequisites: [docs/concepts/functions/math-2/적분.md]
enables: []
mastery: unknown
---

# 도함수와 원함수

미분의 역연산으로서 원함수(부정적분)와 도함수 사이의 관계를 다룹니다. 수학2 적분 단원의 출발점입니다.

## 정의

함수 $F(x)$의 도함수가 $f(x)$이면, 즉 $F'(x) = f(x)$이면 $F(x)$를 $f(x)$의 **원함수**라 합니다. 두 원함수는 상수만큼만 차이가 나므로 부정적분은
$$\int f(x)\, dx = F(x) + C \quad (C\text{는 적분상수})$$
로 표현됩니다.

기본 공식으로는 $n \neq -1$일 때
$$\int x^n\, dx = \frac{x^{n+1}}{n+1} + C, \qquad \int k\, dx = kx + C.$$

## 예시

$f(x) = 3x^2 + 2$의 원함수를 구해 봅니다. 항별로 적분하면
$$F(x) = \int (3x^2 + 2)\, dx = x^3 + 2x + C.$$
실제로 $F'(x) = 3x^2 + 2 = f(x)$이므로 원함수임을 확인할 수 있습니다.

특히 $F(0) = 5$가 되도록 적분상수를 정하면 $C = 5$이고 $F(x) = x^3 + 2x + 5$입니다.

## 관련 개념

- [적분](docs/concepts/functions/math-2/적분.md)
