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

# 삼각함수 기본항등식

## 정확한 진술

삼각함수 기본항등식은 각도 $\theta$에 관계없이 항상 참인 삼각함수 관계식입니다. 가장 중요한 항등식은 다음과 같습니다:

$$\sin^2\theta + \cos^2\theta = 1$$

이를 변형하면:
$$1 + \tan^2\theta = \sec^2\theta$$
$$1 + \cot^2\theta = \csc^2\theta$$

## 직관과 기하적 의미

단위원(반지름이 1인 원) 위의 점 $P(\cos\theta, \sin\theta)$를 생각해봅시다. 이 점은 원점으로부터 항상 거리 1만큼 떨어져 있습니다. 피타고라스 정리를 적용하면:

$$(\cos\theta)^2 + (\sin\theta)^2 = 1^2 = 1$$

따라서 $\sin^2\theta + \cos^2\theta = 1$이 모든 각도에서 성립합니다. 이것이 모든 기본항등식의 근원입니다.

다른 항등식들은 이를 정리한 것입니다. 예를 들어, 양변을 $\cos^2\theta$로 나누면:
$$\frac{\sin^2\theta}{\cos^2\theta} + 1 = \frac{1}{\cos^2\theta}$$
$$\tan^2\theta + 1 = \sec^2\theta$$

## 구체적인 예

$\theta = 45°$일 때: $\sin 45° = \cos 45° = \frac{\sqrt{2}}{2}$이므로

$$\left(\frac{\sqrt{2}}{2}\right)^2 + \left(\frac{\sqrt{2}}{2}\right)^2 = \frac{1}{2} + \frac{1}{2} = 1$$ ✓

또는 $\theta = 60°$일 때 $\sin 60° = \frac{\sqrt{3}}{2}$, $\cos 60° = \frac{1}{2}$이므로

$$\left(\frac{\sqrt{3}}{2}\right)^2 + \left(\frac{1}{2}\right)^2 = \frac{3}{4} + \frac{1}{4} = 1$$ ✓

이 항등식들은 단순한 공식이 아니라 삼각함수의 본질적 성질이므로, 모든 삼각함수 계산과 증명의 기초가 됩니다.
