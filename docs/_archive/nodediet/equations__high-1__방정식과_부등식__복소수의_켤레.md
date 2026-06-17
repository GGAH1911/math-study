---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 방정식
grade: 고1
prerequisites: [docs/concepts/equations/high-1/방정식과_부등식.md]
enables: []
mastery: unknown
---

# 복소수의 켤레

## 정확한 진술

복소수 $z = a + bi$ (단, $a, b$는 실수)에 대하여 **켤레복소수(complex conjugate)**는 $\overline{z} = a - bi$로 정의됩니다. 즉, 허수 부분의 부호를 반대로 바꾼 복소수입니다.

특히:
- 실수 $a$에 대해 $\overline{a} = a$ (켤레는 자기 자신)
- 순허수 $bi$에 대해 $\overline{bi} = -bi$
- $\overline{\overline{z}} = z$ (두 번 켤레하면 원래대로)

## 직관과 기하적 의미

복소평면에서 복소수 $z = a + bi$는 점 $(a, b)$로 나타내고, 켤레복소수 $\overline{z} = a - bi$는 점 $(a, -b)$로 나타납니다. 이는 **실수축에 대한 대칭**입니다. 복소수를 뒤집듯이, 허수축 위의 성분만 음수로 바꾸는 조작이라고 생각할 수 있습니다.

켤레복소수는 다양한 성질을 만족합니다:
$$\overline{z_1 + z_2} = \overline{z_1} + \overline{z_2}, \quad \overline{z_1 \cdot z_2} = \overline{z_1} \cdot \overline{z_2}$$

또한 $z \cdot \overline{z} = (a+bi)(a-bi) = a^2 + b^2 = |z|^2$로, 복소수와 그 켤레의 곱은 항상 음이 아닌 실수입니다.

## 한 줄 예

$z = 3 + 2i$이면 $\overline{z} = 3 - 2i$이고, $z \cdot \overline{z} = 9 + 4 = 13$입니다.

**검산:** `sympy: z = 3 + 2*I; z * z.conjugate()`는 13을 반환합니다.
