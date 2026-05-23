---
sources: []
created: 2026-05-17
updated: 2026-05-17
concept_type: definition
domain: 도형
grade: 중3
prerequisites: [docs/concepts/geometry/middle-3/삼각비.md]
enables: []
mastery: unknown
---

# 주어진 삼각함수로부터 다른 삼각함수 계산

$\sin\theta, \cos\theta, \tan\theta$ 중 하나의 값이 주어졌을 때 나머지를 피타고라스 항등식과 정의로 결정하는 방법입니다. 중3 삼각비 단원의 표준 계산 기법입니다.

## 정의

예각 $\theta$ ($0 < \theta < 90^\circ$)에 대하여 다음 관계식을 사용합니다.
- $\sin^2 \theta + \cos^2 \theta = 1.$
- $\tan\theta = \dfrac{\sin\theta}{\cos\theta}.$

예각 범위에서는 모든 삼각함수 값이 양수이므로 부호 결정에 어려움이 없습니다. 직각삼각형 모델에서 한 비를 알면 나머지 변의 길이를 피타고라스 정리로 구해 다른 삼각비를 직접 읽을 수도 있습니다.

## 예시

예각 $\theta$에서 $\sin\theta = \dfrac{3}{5}$일 때 $\cos\theta, \tan\theta$를 구해 봅니다. 피타고라스 항등식으로
$$\cos^2\theta = 1 - \frac{9}{25} = \frac{16}{25} \implies \cos\theta = \frac{4}{5}.$$
또한
$$\tan\theta = \frac{\sin\theta}{\cos\theta} = \frac{3/5}{4/5} = \frac{3}{4}.$$

기하학적으로는 빗변이 $5$, 대변이 $3$인 직각삼각형의 인접변이 $4$로 결정되어 같은 결과를 얻습니다.

## 관련 개념

- [삼각비](docs/concepts/geometry/middle-3/삼각비.md)
