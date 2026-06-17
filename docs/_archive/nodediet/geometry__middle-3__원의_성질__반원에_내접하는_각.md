---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 도형
grade: 중3
prerequisites: [docs/concepts/geometry/middle-3/원의_성질.md]
enables: []
mastery: unknown
---

# 반원에 내접하는 각

## 정확한 진술
반원의 지름을 $AB$라 하고, 반원 위의 임의의 점을 $C$라 할 때 (단, $C \neq A, B$), 다음이 성립합니다:
$$\angle ACB = 90°$$

## 직관/기하적 의미
원의 중심을 $O$라 하면, 지름 $AB$에 대한 중심각은 $\angle AOB = 180°$입니다. 원주각의 성질에 의해, 같은 호에 대한 원주각은 중심각의 절반이므로:
$$\angle ACB = \frac{1}{2} \angle AOB = \frac{1}{2} \times 180° = 90°$$

이는 **탈레스의 정리**라고도 불리며, 원의 기본 성질 중 가장 우아한 결과입니다. 기하학적으로 반원은 특별한 대칭성을 가지고 있어서, 반원 위의 어떤 점에서 지름을 바라보든 항상 직각이 됩니다.

## 한 줄 예
좌표평면에서 원점 중심, 반지름 1인 원 위의 점 $A(-1, 0)$, $B(1, 0)$, $C(0, 1)$에 대해 $\vec{CA} \cdot \vec{CB} = (-1)·1 + (-1)·(-1) = 0$이므로 $\angle ACB = 90°$입니다. (검산: `sympy.symbols('x y'); solve([(x+1)**2 + y**2 - 1, (x-1)**2 + y**2 - 1, y])`)
