---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 도형
grade: 중3
prerequisites: [docs/concepts/geometry/삼각비.md]
enables: []
mastery: unknown
---

# sin과 tan의 관계

(개념 정의는 학습 시 채워집니다.)

## 정의

## 예시

## 관련 개념

## 본문

### 정확한 진술

임의의 각 $\theta$에 대해 $\cos\theta \neq 0$일 때, 탄젠트는 다음과 같이 정의합니다:

$$\tan\theta = \frac{\sin\theta}{\cos\theta}$$

즉, 탄젠트는 사인을 코사인으로 나눈 값입니다. 이는 단지 계산의 편의가 아니라, 삼각함수의 본질적인 관계를 드러내는 정의입니다.

### 직관과 기하적 의미

직각삼각형에서 생각해 봅시다. 빗변의 길이를 1인 단위원 위의 각 $\theta$를 잡으면, $(\cos\theta, \sin\theta)$가 그 점의 좌표입니다. 

이때 $\tan\theta$는 원점에서 그 점으로 향하는 직선의 **기울기**입니다. 기울기 = $\frac{\text{높이}}{\text{밑변}} = \frac{\sin\theta}{\cos\theta}$이기 때문입니다. 

따라서 탄젠트를 "기울기의 삼각함수 버전"으로 이해하면, 각도가 커질수록 직선이 가파르면 탄젠트값도 커진다는 직관이 생깁니다.

### 한 줄 예

$\theta = 30°$일 때, $\sin 30° = \frac{1}{2}$, $\cos 30° = \frac{\sqrt{3}}{2}$이므로
$$\tan 30° = \frac{1/2}{\sqrt{3}/2} = \frac{1}{\sqrt{3}} = \frac{\sqrt{3}}{3}$$

(`sympy.simplify(sympy.sin(sympy.pi/6) / sympy.cos(sympy.pi/6))`)
