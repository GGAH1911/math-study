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

# 삼각함수의 기본항등식

## 정확한 진술

삼각함수의 기본항등식(fundamental trigonometric identities)은 $\sin\theta, \cos\theta, \tan\theta$ 등의 삼각함수 값들 사이에 항상 성립하는 관계식입니다. 가장 중요한 것들은 다음과 같습니다:

$$\sin^2\theta + \cos^2\theta = 1$$

$$\tan\theta = \frac{\sin\theta}{\cos\theta}$$

$$1 + \tan^2\theta = \sec^2\theta \quad (\cos\theta \neq 0)$$

$$1 + \cot^2\theta = \csc^2\theta \quad (\sin\theta \neq 0)$$

이 식들은 $\theta$의 크기에 관계없이 모든 실수 각에서 성립합니다(정의역 내에서).

## 직관 및 기하적 의미

단위원(반지름 1인 원) 위의 점 $P(\cos\theta, \sin\theta)$를 생각해봅시다. 이 점은 항상 단위원 위에 있으므로 원의 방정식 $x^2 + y^2 = 1$을 만족합니다. 따라서 $\cos^2\theta + \sin^2\theta = 1$이 자동으로 성립합니다.

$\tan\theta = \frac{\sin\theta}{\cos\theta}$는 좌표평면에서 원점과 점 $P$를 잇는 직선의 기울기입니다. 다른 항등식들도 이 기본 관계식에서 양변을 조작하여 얻어집니다. 예를 들어 $\sin^2\theta + \cos^2\theta = 1$을 $\cos^2\theta$로 나누면 $\tan^2\theta + 1 = \sec^2\theta$를 얻습니다.

## 한 줄 예

$\sin 30° = \frac{1}{2}, \cos 30° = \frac{\sqrt{3}}{2}$일 때, $\sin^2 30° + \cos^2 30° = \frac{1}{4} + \frac{3}{4} = 1$ ✓

**검산:** `sympy.simplify(sin(pi/6)**2 + cos(pi/6)**2)`는 1을 반환합니다.

## 활용 시 주의

정의역을 항상 확인하세요. 예를 들어 $\tan\theta$와 $\sec\theta$를 포함한 항등식은 $\cos\theta \neq 0$ (즉, $\theta \neq \frac{\pi}{2} + n\pi$)일 때만 성립합니다. 문제를 풀 때 이 조건을 빠뜨리면 오류가 발생할 수 있습니다.
