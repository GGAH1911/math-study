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

# 코사인 함수

## 정확한 진술

각 $\theta$에 대하여 단위원 위의 점을 $(\cos\theta, \sin\theta)$로 정의할 때, 코사인 함수는 이 점의 **x좌표**입니다. 즉,

$$\cos\theta = \text{(단위원 위 점의 x좌표)}$$

일반적으로는 반지름이 $r$인 원 위의 점에 대해 $\cos\theta = \frac{x}{r}$로 정의하며, 특히 직각삼각형에서는 **빗변 대 밑변의 비**를 나타냅니다:

$$\cos\theta = \frac{\text{밑변}}{\text{빗변}}$$

정의역은 모든 실수이고, 치역은 $[-1, 1]$이며, 주기는 $2\pi$입니다.

## 직관과 기하적 의미

단위원 위를 시계 반대 방향으로 원점에서 각도 $\theta$만큼 회전한 점을 생각해보세요. 이 점의 x좌표가 바로 $\cos\theta$입니다. $\theta$가 0에서 $2\pi$로 증가할 때, 점은 원을 한 바퀴 도는데, x좌표는 1에서 시작해 -1까지 내려갔다가 다시 1로 돌아옵니다.

직각삼각형 관점에서, 예각 $\theta$일 때 코사인은 빗변과 밑변(θ에 인접한 변)의 비이므로, 각이 커질수록 코사인값은 감소합니다. 이는 그래프에서 우파향 파동 형태로 나타나며, 특히 $\cos 0 = 1$, $\cos\frac{\pi}{2} = 0$, $\cos\pi = -1$의 대칭성이 특징입니다.

## 한 줄 예

$\cos 60° = \cos\frac{\pi}{3} = \frac{1}{2}$ (정확히 계산: `sympy.cos(sympy.pi/3)`)
