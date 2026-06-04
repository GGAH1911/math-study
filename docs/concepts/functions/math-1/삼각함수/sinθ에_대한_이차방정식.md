---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 수학1
prerequisites: [docs/concepts/functions/math-1/삼각함수.md]
enables: []
mastery: unknown
---

# sinθ에 대한 이차방정식

## 정확한 진술

$\sin \theta$에 대한 이차방정식은 $\sin \theta$를 미지수 $t$로 보고 $at^2 + bt + c = 0$ 형태로 정리할 수 있는 삼각방정식입니다. 원래 형태로는 $a\sin^2 \theta + b\sin \theta + c = 0$ (단, $a \neq 0$)으로 나타납니다. 이 방정식을 풀기 위해 $t = \sin \theta$로 치환하면 일반 이차방정식 $at^2 + bt + c = 0$을 얻고, 근의 공식으로 $t$의 값을 구한 후 각 $t$ 값에 대해 $\sin \theta = t$를 푸는 방식으로 진행합니다.

## 직관/기하적 의미

$\sin \theta = t$로 치환하는 것은 **삼각함수 문제를 대수 문제로 변환**하는 핵심입니다. $\sin \theta$는 항상 $-1 \leq \sin \theta \leq 1$ 범위에 제한되므로, 이차방정식의 해 중 이 범위를 벗어나는 근은 버려져야 합니다. 기하적으로는 함수 $y = \sin \theta$의 그래프와 $y = t$ (직선)의 교점의 개수가 실제 해의 개수를 결정합니다.

## 한 줄 예

$\sin^2 \theta - 3\sin \theta + 2 = 0$을 풀면, $t = \sin \theta$로 놓았을 때 $t^2 - 3t + 2 = 0$이므로 $(t-1)(t-2) = 0$에서 $t = 1$ 또는 $t = 2$인데, $\sin \theta \leq 1$이므로 $\sin \theta = 1$만 유효하며 따라서 $\theta = \frac{\pi}{2} + 2\pi k$ (단, $k$는 정수)입니다. (`sympy.solve(sympy.sin(x)**2 - 3*sympy.sin(x) + 2, sympy.sin(x))` → `[1, 2]`)
