---
sources: []
created: 2026-05-16
updated: 2026-05-16
auto_explained: true
concept_type: theorem
grade: 미적분
domain: 함수
unit: 여러가지 함수의 극한과 연속
prerequisites: [docs/concepts/functions/calculus/여러가지함수의_극한.md]
enables: []
mastery: unknown
mastery_evidence: []
mastery_updated: 2026-05-16
review_state: new
next_review: 2026-05-17
---

# sinx over x 극한

> **정리** · 미적분 · 단원: [여러가지 함수의 극한과 연속](/concepts/여러가지함수의_극한)

## 요약
$\lim_{x\to 0}\tfrac{\sin x}{x}=1$임이 성립합니다.

## 본문
$x \to 0$일 때, 다음 극한값이 성립합니다.
$$\lim_{x \to 0} \frac{\sin x}{x} = 1$$
이때 $x$는 라디안 단위이며, 이는 삼각함수의 극한을 다루는 가장 기본적이면서도 중요한 정리입니다.

### 증명 스케치
$0 < x < \tfrac{\pi}{2}$ 범위에서 단위원을 이용하여 기하학적으로 증명합니다. 원점 $O$, 원 위의 점 $A$, $B$를 생각할 때 중심각이 $x$이면, 삼각형의 넓이와 부채꼴의 넓이 관계에 의해 $\sin x < x < \tan x$라는 부등식이 성립합니다. 양변을 $\sin x$로 나누면 $1 < \tfrac{x}{\sin x} < \tfrac{1}{\cos x}$가 되고, 다시 역수를 취하면 $\cos x < \tfrac{\sin x}{x} < 1$이 됩니다. $x \to 0^+$일 때 $\cos x$와 $1$이 모두 $1$로 수렴하므로, 조임정리에 의해 $\tfrac{\sin x}{x}$의 극한값은 $1$이 됩니다. $x \to 0^-$인 경우도 함수의 기함수 성질을 이용하면 동일한 결과를 얻습니다.

### 의의와 응용
이 극한은 $\lim_{x \to 0} \tfrac{\tan x}{x} = 1$이나 $\lim_{x \to 0} \tfrac{1 - \cos x}{x^2} = \tfrac{1}{2}$과 같은 다른 삼각함수의 극한을 유도하는 기초가 됩니다. 또한 $\sin x$의 도함수가 $\cos x$임을 증명하는 핵심 단계로 사용됩니다. 실전 문제에서는 $\lim_{x \to 0} \tfrac{\sin 2x}{x} = 2$와 같이 변형된 형태의 극한을 계산할 때 핵심적인 도구로 활용됩니다.

## 학습 체크
- $x \to 0$일 때 $\tfrac{\sin x}{x}$가 $1$로 수렴함을 기하학적 부등식으로 설명할 수 있는가?
- 이 정리를 이용하여 $\tfrac{\tan x}{x}$ 또는 $\tfrac{1-\cos x}{x^2}$의 극한값을 유도할 수 있는가?
- $\sin x$의 미분 계수를 구할 때 이 극한의 원리를 적용할 수 있는가?

## 관련 개념
- **여러가지 함수의 극한과 연속**: 삼각함수를 포함한 다양한 함수의 극한값을 구하는 과정에서 가장 기초가 되는 핵심 정리입니다.
