---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 수와식
grade: 수학1
prerequisites: [docs/concepts/algebra/math-1/지수와_로그.md]
enables: []
mastery: unknown
---

# 거듭제곱의 기본성질

## 정확한 진술

거듭제곱의 기본성질은 같은 밑을 가진 거듭제곱의 계산을 단순화하는 규칙들입니다. 실수 $a, b$와 실수 $m, n$에 대하여 다음이 성립합니다:

- **곱셈**: $a^m \cdot a^n = a^{m+n}$
- **나눗셈**: $a^m \div a^n = a^{m-n}$ (단, $a \neq 0$)
- **거듭제곱의 거듭제곱**: $(a^m)^n = a^{mn}$
- **곱의 거듭제곱**: $(ab)^n = a^n b^n$
- **분수의 거듭제곱**: $\left(\dfrac{a}{b}\right)^n = \dfrac{a^n}{b^n}$ (단, $b \neq 0$)

## 직관/기하적 의미

거듭제곱은 같은 수를 반복해서 곱하는 것입니다. 예를 들어 $a^3 = a \times a \times a$입니다. 

$a^2 \times a^3$을 계산할 때, 이는 $(a \times a) \times (a \times a \times a) = a \times a \times a \times a \times a = a^5$이므로 지수끼리 더합니다. **지수가 곱한 횟수를 세는 것**이므로, 곱셈에서는 지수를 더하고, 나눗셈에서는 뺍니다.

$(a^2)^3$은 $a^2$을 3번 곱한다는 뜻이므로 $a^2 \times a^2 \times a^2 = a^{2+2+2} = a^{2 \times 3}$입니다. 따라서 지수를 곱합니다.

## 한 줄 예

$2^3 \times 2^2 = 2^{3+2} = 2^5 = 32$ ✓ (또는 $8 \times 4 = 32$로 검산)

$(2^3)^2 = 2^{3 \times 2} = 2^6 = 64$ ✓

`sympy.expand_power_base(2**3 * 2**2)` → $2^5$
