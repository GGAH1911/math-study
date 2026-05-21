---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 도형
grade: 중3
prerequisites: [docs/concepts/삼각비.md]
enables: []
mastery: unknown
---

# tan의 정의

(개념 정의는 학습 시 채워집니다.)

## 정의

## 예시

## 관련 개념

## 본문

### 정확한 진술

직각삼각형에서, 예각 $\theta$에 대해 $\tan \theta$는 다음과 같이 정의됩니다:

$$\tan \theta = \frac{\text{대변}}{\text{인접변}} = \frac{\sin \theta}{\cos \theta}$$

단위원 위의 관점에서, 각 $\theta$를 나타내는 동경이 단위원과 만나는 점을 $(\cos \theta, \sin \theta)$라 할 때, 탄젠트는 사인을 코사인으로 나눈 값입니다. 정의역은 $\cos \theta \neq 0$인 모든 실수, 즉 $\theta \neq \frac{\pi}{2} + n\pi$ (단, $n$은 정수)입니다.

### 직관과 기하적 의미

탄젠트는 **각도의 "가파름"** 또는 **기울기**를 나타냅니다. 원점을 지나고 각 $\theta$를 이루는 직선이 수평선과 이루는 기울기가 바로 $\tan \theta$입니다. 직관적으로:

- $\theta = 0°$: 수평이므로 $\tan 0° = 0$
- $\theta = 45°$: 대변과 인접변이 같으므로 $\tan 45° = 1$
- $\theta$가 $90°$에 가까워질 때: 기울기가 무한대로 커지므로 $\tan \theta \to \infty$

같은 각을 가진 모든 직각삼각형은 닮음이므로, 변의 길이 비율은 각도에만 의존합니다. 따라서 탄젠트는 각도를 입력받으면 항상 같은 기울기를 출력합니다.

### 한 줄 예

$\theta = 60°$일 때, $\tan 60° = \frac{\sin 60°}{\cos 60°} = \frac{\frac{\sqrt{3}}{2}}{\frac{1}{2}} = \sqrt{3}$ 
(`from sympy import sin, cos, pi, simplify; simplify(sin(pi/3)/cos(pi/3))` → $\sqrt{3}$)
