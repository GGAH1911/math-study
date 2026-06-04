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

# 삼각함수 항등식

## 정확한 진술

삼각함수 항등식은 각도 변수에 무관하게 모든 정의역 내 각도에서 항상 참인 삼각함수 식입니다. 대표적으로:

$$\sin^2 \theta + \cos^2 \theta = 1 \quad \text{(기본 항등식)}$$

$$\sin(\alpha + \beta) = \sin \alpha \cos \beta + \cos \alpha \sin \beta \quad \text{(덧셈 공식)}$$

$$\cos 2\theta = \cos^2 \theta - \sin^2 \theta \quad \text{(배각 공식)}$$

이들은 특정 각도만이 아니라, 정의된 범위의 **모든 각도**에서 동시에 성립하는 관계식입니다.

## 직관 및 기하적 의미

단위원(반지름 1인 원) 위의 점 $(\cos \theta, \sin \theta)$를 생각해봅시다. 이 점은 항상 원 위에 있으므로, 거리 공식에 의해 $\cos^2 \theta + \sin^2 \theta = 1$이 자동으로 성립합니다.

덧셈 공식 $\sin(\alpha + \beta)$는 두 회전 변환을 합성했을 때의 기하학적 효과를 식으로 나타낸 것입니다. 배각 공식 $\cos 2\theta = 2\cos^2 \theta - 1$은 각을 두 배로 늘렸을 때 코사인 값이 어떻게 변하는지를 보여줍니다.

## 언제 사용하는가

항등식은 복잡한 삼각함수 식을 간단히 정리하거나, 방정식을 풀 때 한 함수를 다른 함수로 바꾸는 데 필수입니다. 예를 들어 $\sin^2 \theta + 4\cos^2 \theta = 3$을 풀 때, 기본 항등식으로 $\sin^2 \theta = 1 - \cos^2 \theta$로 치환하면 $\cos^2 \theta$만의 식이 됩니다.

## 한 줄 예

$\tan \theta = \frac{\sin \theta}{\cos \theta}$는 탄젠트를 사인과 코사인으로 표현하는 항등식입니다.
