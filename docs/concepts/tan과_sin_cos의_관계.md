---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 수학1
prerequisites: [docs/concepts/삼각함수.md]
enables: []
mastery: unknown
---

# tan과 sin cos의 관계

(개념 정의는 학습 시 채워집니다.)

## 정의

## 예시

## 관련 개념

## 본문

### 정확한 진술

탄젠트는 사인을 코사인으로 나눈 값으로 정의됩니다.

$$\tan\theta = \frac{\sin\theta}{\cos\theta} \quad (\cos\theta \neq 0)$$

이 관계식은 모든 각도 $\theta$에 대해 성립하며, 정의역은 $\cos\theta = 0$인 $\theta = \frac{\pi}{2} + n\pi$ (단, $n$은 정수)를 제외한 모든 실수입니다.

### 직관과 기하적 의미

단위원 위의 점 $(\cos\theta, \sin\theta)$를 생각해봅시다. 직각삼각형에서 $\tan\theta$는 "밑변 대 높이"의 비율인데, 이를 삼각함수로 표현하면 높이인 $\sin\theta$를 밑변인 $\cos\theta$로 나누는 것입니다. 즉, 탄젠트는 각도가 $x$축(코사인)에서 얼마나 기울어져 있는지를 나타내는 기울기입니다. 이 정의 덕분에 $\sin$과 $\cos$의 모든 항등식을 이용하여 $\tan$의 성질을 유도할 수 있습니다.

### 한 줄 예

$\theta = \frac{\pi}{4}$일 때, $\sin\frac{\pi}{4} = \frac{\sqrt{2}}{2}$, $\cos\frac{\pi}{4} = \frac{\sqrt{2}}{2}$이므로 $\tan\frac{\pi}{4} = \frac{\sqrt{2}/2}{\sqrt{2}/2} = 1$입니다.

**검산:** `sympy: tan(pi/4)` = 1
