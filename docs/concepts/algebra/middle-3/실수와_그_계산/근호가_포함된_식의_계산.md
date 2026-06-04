---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 수와식
grade: 중3
prerequisites: [docs/concepts/algebra/middle-3/실수와_그_계산.md]
enables: []
mastery: unknown
---

# 근호가 포함된 식의 계산

## 정확한 진술

근호가 포함된 식의 계산이란, 제곱근 기호 $\sqrt{\ }$를 포함한 식을 간단히 정리하거나 값을 구하는 과정입니다. 근호의 성질을 이용하여 다음과 같은 규칙을 적용합니다:

- **근호의 곱셈**: $\sqrt{a} \cdot \sqrt{b} = \sqrt{ab}$ (단, $a \geq 0, b \geq 0$)
- **근호의 나눗셈**: $\frac{\sqrt{a}}{\sqrt{b}} = \sqrt{\frac{a}{b}}$ (단, $a \geq 0, b > 0$)
- **제곱근의 정의**: $(\sqrt{a})^2 = a$ (단, $a \geq 0$)
- **근호 안의 완전제곱수 빼내기**: $\sqrt{12} = \sqrt{4 \cdot 3} = 2\sqrt{3}$

이들 규칙을 조합하여 근호가 포함된 식을 한 가지 표준 형태로 정리합니다.

## 직관과 의미

근호 안의 수가 클수록 계산이 복잡해지므로, 근호 안을 가능한 한 작은 수로 줄이는 것이 목표입니다. 예를 들어 $\sqrt{12}$를 $2\sqrt{3}$으로 정리하면, 근호 안의 3에는 완전제곱수가 없으므로 더 이상 간단히 할 수 없음을 알 수 있습니다. 이를 **기약근호 형태** 또는 **표준형**이라 부릅니다.

또한 분모에 근호가 있는 경우 분모를 유리화(근호를 없애는 과정)하여 정리합니다. 예: $\frac{1}{\sqrt{2}} = \frac{\sqrt{2}}{2}$

## 한 줄 예

$\sqrt{18} + \sqrt{8} = 3\sqrt{2} + 2\sqrt{2} = 5\sqrt{2}$ (sympy 검산: `sympy.simplify(sympy.sqrt(18) + sympy.sqrt(8))`)

근호가 포함된 식의 계산은 고등학교 전체에서 함수, 방정식, 적분 등 다양한 단원에서 자주 등장하므로 정확하고 빠르게 처리하는 능력이 중요합니다.
