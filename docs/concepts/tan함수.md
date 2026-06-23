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

## 요약
각도 $\theta$에 대하여 $\tan\theta = \tfrac{\sin\theta}{\cos\theta}$로 정의되는 함수로, 주기가 $\pi$이며 점근선을 갖는 단조 증가 함수이다.

## 본문
각도 $\theta$에 대한 탄젠트 함수 $y = \tan\theta$는 사인과 코사인의 비로 정의된다. 즉, $\tan\theta = \tfrac{\sin\theta}{\cos\theta}$이다. 이때 코사인이 분모에 위치하므로 $\cos\theta = 0$이 되는 $\theta = \tfrac{\pi}{2} + n\pi$ ($n$은 정수)인 지점에서는 함수가 정의되지 않으며, 이 지점들은 함수의 점근선이 된다.

### 직관과 기하적 의미
단위원 위에서 각도 $\theta$에 대응하는 점의 좌표를 $(\cos\theta, \sin\theta)$라고 할 때, $\tan\theta$는 해당 점의 $y$좌표를 $x$좌표로 나눈 값과 같다. 이는 기하학적으로 단위원 위의 점을 지나는 동경의 기울기와 일치한다.

### 기본 성질
$\tan\theta$의 치역은 모든 실수이며, 주기는 $\pi$이다. 따라서 $\tan(\theta + \pi) = \tan\theta$가 모든 $\theta$에 대해 성립한다. 함수의 그래프는 $x = \tfrac{\pi}{2} + n\pi$를 점근선으로 하여 아래에서 위로 단조 증가하는 곡선이 반복되는 형태를 띤다.

**예시 1.** $\theta = \tfrac{\pi}{3}$일 때 탄젠트 값을 구하라.
$$\tan\frac{\pi}{3} = \frac{\sin\frac{\pi}{3}}{\cos\frac{\pi}{3}} = \frac{\frac{\sqrt{3}}{2}}{\frac{1}{2}} = \sqrt{3}$$

**예시 2.** $\theta = \tfrac{3\pi}{4}$일 때 탄젠트 값을 구하라.
$$\tan\frac{3\pi}{4} = \frac{\sin\frac{3\pi}{4}}{\cos\frac{3\pi}{4}} = \frac{\frac{\sqrt{2}}{2}}{-\frac{\sqrt{2}}{2}} = -1$$
이때 2사분면에서는 $\sin\theta > 0$이고 $\cos\theta < 0$이므로 $\tan\theta < 0$임을 알 수 있다.

## 학습 체크
- $\tan\theta$의 값이 정의되지 않는 $\theta$의 일반적인 형태는 무엇인가?
- $\tan\theta$의 주기와 그래프의 개형에 대해 설명할 수 있는가?
- 사분면에 따른 $\tan\theta$의 부호를 사인과 코사인의 부호를 이용하여 설명할 수 있는가?

## 관련 개념

**삼각함수** 전체의 틀 안에서 $\tan\theta$는 $\sin\theta$, $\cos\theta$와 함께 삼각함수의 세 기둥 중 하나다. $\tan\theta$의 정의 자체가 $\sin$과 $\cos$의 비이므로, 두 함수를 먼저 이해하는 것이 필수다.

**삼각함수의 공식**과도 긴밀히 연결된다. 예를 들어 피타고라스 항등식 $\sin^2\theta + \cos^2\theta = 1$의 양변을 $\cos^2\theta$로 나누면

$$\tan^2\theta + 1 = \sec^2\theta$$

라는 항등식을 얻는다. 이 관계는 적분이나 방정식 풀이에서 자주 쓰인다.

**사인법칙·코사인법칙**을 배울 때도 삼각형의 각과 변 사이의 관계에서 탄젠트 값이 등장하며, 좌표 평면에서 직선의 기울기가 $\tan\theta$(단, $\theta$는 $x$축과의 각도)와 같다는 연결도 중요하다.
