---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 도형
grade: 고1
prerequisites: [docs/concepts/geometry/high-1/도형의_방정식.md]
enables: []
mastery: unknown
---

# 점의 대칭이동

## 정확한 진술

점 $P(x, y)$를 점 $A(a, b)$에 대해 **대칭이동**하면, 새로운 점 $P'(x', y')$의 좌표는 점 $A$가 선분 $PP'$의 중점이 되도록 결정됩니다.

중점 공식에 의해:
$$\frac{x + x'}{2} = a, \quad \frac{y + y'}{2} = b$$

이를 $x'$, $y'$에 대해 정리하면:
$$x' = 2a - x, \quad y' = 2b - y$$

## 직관/기하적 의미

점 $P$를 점 $A$에 대해 대칭이동한다는 것은 기하학적으로 **점 $A$를 중심으로 점 $P$를 $180°$ 회전**시키는 것과 같습니다. 점 $A$가 $P$와 $P'$ 사이의 정확한 중간에 위치하므로 두 점이 대칭 중심을 기준으로 완벽하게 균형을 이룹니다. 

특별히 원점 $O(0, 0)$에 대한 대칭이동은 매우 간단해져서 $x' = -x$, $y' = -y$가 되며, 이는 도형의 대칭성, 함수의 홀짝성을 판단할 때 자주 사용됩니다. 대칭이동은 도형 전체를 옮길 때도 필수이므로, 곡선의 방정식을 구할 때 기초가 되는 개념입니다.

## 한 줄 예

점 $P(3, 4)$를 점 $A(1, 2)$에 대해 대칭이동하면 $P'(2 \cdot 1 - 3, 2 \cdot 2 - 4) = P'(-1, 0)$입니다. (검증: `sympy.Point(3, 4).reflect(sympy.Point(1, 2))`)
