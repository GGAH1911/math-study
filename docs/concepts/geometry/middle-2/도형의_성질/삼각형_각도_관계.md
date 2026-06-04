---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 도형
grade: 중2
prerequisites: [docs/concepts/geometry/middle-2/도형의_성질.md]
enables: []
mastery: unknown
---

# 삼각형 각도 관계

## 정확한 진술

삼각형의 세 내각의 합은 항상 $180°$입니다. 즉, 삼각형 $ABC$에서 $\angle A + \angle B + \angle C = 180°$가 성립합니다. 이는 모든 삼각형에 대해 불변인 성질로, 삼각형을 정의하는 가장 기본적인 각도 관계입니다.

## 직관/기하적 의미

한 꼭짓점에서 평행선을 그어보면 이 성질을 쉽게 이해할 수 있습니다. 삼각형 $ABC$의 꼭짓점 $A$에서 변 $BC$와 평행한 직선을 그으면, 이 직선 위에서 $\angle A$와 나머지 두 내각 $\angle B$, $\angle C$가 일렬로 펼쳐집니다. 평행선에 의해 만들어지는 엇각(또는 동위각) 관계에 의해 $\angle B + \angle C$의 합이 정확히 $\angle A$의 보각이 되므로, 세 각의 합은 $180°$(평각)가 됩니다.

이 성질로부터 삼각형의 **외각**도 정의됩니다. 어떤 삼각형의 한 꼭짓점에서의 외각은 그 꼭짓점을 제외한 두 내각의 합과 같습니다. 예를 들어, $\angle A$의 외각 $= \angle B + \angle C = 180° - \angle A$입니다.

## 한 줄 예

$\angle A = 50°$, $\angle B = 70°$인 삼각형에서 $\angle C = 180° - 50° - 70° = 60°$입니다. 

```
# sympy로 검산: solve(50 + 70 + C, C)[0] = 60
```
