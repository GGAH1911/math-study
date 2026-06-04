---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 수학1
prerequisites: [docs/concepts/functions/math-1/수열.md]
enables: []
mastery: unknown
---

# 등비수열의 항 관계

## 정확한 진술

등비수열에서 **인접한 두 항의 비는 항상 같고**, 이 비를 **공비**(common ratio) $r$이라 합니다. 즉, 첫째 항을 $a_1$이라 할 때:

$$a_{n+1} = a_n \cdot r \quad \text{(모든 } n \geq 1\text{에서)}$$

따라서 $n$번째 항 $a_n$은:

$$a_n = a_1 \cdot r^{n-1}$$

더 일반적으로, 등비수열의 **지수 합 성질**이 있습니다. 지표 $p + q = m + n$을 만족하면:

$$a_p \cdot a_q = a_m \cdot a_n$$

특히 대칭적인 경우, 첫 항을 $a_1$, 마지막 항을 $a_n$이라 하면:

$$a_k \cdot a_{n+1-k} = a_1 \cdot a_n \quad (1 \leq k \leq n)$$

## 직관/기하적 의미

등비수열은 **곱셈으로 진행**하는 수열입니다. 매번 같은 배수 $r$를 곱하므로, 각 항은 이전 항의 기하학적 '배율'을 유지합니다. 예컨대 $r = 2$면 2배씩 증가하고, $0 < r < 1$이면 지수적으로 감소합니다.

지수 합 성질 $a_p \cdot a_q = a_m \cdot a_n$ (단, $p + q = m + n$)은 수열이 **로그 스케일에서 등차수열**이기 때문입니다. $\log a_n = \log a_1 + (n-1) \log r$이므로, 대수에서 보면 균등하게 배치된 형태죠.

## 한 줄 예

$1, 2, 4, 8, 16, \ldots$ (공비 $r=2$)에서 $a_2 \cdot a_4 = 2 \times 8 = 16 = 4 \times 4 = a_3 \cdot a_3$입니다.
$(\text{검증: } \text{sympy.solve를 이용하면 } a_1=1, r=2\text{일 때 } a_n=2^{n-1})$
