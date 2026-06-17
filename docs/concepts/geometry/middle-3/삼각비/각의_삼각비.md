---
unit: 삼각비
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 도형
grade: 중3
prerequisites: [docs/concepts/geometry/middle-2/도형의_성질.md]
enables: []
mastery: unknown
---

# 각의 삼각비

## 정확한 진술

직각삼각형에서 한 예각 $\theta$에 대해, **대변**(opposite)을 $a$, **인접변**(adjacent)을 $b$, **빗변**(hypotenuse)을 $c$라 할 때, 삼각비는 다음과 같이 정의합니다:

$$\sin \theta = \frac{a}{c}, \quad \cos \theta = \frac{b}{c}, \quad \tan \theta = \frac{a}{b}$$

더 일반적으로, 좌표평면의 원점을 중심으로 하는 각 $\theta$에 대해, 반지름이 1인 단위원 위의 점을 $(x, y)$라 하면:

$$\cos \theta = x, \quad \sin \theta = y, \quad \tan \theta = \frac{y}{x}$$

## 직관 및 기하적 의미

삼각비는 **각도와 길이의 관계**를 수량화합니다. 직각삼각형에서 한 각이 정해지면, 변의 길이의 비는 유일하게 결정되며, 이 비가 삼각비입니다. 

단위원으로 확장하면, 각 $\theta$에 따라 원 위의 점이 움직이고, 그 점의 $x$좌표가 $\cos \theta$, $y$좌표가 $\sin \theta$가 됩니다. 이를 통해 음의 각, $90°$를 넘는 각까지 삼각비를 자연스럽게 확장할 수 있습니다.

## 한 줄 예

$30°$일 때: $\sin 30° = \frac{1}{2}$, $\cos 30° = \frac{\sqrt{3}}{2}$, $\tan 30° = \frac{1}{\sqrt{3}}$ (검산: `import math; round(math.sin(math.radians(30)), 3)` → 0.5)
