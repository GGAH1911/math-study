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

# 평면 위의 정사영

공간의 점이나 도형을 어떤 평면에 수직으로 비추어 얻은 그림자 도형을 가리킵니다. 기하 공간도형 단원의 핵심 변환입니다.

## 정의

평면 $\pi$가 주어졌을 때, 공간의 점 $\mathrm{P}$의 $\pi$ 위로의 **정사영**은 $\mathrm{P}$에서 $\pi$에 내린 수선의 발 $\mathrm{P}'$입니다. 공간의 도형 $F$의 정사영은 $F$의 모든 점의 정사영의 집합입니다.

이때 도형 $F$가 평면 $\pi_1$ 위에 있고 $\pi_1$과 $\pi$가 이루는 각이 $\theta$이면, 도형의 정사영의 넓이는
$$S' = S \cos\theta$$
($S$는 원래 넓이)로 계산됩니다.

## 예시

점 $\mathrm{P}(2, 3, 5)$의 $xy$평면 위의 정사영은 $z$좌표를 $0$으로 만든 점 $(2, 3, 0)$입니다.

또한 정삼각형(넓이 $S = \sqrt{3}$)이 어떤 평면 위에 있고, 그 평면과 사영 평면이 $30^\circ$를 이루면 정사영의 넓이는 $\sqrt{3} \cos 30^\circ = \sqrt{3} \cdot \dfrac{\sqrt{3}}{2} = \dfrac{3}{2}$입니다.

## 관련 개념

- [공간벡터와 정사영](docs/concepts/geometry/geometry-elective/공간도형과_공간벡터/벡터의_정사영.md)
- [정사영의 넓이 계산](docs/concepts/geometry/geometry-elective/공간도형과_공간벡터/정사영의_넓이_계산.md)
- [공간도형과 공간벡터](docs/concepts/geometry/geometry-elective/공간도형과_공간벡터.md)
