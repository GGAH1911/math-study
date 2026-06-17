---
sources: []
created: 2026-05-17
updated: 2026-05-17
concept_type: definition
domain: 도형
grade: 기하
prerequisites: [docs/concepts/geometry/geometry-elective/공간도형과_공간벡터.md]
enables: []
mastery: unknown
---

# 공간벡터와 정사영

공간의 벡터를 어떤 직선 또는 평면 위로 그림자처럼 떨어뜨린 결과를 가리키는 개념입니다. 기하 공간도형과 공간벡터 단원의 핵심 도구입니다.

## 정의

공간의 벡터 $\vec{u}$의 단위벡터 $\hat{n} = \dfrac{\vec{n}}{|\vec{n}|}$ 방향 직선 위로의 **정사영 벡터**는
$$\mathrm{proj}_{\vec{n}}\vec{u} = (\vec{u} \cdot \hat{n})\, \hat{n} = \frac{\vec{u} \cdot \vec{n}}{|\vec{n}|^2}\, \vec{n}.$$
- 한 점 $\mathrm{P}$의 평면 $\pi$ 위로의 정사영은 $\mathrm{P}$에서 평면에 내린 수선의 발.
- 도형의 정사영의 넓이는 원래 넓이의 $\cos\theta$배 ($\theta$는 도형의 평면과 사영 평면이 이루는 각).

## 예시

$\vec{u} = (3, 2, 1)$의 $\vec{n} = (1, 0, 0)$ 방향으로의 정사영을 구해 봅니다. $|\vec{n}|^2 = 1$, $\vec{u} \cdot \vec{n} = 3$이므로
$$\mathrm{proj}_{\vec{n}}\vec{u} = 3 \cdot (1, 0, 0) = (3, 0, 0).$$

또한 평면과 $60^\circ$를 이루는 도형의 넓이가 $4$이면 정사영의 넓이는 $4 \cos 60^\circ = 2$입니다.

## 관련 개념

- [평면 위의 정사영](docs/concepts/geometry/geometry-elective/공간도형과_공간벡터/정사영.md)
- [정사영의 넓이 계산](docs/concepts/geometry/geometry-elective/공간도형과_공간벡터/정사영의_넓이_계산.md)
- [공간도형과 공간벡터](docs/concepts/geometry/geometry-elective/공간도형과_공간벡터.md)
