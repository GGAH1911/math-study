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

# 삼각함수의 배각공식

## 정확한 진술

삼각함수의 배각공식(double angle formula)은 어떤 각 $\theta$에 대해 그 각의 2배인 $2\theta$의 삼각함수값을 $\theta$의 삼각함수값으로 나타내는 공식입니다.

$$\sin 2\theta = 2\sin\theta\cos\theta$$

$$\cos 2\theta = \cos^2\theta - \sin^2\theta = 2\cos^2\theta - 1 = 1 - 2\sin^2\theta$$

$$\tan 2\theta = \frac{2\tan\theta}{1-\tan^2\theta} \quad (\tan\theta \text{가 정의되고 } \tan^2\theta \neq 1)$$

## 직관과 의미

배각공식은 **덧셈공식의 특수한 경우**입니다. 덧셈공식 $\sin(\alpha + \beta) = \sin\alpha\cos\beta + \cos\alpha\sin\beta$에서 $\alpha = \beta = \theta$로 놓으면 $\sin 2\theta = 2\sin\theta\cos\theta$를 얻습니다. 

기하학적으로는 한 각을 두 번 더하면 어떻게 삼각함수값이 변하는지를 보여줍니다. 코사인 공식의 세 가지 형태는 문맥에 따라 활용도가 다른데, 특히 $\cos 2\theta = 2\cos^2\theta - 1$ 형태는 $\cos^2\theta$를 구할 때 유용하고, $\cos 2\theta = 1 - 2\sin^2\theta$ 형태는 $\sin^2\theta$를 구할 때 편합니다.

## 한 줄 예

$\sin 30° = \frac{1}{2}$일 때, $\sin 60°$를 배각공식으로 구하면: $\sin 60° = \sin(2 \times 30°) = 2\sin 30°\cos 30° = 2 \cdot \frac{1}{2} \cdot \frac{\sqrt{3}}{2} = \frac{\sqrt{3}}{2}$

(`sympy.simplify(2 * sp.sin(sp.pi/6) * sp.cos(sp.pi/6))` → $\frac{\sqrt{3}}{2}$)
