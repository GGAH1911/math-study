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

# 곱의 조건

## 정확한 진술

등비수열에서 **세 개의 연속된 항이 만족하는 곱의 조건**은 다음과 같습니다.

등비수열 $\{a_n\}$의 공비를 $r$이라 할 때, 임의의 자연수 $n$에 대하여

$$a_{n-1} \cdot a_{n+1} = a_n^2$$

이 성립합니다. 더 일반적으로, 세 항 $a_p, a_q, a_r$이 $p + r = 2q$를 만족하면

$$a_p \cdot a_r = a_q^2$$

입니다.

## 직관과 의미

곱의 조건은 **등비수열의 기본 특성**을 가장 간결하게 표현합니다. 

첫 번째 항을 $a$, 공비를 $r$이라 하면 연속된 세 항은 $a, ar, ar^2$입니다. 이들의 관계를 보면:

$$ar \cdot ar = a \cdot ar^2$$

$$(ar)^2 = a \cdot ar^2$$

양변이 정확히 같으므로 조건이 성립합니다. 기하학적으로 이는 **중간 항이 양쪽 항의 기하평균**이라는 의미입니다. 즉, $a_n = \sqrt{a_{n-1} \cdot a_{n+1}}$ (단, 모든 항이 양수일 때).

이 성질은 세 수가 등비수열을 이루는지 **판별하는 도구**로도 유용합니다.

## 한 줄 예

세 수 $2, 6, 18$이 등비수열을 이루는지 확인: $6^2 = 36$이고 $2 \times 18 = 36$이므로 곱의 조건을 만족하여 공비 $3$인 등비수열입니다. (검증: `sympy.simplify(6**2 - 2*18)` = 0)
