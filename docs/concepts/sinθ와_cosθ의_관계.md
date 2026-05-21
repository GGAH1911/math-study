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

# sinθ와 cosθ의 관계

(개념 정의는 학습 시 채워집니다.)

## 정의

## 예시

## 관련 개념

## 본문

### 정확한 진술

임의의 실수 $\theta$에 대해 다음 기본 항등식이 성립합니다.

$$\sin^2\theta + \cos^2\theta = 1$$

이를 단위원 항등식(fundamental trigonometric identity)이라고 부르며, 이로부터 파생되는 관계식들은 다음과 같습니다.

$$\tan\theta = \frac{\sin\theta}{\cos\theta} \quad (\cos\theta \neq 0)$$

$$1 + \tan^2\theta = \sec^2\theta \quad (\cos\theta \neq 0)$$

$$1 + \cot^2\theta = \csc^2\theta \quad (\sin\theta \neq 0)$$

### 직관/기하적 의미

좌표평면에서 원점을 중심으로 반지름이 1인 단위원 위의 점 $P(\cos\theta, \sin\theta)$를 생각해봅시다. 원점에서 점 $P$까지의 거리는 정의상 항상 1입니다. 거리 공식을 적용하면

$$\sqrt{\cos^2\theta + \sin^2\theta} = 1$$

양변을 제곱하면 $\sin^2\theta + \cos^2\theta = 1$을 얻습니다. 즉, 이 항등식은 **피타고라스 정리의 직접적인 결과**입니다. 

$\theta$가 변해도 점 $P$는 항상 단위원 위에 있으므로, 이 관계식은 모든 각도에서 성립합니다. 이는 $\sin\theta$와 $\cos\theta$가 독립적이지 않으며, 한쪽이 결정되면 다른 한쪽의 범위가 제한됨을 의미합니다.

### 한 줄 예

$\theta = 60°$일 때, $\sin 60° = \frac{\sqrt{3}}{2}$, $\cos 60° = \frac{1}{2}$이므로

$$\left(\frac{\sqrt{3}}{2}\right)^2 + \left(\frac{1}{2}\right)^2 = \frac{3}{4} + \frac{1}{4} = 1 \checkmark$$

`sympy.solve(sin(x)**2 + cos(x)**2 - 1, x)` → 모든 실수에서 항등식 성립
