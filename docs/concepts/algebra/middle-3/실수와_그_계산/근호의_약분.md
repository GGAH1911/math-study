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

# 근호의 약분

## 정확한 진술

제곱근 $\sqrt{n}$에서 근호 안의 완전제곱수를 밖으로 빼내는 과정을 **근호의 약분** 또는 **근호의 간단히 하기**라고 합니다. 일반적으로 양수 $n = m^2 \cdot k$ (단, $m$은 양의 정수, $k$는 완전제곱수를 인수로 갖지 않음)로 인수분해할 때, $\sqrt{n} = m\sqrt{k}$로 나타내며, 이를 **약분된 형태** 또는 **표준 형태**라 합니다. 계산 원리는 $\sqrt{a^2 b} = |a|\sqrt{b}$라는 제곱근의 성질에 기초합니다.

## 직관/기하적 의미

근호 약분은 제곱근을 통일된 표준 형태로 표현하는 규칙화 과정입니다. 예를 들어 $\sqrt{12}$와 $2\sqrt{3}$은 수학적으로 같지만, 약분된 형태인 $2\sqrt{3}$을 사용하면:
- 여러 제곱근을 더하거나 뺄 때 계산이 간단해집니다 ($\sqrt{12} + \sqrt{27} = 2\sqrt{3} + 3\sqrt{3} = 5\sqrt{3}$)
- 답이 명확하고 일관되므로 검증과 채점이 정확합니다
- 근호 안의 수가 작아져 계산 실수가 줄어듭니다
- 분모의 유리화 같은 후속 연산도 더 쉬워집니다

## 한 줄 예

$\sqrt{72}$를 약분하면, $72 = 36 \times 2 = 6^2 \times 2$이므로 $\sqrt{72} = 6\sqrt{2}$입니다. (`sympy.sqrt(72).simplify()` → $6\sqrt{2}$)
