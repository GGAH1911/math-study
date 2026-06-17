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

# 함수 간의 대소관계

두 함수 $f(x), g(x)$가 어떤 구간에서 어느 쪽이 큰지를 결정하는 문제입니다. 중3 이차함수 단원에서 부등식과 그래프의 위치 관계로 연결됩니다.

## 정의

구간 $I$ 위에서 모든 $x$에 대해 $f(x) \ge g(x)$이면 "$I$에서 $f$가 $g$보다 크거나 같다"고 합니다. 이는 차함수 $h(x) = f(x) - g(x)$의 부호 판정으로 환원됩니다:
$$f(x) \ge g(x) \iff h(x) \ge 0.$$

이차함수 사이의 대소는 차함수가 보통 이차식 또는 더 낮은 차수 식이 되어 판별식·인수분해로 부호를 결정할 수 있습니다.

## 예시

구간 $[0, 1]$에서 $f(x) = x^2$와 $g(x) = x$의 대소를 결정해 봅니다. 차함수는 $h(x) = x^2 - x = x(x - 1)$. 구간 $[0, 1]$에서 $x \ge 0$, $x - 1 \le 0$이므로 $h(x) \le 0$.

따라서 $[0, 1]$에서 $f(x) \le g(x)$이며, 등호는 $x = 0$과 $x = 1$에서만 성립합니다.

## 관련 개념

- [부등식과 이차함수의 관계](docs/concepts/functions/middle-3/이차함수/부등식과_이차함수의_관계.md)
- [이차함수 교점](docs/concepts/functions/middle-3/이차함수/이차함수와_직선의_교점.md)
- [이차함수](docs/concepts/functions/middle-3/이차함수.md)
