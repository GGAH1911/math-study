---
sources: []
created: 2026-05-17
updated: 2026-05-17
concept_type: definition
domain: 함수
grade: 수학1
prerequisites: [docs/concepts/functions/math-1/삼각함수.md]
enables: []
mastery: unknown
---

# sin/cos 관계식

$\sin\theta$와 $\cos\theta$ 사이의 기본 항등식과 변환식들입니다. 수학1 삼각함수 단원에서 삼각식 정리와 방정식 풀이의 핵심 도구입니다.

## 정의

임의의 실수 $\theta$에 대하여 다음이 성립합니다.
- 피타고라스 항등식: $\sin^2 \theta + \cos^2 \theta = 1.$
- 보각·여각·음각 공식:
  - $\sin(-\theta) = -\sin\theta,\ \cos(-\theta) = \cos\theta.$
  - $\sin\!\left(\dfrac{\pi}{2} - \theta\right) = \cos\theta,\ \cos\!\left(\dfrac{\pi}{2} - \theta\right) = \sin\theta.$
  - $\sin(\pi - \theta) = \sin\theta,\ \cos(\pi - \theta) = -\cos\theta.$

## 예시

$\sin\theta = \dfrac{3}{5}$이고 $\theta$가 제1사분면 각일 때 $\cos\theta$를 구해 봅니다. 피타고라스 항등식에 의해
$$\cos^2\theta = 1 - \sin^2\theta = 1 - \frac{9}{25} = \frac{16}{25}.$$
제1사분면에서 $\cos\theta > 0$이므로 $\cos\theta = \dfrac{4}{5}$입니다.

또한 $\sin 150^\circ = \sin(180^\circ - 30^\circ) = \sin 30^\circ = \dfrac{1}{2}$.

## 관련 개념

- [삼각함수의 기본성질](docs/concepts/functions/math-1/삼각함수/삼각함수의_성질.md)
- [삼각함수](docs/concepts/functions/math-1/삼각함수.md)
