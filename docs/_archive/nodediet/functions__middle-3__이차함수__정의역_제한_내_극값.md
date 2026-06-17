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

# 정의역 제한 내 극값

이차함수의 정의역을 어떤 닫힌구간으로 제한했을 때 그 구간에서의 최댓값과 최솟값을 찾는 절차입니다. 중3 이차함수 단원의 대표 응용 문제 유형입니다.

## 정의

이차함수 $f(x) = a(x - p)^2 + q$의 정의역을 $[\alpha, \beta]$로 제한할 때 최댓값·최솟값은 다음 점에서 나타납니다.
- 꼭짓점 $x = p$가 $[\alpha, \beta]$에 속하면, 함숫값 $f(p)$와 끝점 함숫값 $f(\alpha),\ f(\beta)$를 모두 비교.
- 꼭짓점이 구간 밖이면, 함수가 그 구간에서 단조이므로 끝점에서만 비교.

$a > 0$이면 꼭짓점에서 최솟값, 양 끝점 중 한쪽에서 최댓값. $a < 0$이면 그 반대.

## 예시

$f(x) = x^2 - 2x + 3 = (x-1)^2 + 2$의 구간 $[2, 4]$에서의 최댓값·최솟값을 구해 봅니다. 꼭짓점 $x = 1$이 구간 밖이고 $a > 0$이므로 $f$는 $[2, 4]$에서 증가합니다.

따라서 최솟값은 $f(2) = 3$, 최댓값은 $f(4) = 11$입니다.

## 관련 개념

- [정의역 제약](docs/concepts/functions/middle-3/이차함수/정의역_제한.md)
- [구간에서의 극값](docs/concepts/functions/middle-3/이차함수/구간별_최댓값과_최솟값.md)
- [이차함수](docs/concepts/functions/middle-3/이차함수.md)
