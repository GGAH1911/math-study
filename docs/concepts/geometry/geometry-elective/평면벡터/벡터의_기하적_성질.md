---
unit: 평면벡터
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 도형
grade: 기하
prerequisites: [docs/concepts/geometry/geometry-elective/공간도형과_공간벡터.md]
enables: []
mastery: unknown
---

# 벡터의 기하적 성질

## 정확한 진술

벡터의 **기하적 성질**은 벡터가 크기와 방향을 가진 물리적 대상으로서 만족하는 성질들입니다. 핵심은 다음 네 가지입니다:

1. **위치 독립성**: 벡터 $\vec{a}$는 시작점이 어디이든 크기와 방향이 같으면 같은 벡터입니다.
2. **크기**: $|\vec{a}| = \sqrt{a_1^2 + a_2^2}$ (평면) 또는 $|\vec{a}| = \sqrt{a_1^2 + a_2^2 + a_3^2}$ (공간)
3. **평행 조건**: $\vec{a} \parallel \vec{b} \Leftrightarrow \vec{a} = k\vec{b}$ (단, $k$는 0이 아닌 실수)
4. **직교 조건**: $\vec{a} \perp \vec{b} \Leftrightarrow \vec{a} \cdot \vec{b} = 0$

## 직관/기하적 의미

벡터는 단순한 수의 조합이 아니라 공간에서 화살표로 표현되는 기하학적 객체입니다. 같은 벡터라도 다양한 위치에서 그릴 수 있다는 것은 이동(평행이동)해도 본질이 바뀌지 않는다는 뜻입니다. 

벡터의 크기는 그 화살표의 길이이고, 방향은 화살표가 가리키는 방향입니다. 두 벡터가 평행하다는 것은 방향이 같거나 정반대라는 뜻이며, 직교한다는 것은 내적이 0이 되어 기하학적으로 수직(90°)을 이룬다는 뜻입니다. 이 성질들이 실제 기하 문제—거리 계산, 각도 구하기, 수직/평행 판정—을 푸는 도구가 됩니다.

## 한 줄 예

벡터 $\vec{a} = (3, 4)$의 크기는 $|\vec{a}| = \sqrt{3^2 + 4^2} = 5$이고, $\vec{b} = (-6, -8)$과는 $\vec{b} = -2\vec{a}$이므로 평행하며, $\vec{c} = (4, -3)$과는 $\vec{a} \cdot \vec{c} = 3 \times 4 + 4 \times (-3) = 0$이므로 직교합니다.
