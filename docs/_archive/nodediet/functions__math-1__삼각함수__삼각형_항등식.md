---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 수학1
prerequisites: [docs/concepts/functions/math-1/삼각함수.md]
enables: []
mastery: unknown
---

# 삼각형 항등식

## 정확한 진술

삼각형 항등식은 삼각형의 세 꼭짓점 $A$, $B$, $C$의 대변의 길이를 각각 $a$, $b$, $c$, 각의 크기를 각각 $A$, $B$, $C$라 할 때 항상 성립하는 관계식입니다. 가장 중요한 두 가지는 **정현 법칙**과 **코사인 법칙**입니다.

**정현 법칙(sine rule):**
$$\frac{a}{\sin A} = \frac{b}{\sin B} = \frac{c}{\sin C} = 2R$$
여기서 $R$은 삼각형의 외접원의 반지름입니다.

**코사인 법칙(cosine rule):**
$$a^2 = b^2 + c^2 - 2bc \cos A$$
$$b^2 = c^2 + a^2 - 2ca \cos B$$
$$c^2 = a^2 + b^2 - 2ab \cos C$$

## 직관/기하적 의미

정현 법칙은 "변의 길이와 그 대각의 사인값의 비율이 같다"는 의미입니다. 이는 삼각형의 크기가 클수록, 그리고 각이 클수록 대변이 길어지는 자연스러운 관계를 나타냅니다. 외접원의 반지름 $R$과의 관계는 호의 성질에서 비롯됩니다.

코사인 법칙은 **피타고라스 정리의 일반화**입니다. 직각삼각형이면 $\cos 90° = 0$이 되어 $a^2 = b^2 + c^2$이 되지만, 일반적인 삼각형에서는 각도에 따라 보정항 $-2bc \cos A$가 추가됩니다. 이는 두 변의 길이와 사잇각이 주어졌을 때 나머지 한 변을 구하는 핵심 도구입니다.

## 한 줄 예

변의 길이가 $a = 5$, $b = 6$, $c = 7$인 삼각형에서 코사인 법칙을 사용하면 $\cos A = \frac{b^2 + c^2 - a^2}{2bc} = \frac{36 + 49 - 25}{2 \cdot 6 \cdot 7} = \frac{5}{7}$입니다. (`sympy.symbols('A'); sympy.solve(25 - (36 + 49 - 2*6*7*sympy.cos(A)), A)` 로 검산 가능)
