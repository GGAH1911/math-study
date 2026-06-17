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

# 삼각함수 정의

## 정확한 진술

좌표평면의 원점을 중심으로 하고 반지름이 1인 **단위원** 위의 점을 생각하자. 원점에서 양의 $x$축 방향으로부터 반시계방향으로 측정한 각을 $\theta$라 하고, 각 $\theta$만큼 회전한 점의 좌표를 $(x, y)$라 하면 삼각함수는 다음과 같이 정의된다:

$$\cos \theta = x, \quad \sin \theta = y$$

$\cos \theta \neq 0$일 때:
$$\tan \theta = \frac{\sin \theta}{\cos \theta}$$

## 직관 및 기하적 의미

삼각함수는 **회전 각도와 좌표의 관계**를 나타낸다. 단위원 위의 점이 각도 $\theta$에 따라 어디에 위치하는지를 기술하는 것이다.

- $\cos \theta$: 점의 $x$좌표(수평 방향 거리)
- $\sin \theta$: 점의 $y$좌표(수직 방향 거리)  
- $\tan \theta$: 원점과 점을 잇는 직선의 기울기

각 $\theta$가 $0°$에서 $360°$로 변하면, 점은 단위원을 따라 한 바퀴 도는데, 이 과정에서 $\cos \theta$와 $\sin \theta$는 $-1$부터 $1$ 사이에서 주기적으로 반복된다. 또한 $\cos^2 \theta + \sin^2 \theta = 1$이라는 **기본 항등식**은 점이 항상 단위원 위에 있다는 기하학적 사실에서 나온다.

## 한 줄 예

$\theta = 60°$일 때 단위원 위의 점은 $\left(\frac{1}{2}, \frac{\sqrt{3}}{2}\right)$이므로 $\cos 60° = \frac{1}{2}$, $\sin 60° = \frac{\sqrt{3}}{2}$, $\tan 60° = \sqrt{3}$ (검증: `sympy.cos(sympy.pi/3), sympy.sin(sympy.pi/3)` → `(1/2, √3/2)`)
