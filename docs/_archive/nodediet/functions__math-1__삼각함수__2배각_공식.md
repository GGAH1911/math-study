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

# 2배각 공식

## 정확한 진술

2배각 공식은 한 각의 2배에 대한 삼각함수값을 원래 각의 삼각함수값으로 나타내는 공식입니다.

$$\sin(2\theta) = 2\sin(\theta)\cos(\theta)$$

$$\cos(2\theta) = \cos^2(\theta) - \sin^2(\theta) = 2\cos^2(\theta) - 1 = 1 - 2\sin^2(\theta)$$

$$\tan(2\theta) = \frac{2\tan(\theta)}{1 - \tan^2(\theta)}$$

## 직관/기하적 의미

2배각 공식은 **덧셈공식에서 바로 유도**됩니다. 덧셈공식 $\sin(\alpha + \beta) = \sin(\alpha)\cos(\beta) + \cos(\alpha)\sin(\beta)$에서 $\alpha = \beta = \theta$로 놓으면 첫 번째 공식을 얻습니다. 코사인도 마찬가지로 $\cos(\theta + \theta) = \cos^2(\theta) - \sin^2(\theta)$입니다.

**기하학적으로**, 각을 2배로 늘릴 때 좌표가 어떻게 변하는지 보여줍니다. 원 위의 점 $(\cos\theta, \sin\theta)$에서 출발하면, 2배각 위치 $(\cos(2\theta), \sin(2\theta))$는 단순히 2배가 아니라 복잡한 관계를 가집니다.

**실무적 의미**: 삼각방정식을 풀거나 삼각함수 항등식을 증명할 때 차수를 낮출 수 있어 매우 유용합니다. 예를 들어 $\cos(2\theta) = 2\cos^2(\theta) - 1$을 정리하면 $\cos^2(\theta) = \frac{1 + \cos(2\theta)}{2}$가 되어 제곱을 제거할 수 있습니다.

## 한 줄 예

$\theta = 15°$일 때, $\sin(30°) = 2\sin(15°)\cos(15°)$를 확인하면 $\frac{1}{2} = 2 \cdot \frac{\sqrt{6}-\sqrt{2}}{4} \cdot \frac{\sqrt{6}+\sqrt{2}}{4} = 2 \cdot \frac{6-2}{16} = \frac{1}{2}$ ✓

(`sympy.simplify(2*sin(pi/12)*cos(pi/12) - sin(pi/6))` → `0`)
