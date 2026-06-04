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

# tan의 계산

## 정확한 진술

각의 탄젠트(tangent, 약칭 tan)는 다음과 같이 정의됩니다:

$$\tan\theta = \frac{\sin\theta}{\cos\theta}$$

직각삼각형에서 해석하면, 각 $\theta$에 대해:

$$\tan\theta = \frac{\text{대변}}{\text{인접변}}$$

단위원 위의 점 $(\cos\theta, \sin\theta)$에서는:

$$\tan\theta = \frac{y\text{좌표}}{x\text{좌표}}$$

단, $\cos\theta \neq 0$이어야 합니다 ($\theta \neq \frac{\pi}{2} + n\pi$, $n$은 정수).

## 직관/기하적 의미

탄젠트는 **기울기**를 나타냅니다. 원점에서 각 $\theta$만큼 회전한 직선이 $y$축과 이루는 기울기가 바로 $\tan\theta$입니다. 

직각삼각형에서 생각하면, 같은 각도라도 삼각형의 크기가 달라도 대변과 인접변의 **비율**은 항상 같습니다. 이 비율이 $\tan\theta$입니다. 예를 들어, 비탈진 경사로의 가파름 정도는 "높이 ÷ 수평거리"로 나타내는데, 이것이 바로 탄젠트입니다.

기하학적으로, 단위원 위의 점 $(\cos\theta, \sin\theta)$에서 수평축에 수직인 선을 긋고, 각 $\theta$를 나타내는 반직선이 그 선과 만나는 점의 $y$좌표가 $\tan\theta$입니다.

## 한 줄 예

$\tan 45° = 1$, $\tan 60° = \sqrt{3}$, $\tan 30° = \frac{1}{\sqrt{3}}$ 

```python
# sympy로 검산
import sympy as sp
print(sp.tan(sp.pi/4), sp.tan(sp.pi/3), sp.tan(sp.pi/6))  
# 출력: 1, sqrt(3), 1/sqrt(3)
```
