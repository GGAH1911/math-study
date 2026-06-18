---
unit: 함수와 그래프
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 고1
prerequisites: [docs/concepts/functions/math-1/삼각함수.md]
enables: []
mastery: unknown
---

# 함수의 범위

## 정확한 진술

함수 $f: X \to Y$의 **범위(치역, range)**는 실제로 함수값으로 나타나는 모든 원소들의 집합입니다. 기호로는 다음과 같이 정의합니다:

$$\text{Range}(f) = \{ f(x) \mid x \in X \} = \{ y \in Y \mid y = f(x) \text{인 } x \in X \text{가 존재} \}$$

범위는 항상 치역(codomain) $Y$의 부분집합이며, 경우에 따라 $Y$와 같을 수도 있고 작을 수도 있습니다.

## 직관과 기하적 의미

함수의 그래프를 생각할 때, 범위는 **그래프에서 나타나는 모든 y좌표값들의 집합**입니다. 정의역의 모든 점을 그래프 위에 표시했을 때, 그 점들의 y좌표를 모두 모으면 범위가 됩니다.

예를 들어 $f(x) = x^2$ (정의역: 모든 실수)의 그래프는 포물선이고, 이 포물선에서 나타나는 y값은 $0$ 이상의 모든 수입니다. 따라서 범위는 $[0, \infty)$입니다. 선수 개념인 삼각함수에서 $f(x) = \sin x$는 정의역이 모든 실수지만 범위는 $[-1, 1]$로 제한됩니다.

## 한 줄 예

$f(x) = 2\cos x$의 범위는 $[-2, 2]$입니다. (왜냐하면 $\cos x \in [-1, 1]$이므로 $2\cos x \in [-2, 2]$)
