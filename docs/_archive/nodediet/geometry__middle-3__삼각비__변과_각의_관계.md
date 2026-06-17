---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 도형
grade: 중3
prerequisites: [docs/concepts/geometry/middle-3/삼각비.md]
enables: []
mastery: unknown
---

# 변과 각의 관계

## 정확한 진술

삼각형 $ABC$에서 변의 길이를 $a, b, c$ (각각 각 $A, B, C$의 대변), 외접원의 반지름을 $R$이라 할 때, **변과 각의 관계**는 다음 두 법칙으로 표현됩니다.

**사인 법칙(정현법칙):**
$$\frac{a}{\sin A} = \frac{b}{\sin B} = \frac{c}{\sin C} = 2R$$

**코사인 법칙(여현법칙):**
$$c^2 = a^2 + b^2 - 2ab\cos C$$

그리고 대칭적으로 $a^2 = b^2 + c^2 - 2bc\cos A$, $b^2 = a^2 + c^2 - 2ac\cos B$입니다.

## 직관/기하적 의미

사인 법칙은 각이 클수록 대변이 비례적으로 커진다는 의미입니다. 외접원 위의 현의 길이는 그 현이 대하는 중심각(또는 원주각)에 의해 결정되는데, 이를 삼각비로 표현한 것입니다.

코사인 법칙은 직각삼각형의 피타고라스 정리를 일반적인 삼각형으로 확장한 것입니다. 두 변 $a, b$와 그 사이의 각 $C$를 알면 나머지 변 $c$를 구할 수 있으며, 각이 직각이 되면 $\cos C = 0$이 되어 피타고라스 정리로 수렴합니다.

## 한 줄 예

변의 길이가 $a=5, b=7$이고 그 사이의 각이 $C=60°$인 삼각형에서, 세 번째 변은 $c^2 = 25 + 49 - 2(5)(7)\cos 60° = 74 - 35 = 39$이므로 $c = \sqrt{39}$입니다.

(검증: `from sympy import *; c_sq = 5**2 + 7**2 - 2*5*7*cos(pi/3); print(simplify(c_sq))` → 39)
