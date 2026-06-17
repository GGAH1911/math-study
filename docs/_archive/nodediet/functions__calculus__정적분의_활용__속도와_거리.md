---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 미적분
prerequisites: [docs/concepts/functions/calculus/정적분의_활용.md]
enables: []
mastery: unknown
---

# 속도와 거리

## 정확한 진술

시간 $t$에 대한 속도 함수 $v(t)$가 주어졌을 때, 시간 구간 $[a, b]$에서의 **변위(displacement)**는 $\int_a^b v(t) dt$이고, **거리(distance)**는 $\int_a^b |v(t)| dt$로 정의됩니다. 변위는 물체의 처음 위치와 끝 위치의 차이를 나타내고, 거리는 실제로 이동한 경로의 길이를 나타냅니다.

## 직관과 기하적 의미

속도를 시간에 대한 변화율로 생각하면, 미소 시간 $dt$ 동안 물체는 약 $v(t) dt$만큼 이동합니다. 이를 모두 누적하면 변위가 됩니다.

**핵심 차이는 방향성입니다.** 변위 $\int_a^b v(t) dt$는 음의 속도를 그대로 반영하므로 음수가 될 수 있습니다. 반면 거리 $\int_a^b |v(t)| dt$는 속도의 크기만 고려하므로 항상 0 이상입니다. 속도-시간 그래프에서 변위는 x축 위의 면적에서 x축 아래의 면적을 뺀 값이고, 거리는 모든 면적의 절댓값을 더한 값입니다.

## 예시

$v(t) = 2t - 4$ (m/s), $t \in [0, 3]$일 때:

$t=2$에서 속도가 0이 되고, $t \in [0, 2)$에서는 음의 속도, $t \in (2, 3]$에서는 양의 속도입니다.

**변위**: 
$$\int_0^3 (2t-4) dt = \left[t^2 - 4t\right]_0^3 = 9 - 12 = -3 \text{ m}$$

**거리**: 
$$\int_0^2 |2t-4| dt + \int_2^3 (2t-4) dt = \int_0^2 (4-2t) dt + \int_2^3 (2t-4) dt = 4 + 3 = 7 \text{ m}$$

물체는 최종적으로 3 m 뒤로 이동했지만(변위 −3 m), 실제 경로는 7 m입니다(거리 7 m). 

(`sympy.integrate(Abs(2*t - 4), (t, 0, 3))` → 7.0)
