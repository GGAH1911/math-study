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

# 기본 항등식

## 정확한 진술
임의의 실수 각 $\theta$에 대해 다음이 항상 성립합니다:
$$\sin^2\theta + \cos^2\theta = 1$$
이를 **기본 삼각함수 항등식** 또는 **피타고라스 항등식**이라 부릅니다. 이것은 모든 삼각함수 항등식의 출발점이 되는 가장 기본적인 식이며, 수능과 대학 입시 수학에서 가장 자주 나오는 항등식입니다.

## 직관/기하적 의미
단위원(반지름이 1인 원) 위의 임의의 점을 각도 $\theta$로 나타내면 좌표는 $(\cos\theta, \sin\theta)$입니다. 단위원의 정의에 의해 이 점은 항상 원점으로부터 거리가 정확히 1이므로, 거리 공식을 적용하면:
$$\sqrt{\cos^2\theta + \sin^2\theta} = 1$$
양변을 제곱하면 기본 항등식을 얻습니다. 따라서 이 항등식은 단위원의 기하학적 정의에서 자연스럽게 나오는 성질입니다. 모든 각도에서 항상 성립하는 이유가 바로 여기에 있습니다.

## 한 줄 예
$\theta = 60°$일 때, $\sin 60° = \frac{\sqrt{3}}{2}$, $\cos 60° = \frac{1}{2}$이므로:
$$\left(\frac{\sqrt{3}}{2}\right)^2 + \left(\frac{1}{2}\right)^2 = \frac{3}{4} + \frac{1}{4} = 1$$
검증: `sympy.sin(sympy.pi/3)**2 + sympy.cos(sympy.pi/3)**2` → `1`
