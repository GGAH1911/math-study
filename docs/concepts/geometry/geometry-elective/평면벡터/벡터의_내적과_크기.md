---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 도형
grade: 기하
prerequisites: [docs/concepts/geometry/geometry-elective/평면벡터.md]
enables: []
mastery: unknown
---

# 벡터의 내적과 크기

## 정확한 진술

두 평면벡터 $\vec{a} = (a_1, a_2)$와 $\vec{b} = (b_1, b_2)$에 대해:

**내적(dot product)**은 다음과 같이 정의됩니다.
$$\vec{a} \cdot \vec{b} = a_1b_1 + a_2b_2$$

**벡터의 크기(magnitude)**는 원점에서의 거리로 정의됩니다.
$$|\vec{a}| = \sqrt{a_1^2 + a_2^2}$$

또한 내적은 두 벡터 사이의 각 $\theta$ ($0 \le \theta \le \pi$)를 이용하여 다음과 같이도 표현됩니다.
$$\vec{a} \cdot \vec{b} = |\vec{a}||\vec{b}|\cos\theta$$

## 직관/기하적 의미

**내적**은 한 벡터가 다른 벡터 방향으로 얼마나 강하게 작용하는지를 나타냅니다. 내적이 양수면 두 벡터가 같은 방향을 향하고, 음수면 반대 방향입니다. 내적이 0이면 두 벡터는 수직입니다.

직관적으로는 $\vec{a}$의 방향 위에 $\vec{b}$를 수직으로 내린 정사영(projection)의 길이에 $|\vec{a}|$를 곱한 값이 내적입니다. 내적을 계산하기 위해 각도를 알 필요가 없다는 점이 강력한 장점입니다.

**벡터의 크기**는 원점으로부터 그 벡터가 나타내는 점까지의 거리입니다. 피타고라스 정리를 좌표에 적용한 것으로 이해할 수 있습니다. 내적을 이용하면 $|\vec{a}| = \sqrt{\vec{a} \cdot \vec{a}}$로 표현됩니다.

## 한 줄 예

$\vec{a} = (3, 4)$, $\vec{b} = (1, 2)$일 때, 내적은 $\vec{a} \cdot \vec{b} = 3 \cdot 1 + 4 \cdot 2 = 11$이고, $\vec{a}$의 크기는 $|\vec{a}| = \sqrt{3^2 + 4^2} = 5$입니다.
