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

# 수직 직선

좌표평면에서 서로 직각으로 만나는 두 직선의 관계입니다. 고1 도형의 방정식 단원에서 직선의 위치 관계의 기본입니다.

## 정의

좌표평면 위의 두 직선이 서로 수직이라는 것은 두 직선이 만나는 점에서 $90^\circ$를 이룬다는 의미입니다. 두 직선의 기울기 관계는 다음과 같습니다.
- 두 직선의 기울기가 모두 존재하고 $m_1, m_2$이면, 수직 $\iff m_1 \cdot m_2 = -1$.
- 한 직선이 수평($y = c$)이면 수직인 직선은 수직선($x = k$).

법선벡터 관점에서는, 두 직선의 방향벡터의 내적이 $0$일 때 수직입니다.

## 예시

직선 $y = 2x + 1$에 수직이고 점 $(1, 3)$을 지나는 직선의 방정식을 구해 봅니다. 주어진 직선의 기울기는 $2$이므로 수직 직선의 기울기는 $-\dfrac{1}{2}$. 점-기울기 형식으로
$$y - 3 = -\frac{1}{2}(x - 1) \implies y = -\frac{1}{2}x + \frac{7}{2}.$$

## 관련 개념

- [수직선의 기울기 관계](docs/concepts/geometry/high-1/도형의_방정식/수직_조건.md)
- [수직인 두 직선](docs/concepts/geometry/high-1/도형의_방정식/수직_조건.md)
- [도형의 방정식](docs/concepts/geometry/high-1/도형의_방정식.md)
