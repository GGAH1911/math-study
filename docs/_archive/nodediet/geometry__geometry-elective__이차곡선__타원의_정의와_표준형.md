---
sources: []
created: 2026-05-17
updated: 2026-05-17
concept_type: definition
domain: 도형
grade: 기하
prerequisites: [docs/concepts/geometry/geometry-elective/이차곡선.md]
enables: []
mastery: unknown
---

# 타원의 정의와 표준형

두 정점에서의 거리의 합이 일정한 점들의 자취가 타원입니다. 기하 이차곡선 단원의 핵심 곡선입니다.

## 정의

평면의 서로 다른 두 정점 $\mathrm{F}, \mathrm{F}'$를 **초점**이라 하고, $\overline{\mathrm{FF}'} = 2c$라 합시다. 두 초점에서의 거리의 합이 $2a$ ($a > c > 0$)로 일정한 점 $\mathrm{P}$의 자취를 **타원**이라 합니다. 즉,
$$\overline{\mathrm{PF}} + \overline{\mathrm{PF}'} = 2a.$$

초점을 $x$축 위의 $\mathrm{F}(c, 0), \mathrm{F}'(-c, 0)$로 두고 $b^2 = a^2 - c^2$이라 하면 타원의 **표준형 방정식**은
$$\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1 \quad (a > b > 0).$$
장축의 길이는 $2a$, 단축의 길이는 $2b$이며 $c = \sqrt{a^2 - b^2}$.

## 예시

타원 $\dfrac{x^2}{25} + \dfrac{y^2}{9} = 1$의 주요 요소를 살펴봅니다. $a^2 = 25,\ b^2 = 9$이므로 $a = 5,\ b = 3$, $c = \sqrt{25 - 9} = 4$. 초점은 $(\pm 4, 0)$, 장축은 $10$, 단축은 $6$. 타원 위의 임의의 점 $\mathrm{P}$에 대해 $\overline{\mathrm{PF}} + \overline{\mathrm{PF}'} = 10$.

## 관련 개념

- [각의 이등분선의 성질](docs/concepts/geometry/geometry-elective/이차곡선/각의_이등분선의_성질.md)
- [이차곡선](docs/concepts/geometry/geometry-elective/이차곡선.md)
