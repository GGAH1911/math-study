---
sources: []
created: 2026-05-17
updated: 2026-05-17
concept_type: definition
prerequisites: [docs/concepts/functions/math-1/삼각함수.md]
enables: []
mastery: unknown
auto_explained: true
---

# tan함수

각도 $\theta$에 대한 탄젠트 함수 $y = \tan\theta$는 사인과 코사인의 비로 정의된다.

$$\tan\theta = \frac{\sin\theta}{\cos\theta}$$

코사인이 분모에 있으므로 $\cos\theta = 0$이 되는 $\theta = \frac{\pi}{2} + n\pi$($n$은 정수)에서는 정의되지 않는다. 이 점들이 바로 $y = \tan\theta$의 점근선이 된다.

$\tan\theta$의 값의 범위는 모든 실수이며, 주기는 $\pi$다. 즉 $\tan(\theta + \pi) = \tan\theta$가 항상 성립한다. 함수의 그래프는 $x = \frac{\pi}{2} + n\pi$를 점근선으로 하여 아래에서 위로 단조 증가하는 곡선이 반복된다.

단위원으로 해석하면, 각도 $\theta$에 대응하는 단위원 위의 점 $(\cos\theta,\, \sin\theta)$에서 $y$좌표를 $x$좌표로 나눈 값이 $\tan\theta$다.

---

## 예시

**예시 1.** $\theta = \frac{\pi}{3}$일 때 탄젠트 값을 구하라.

$$\tan\frac{\pi}{3} = \frac{\sin\frac{\pi}{3}}{\cos\frac{\pi}{3}} = \frac{\frac{\sqrt{3}}{2}}{\frac{1}{2}} = \sqrt{3}$$

**예시 2.** $\theta = \frac{3\pi}{4}$일 때 탄젠트 값을 구하라.

$$\tan\frac{3\pi}{4} = \frac{\sin\frac{3\pi}{4}}{\cos\frac{3\pi}{4}} = \frac{\frac{\sqrt{2}}{2}}{-\frac{\sqrt{2}}{2}} = -1$$

2사분면에서는 $\sin\theta > 0$, $\cos\theta < 0$이므로 $\tan\theta < 0$임을 확인할 수 있다.

---

## 관련 개념

**삼각함수** 전체의 틀 안에서 $\tan\theta$는 $\sin\theta$, $\cos\theta$와 함께 삼각함수의 세 기둥 중 하나다. $\tan\theta$의 정의 자체가 $\sin$과 $\cos$의 비이므로, 두 함수를 먼저 이해하는 것이 필수다.

**삼각함수의 공식**과도 긴밀히 연결된다. 예를 들어 피타고라스 항등식 $\sin^2\theta + \cos^2\theta = 1$의 양변을 $\cos^2\theta$로 나누면

$$\tan^2\theta + 1 = \sec^2\theta$$

라는 항등식을 얻는다. 이 관계는 적분이나 방정식 풀이에서 자주 쓰인다.

**사인법칙·코사인법칙**을 배울 때도 삼각형의 각과 변 사이의 관계에서 탄젠트 값이 등장하며, 좌표 평면에서 직선의 기울기가 $\tan\theta$(단, $\theta$는 $x$축과의 각도)와 같다는 연결도 중요하다.
