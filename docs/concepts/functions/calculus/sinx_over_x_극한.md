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
$\lim_{x\to 0}\sin x/x=1$

## 본문 (학습 시 채워짐)

### 정리의 진술

$x \to 0$일 때, 다음이 성립합니다.

$$\lim_{x \to 0} \frac{\sin x}{x} = 1$$

여기서 각 $x$는 라디안 단위입니다. 이는 삼각함수의 극한을 다루는 가장 기본적이면서도 중요한 정리입니다.

### 증명 스케치: 기하학적 방법

$0 < x < \frac{\pi}{2}$ 범위에서 단위원을 이용합니다. 원점 $O$, 원 위의 점 $A$, $B$를 생각할 때 중심각이 $x$라고 하면, 다음 부등식이 성립합니다.

$$\sin x < x < \tan x$$

이는 삼각형 $OAB$의 넓이 < 부채꼴의 넓이 < 삼각형 $OCD$의 넓이로 기하학적으로 명백합니다. 양변을 $\sin x > 0$으로 나누면:

$$1 < \frac{x}{\sin x} < \frac{1}{\cos x}$$

양변에 역수를 취하면 (부등호 방향 바뀜):

$$\cos x < \frac{\sin x}{x} < 1$$

$x \to 0^+$일 때, $\cos x \to 1$이고 $1 \to 1$이므로 **조임정리(squeeze theorem)**에 의해 $\frac{\sin x}{x} \to 1$입니다. $x \to 0^-$일 때는 $\sin(-x) = -\sin x$의 짝수·홀수 성질로 같은 결론을 얻습니다.

### 의의 및 응용

이 극한은 다른 삼각함수 극한을 계산하는 기초입니다. 예를 들어 $\lim_{x \to 0} \frac{\tan x}{x} = 1$, $\lim_{x \to 0} \frac{1 - \cos x}{x^2} = \frac{1}{2}$ 등이 모두 이 정리로부터 유도됩니다. 또한 **$\sin x$의 도함수가 $\cos x$임**을 증명하는 핵심 단계이기도 합니다. 수능에서 삼각함수 극한 계산 문제가 나올 때 이 정리를 직접 또는 간접적으로 활용하게 됩니다.

검산 예: $\lim_{x \to 0} \frac{\sin 2x}{x}$는 $\lim_{u \to 0} \frac{\sin u}{u/2} = 2\lim_{u \to 0} \frac{\sin u}{u} = 2 \cdot 1 = 2$입니다.


## 학습 체크
- [ ] 정의/진술을 외울 수 있다
- [ ] 단순 예제를 풀 수 있다
- [ ] 응용 문제에서 인식할 수 있다
