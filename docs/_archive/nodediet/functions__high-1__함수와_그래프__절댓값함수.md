---
unit: 함수와 그래프
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 고1
prerequisites: [docs/concepts/functions/calculus/도함수의_활용_심화.md]
enables: []
mastery: unknown
---

# 절댓값함수

## 정의

실수 $x$에 대해 절댓값 $|x|$를 다음과 같이 정의합니다:
$$|x| = \begin{cases} x & \text{if } x \geq 0 \\ -x & \text{if } x < 0 \end{cases}$$

**절댓값함수**는 절댓값의 성질을 이용해 정의된 함수입니다. 가장 기본적인 형태는 $f(x) = |x|$이며, 더 일반적으로는 $f(x) = |g(x)|$ 형태로 주어진 함수 $g(x)$의 절댓값으로 정의됩니다.

## 직관과 기하적 의미

$f(x) = |x|$의 그래프는 원점을 꼭짓점으로 하는 **V자 모양**입니다. $x \geq 0$에서는 $f(x) = x$로 직선이고, $x < 0$에서는 $f(x) = -x$로 역시 직선입니다. 

절댓값함수는 **수직 축에 대해 대칭**이라는 특징이 있습니다. 즉, $f(-x) = f(x)$이므로 짝함수입니다. 기하학적으로 절댓값은 수직선 위의 점이 원점으로부터 떨어진 거리를 나타냅니다.

$f(x) = |g(x)|$인 경우, $g(x) = 0$인 점에서 꺾이며, $g(x) > 0$ 구간에서는 $y = g(x)$를 따르고, $g(x) < 0$ 구간에서는 $g(x)$를 $x$축에 대해 대칭이동한 곡선을 따릅니다.

## 한 줄 예

$f(x) = |x - 2|$는 $x = 2$에서 꺾이며, $x \geq 2$일 때 $f(x) = x - 2$, $x < 2$일 때 $f(x) = 2 - x$입니다.
