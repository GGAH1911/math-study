---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 수학1
prerequisites: [docs/concepts/functions/삼각함수.md]
enables: []
mastery: unknown
---

# tan값

(개념 정의는 학습 시 채워집니다.)

## 정의

## 예시

## 관련 개념

## 본문

### 정확한 진술

각 $\theta$의 탄젠트값(tangent, 줄여서 tan)은 다음과 같이 정의됩니다:

$$\tan \theta = \frac{\sin \theta}{\cos \theta}$$

단위원 위의 점이 $(x, y) = (\cos \theta, \sin \theta)$일 때, **$\tan \theta = \frac{y}{x}$** 입니다. 직각삼각형에서는 **$\tan \theta = \frac{\text{대변}}{\text{인접변}}$** 로도 나타냅니다.

### 직관/기하적 의미

탄젠트는 각도의 "기울기"를 나타냅니다. 단위원 위에서 $\theta$만큼 회전한 점에서 원점으로 돌아오는 직선의 기울기가 바로 $\tan \theta$입니다. 

직각삼각형에서는 한 각이 커질수록 대변이 인접변보다 빨리 늘어나므로, $\tan \theta$는 각도가 증가할수록 빠르게 증가합니다. 특히 $\theta = 90°$에 가까워지면 $\tan \theta$는 무한히 커집니다 ($\cos 90° = 0$이기 때문). 

그래프는 쌍곡선 모양이며, $\theta = 90°, 270°$ 등에서 **수직 점근선**(그래프가 닿지 않는 직선)을 가집니다.

### 한 줄 예

- $\tan 45° = 1$ (직각이등변삼각형에서 대변 = 인접변)
- $\tan 60° = \sqrt{3}$ (정삼각형을 반으로 나눈 직각삼각형)
- $\tan 30° = \frac{1}{\sqrt{3}} = \frac{\sqrt{3}}{3}$

```python
# 검산: sympy.tan(sympy.pi/4), sympy.tan(sympy.pi/3), sympy.tan(sympy.pi/6)
```
