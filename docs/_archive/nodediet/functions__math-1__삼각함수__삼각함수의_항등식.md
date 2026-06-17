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

# 삼각함수의 항등식

## 정확한 진술

삼각함수 항등식은 삼각함수를 포함한 식이 특정 범위의 모든 각도에서 성립하는 등식입니다. 고등학교 교육과정에서 다루는 기본 항등식은 다음과 같습니다.

**기본 항등식:**
$$\sin^2\theta + \cos^2\theta = 1$$

**덧셈 공식:**
$$\sin(\alpha + \beta) = \sin\alpha\cos\beta + \cos\alpha\sin\beta$$
$$\cos(\alpha + \beta) = \cos\alpha\cos\beta - \sin\alpha\sin\beta$$

**배각 공식:**
$$\sin2\theta = 2\sin\theta\cos\theta$$
$$\cos2\theta = \cos^2\theta - \sin^2\theta = 2\cos^2\theta - 1 = 1 - 2\sin^2\theta$$

**반각 공식:**
$$\sin^2\frac{\theta}{2} = \frac{1-\cos\theta}{2}, \quad \cos^2\frac{\theta}{2} = \frac{1+\cos\theta}{2}$$

## 직관/기하적 의미

단위원 위의 점 $(\cos\theta, \sin\theta)$를 생각해봅시다. 이 점은 항상 원점으로부터 거리 1이므로, 거리 공식에 의해 $\cos^2\theta + \sin^2\theta = 1$이 자동으로 따라옵니다. 

덧셈 공식은 두 각도를 더할 때 삼각함수의 값이 어떻게 변하는지 보여줍니다. 배각 공식은 이를 특수한 경우 $\alpha = \beta = \theta$로 단순화한 결과입니다. 이 항등식들은 삼각함수의 주기성과 대칭성이 만드는 필연적 관계를 나타냅니다.

## 한 줄 예

$\sin^2 30° + \cos^2 30° = \left(\frac{1}{2}\right)^2 + \left(\frac{\sqrt{3}}{2}\right)^2 = 1$ ✓
