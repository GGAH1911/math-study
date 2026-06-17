---
sources: []
created: 2026-05-17
updated: 2026-05-17
concept_type: definition
domain: 도형
grade: 고1
prerequisites: [docs/concepts/geometry/high-1/도형의_방정식.md]
enables: []
mastery: unknown
---

# 원의 중심과 반지름

원의 방정식에서 직접 또는 완전제곱식 변형을 통해 읽어내는 두 핵심 정보입니다. 고1 도형의 방정식 단원의 기본입니다.

## 정의

좌표평면 위 한 점 $\mathrm{C}(a, b)$로부터 거리가 $r$ ($r > 0$)인 점들의 집합을 **중심**이 $\mathrm{C}$이고 **반지름**이 $r$인 원이라 합니다. 표준형 방정식은
$$(x - a)^2 + (y - b)^2 = r^2.$$
일반형 $x^2 + y^2 + Dx + Ey + F = 0$이 원을 나타내려면 양변에 완전제곱식을 만들어
$$\left(x + \frac{D}{2}\right)^2 + \left(y + \frac{E}{2}\right)^2 = \frac{D^2 + E^2 - 4F}{4}$$
로 변형하고, 우변이 양수이어야 합니다. 이때 중심은 $\left(-\dfrac{D}{2}, -\dfrac{E}{2}\right)$, 반지름은 $\dfrac{\sqrt{D^2 + E^2 - 4F}}{2}$.

## 예시

방정식 $x^2 + y^2 - 4x + 6y - 12 = 0$의 중심과 반지름을 구해 봅니다. 완전제곱식으로
$$(x - 2)^2 + (y + 3)^2 = 4 + 9 + 12 = 25.$$
중심은 $(2, -3)$, 반지름은 $5$입니다.

## 관련 개념

- [원의 표준형 방정식](docs/concepts/geometry/high-1/도형의_방정식/원의_방정식.md)
- [원과 좌표축의 접선 조건](docs/concepts/geometry/high-1/도형의_방정식/원과_좌표축의_접선_조건.md)
- [도형의 방정식](docs/concepts/geometry/high-1/도형의_방정식.md)
