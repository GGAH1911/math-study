---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 도형
grade: 중3
prerequisites: [docs/concepts/geometry/middle-3/삼각비.md]
enables: []
mastery: unknown
---

# 사분면 판정

## 정확한 진술

좌표평면을 $x$축과 $y$축으로 나누어 만든 네 개의 영역을 사분면(quadrant)이라 부른다. 제1사분면은 $x>0, y>0$, 제2사분면은 $x<0, y>0$, 제3사분면은 $x<0, y<0$, 제4사분면은 $x>0, y<0$이다. 주어진 각 $\theta$의 동경이 지나는 사분면을 판정하여 삼각함수 $\sin\theta, \cos\theta, \tan\theta$의 부호를 결정하는 과정을 사분면 판정이라 한다.

## 직관/기하적 의미

단위원 위의 점 $(\cos\theta, \sin\theta)$를 생각해 보자. 각 $\theta$의 동경이 단위원과 만나는 점이 어느 사분면에 있는지에 따라 $\cos\theta$(점의 $x$좌표)와 $\sin\theta$(점의 $y$좌표)의 부호가 결정된다. 따라서 사분면을 알면 삼각함수의 부호를 즉시 판단할 수 있다. 고등학교에서는 **ASTC 법칙**으로 암기한다: 제1사분면은 모든 값이 양(All), 제2사분면은 정현만 양(Sine), 제3사분면은 정접만 양(Tangent), 제4사분면은 코사인만 양(Cosine). $\tan\theta = \frac{\sin\theta}{\cos\theta}$이므로 제1, 3사분면에서 $\tan\theta>0$이고 제2, 4사분면에서 $\tan\theta<0$이다.

## 한 줄 예

$\theta = 150°$일 때, 동경은 제2사분면을 지나므로 $\sin 150° > 0$, $\cos 150° < 0$, $\tan 150° < 0$이다. (검증: $\sin 150° = 0.5$, $\cos 150° \approx -0.866$, $\tan 150° \approx -0.577$)
