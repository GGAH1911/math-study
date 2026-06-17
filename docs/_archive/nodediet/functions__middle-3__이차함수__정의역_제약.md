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

# 정의역 제약

이차함수의 정의역에 추가로 부여하는 조건으로, 어떤 구간 또는 부분집합으로 한정하는 것입니다. 중3 이차함수의 최댓값·최솟값 문제에서 결정적인 역할을 합니다.

## 정의

함수 $f(x)$의 정의역을 임의의 부분집합 $D \subseteq \mathbb{R}$로 한정하면, 같은 식이라도 치역과 최댓값·최솟값이 달라집니다. 이차함수에서는 정의역 제약이 다음 두 가지 형태로 자주 나타납니다.
- **닫힌구간** $[\alpha, \beta]$: 최댓값·최솟값이 반드시 존재(꼭짓점 또는 끝점에서).
- **부등식 조건**: 예를 들어 $x \ge 0$, $x \ne p$ 등.

## 예시

$f(x) = -x^2 + 4x$의 정의역을 $\mathbb{R}$ 전체로 두면 $f(x) = -(x-2)^2 + 4$이므로 $x = 2$에서 최댓값 $4$를 갖고, 최솟값은 없습니다(치역 $(-\infty, 4]$).

같은 함수의 정의역을 $[0, 1]$로 제약하면 축 $x = 2$가 구간 밖이므로 끝점에서만 비교합니다. $f(0) = 0$, $f(1) = 3$이므로 최댓값은 $3$, 최솟값은 $0$입니다.

## 관련 개념

- [구간제한](docs/concepts/functions/middle-3/이차함수/정의역_제한.md)
- [정의역 제한 내 극값](docs/concepts/functions/middle-3/이차함수/구간별_최댓값과_최솟값.md)
- [이차함수](docs/concepts/functions/middle-3/이차함수.md)
