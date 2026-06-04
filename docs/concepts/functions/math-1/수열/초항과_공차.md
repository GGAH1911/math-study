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

# 초항과 공차

## 정확한 진술

등차수열을 정의하는 두 가지 핵심 요소입니다.

**초항(首項)**: 수열의 첫 번째 항으로, 보통 $a_1$ 또는 $a$로 표기합니다.

**공차(公差)**: 등차수열에서 인접한 두 항의 차이로, $d$로 표기합니다. 즉, $d = a_{n+1} - a_n$ (모든 $n$에 대해 일정).

초항 $a$와 공차 $d$가 주어지면, 등차수열의 일반항은 다음과 같이 결정됩니다:
$$a_n = a + (n-1)d$$

## 직관과 의미

초항과 공차는 등차수열의 **완전한 정보**입니다. 이 두 수만 알면 수열의 모든 항을 계산할 수 있습니다.

- **초항 $a$**: 수열이 어디서 시작하는지를 결정
- **공차 $d$**: 수열이 얼마나 빠르게 증가(또는 감소)하는지를 결정

$d > 0$이면 증가수열, $d < 0$이면 감소수열, $d = 0$이면 상수수열입니다. 기하학적으로, 등차수열을 좌표평면에 점 $(n, a_n)$으로 나타내면 일직선 위에 배치됩니다.

## 예시

수열 $2, 5, 8, 11, \ldots$을 생각해봅시다.
- 초항: $a = 2$
- 공차: $d = 5 - 2 = 3$
- 일반항: $a_n = 2 + (n-1) \cdot 3 = 3n - 1$
- 검증: $a_1 = 2, a_2 = 5, a_3 = 8$ ✓

```
# sympy로 확인
from sympy import symbols, simplify
n = symbols('n')
a_n = 2 + (n-1)*3
print(simplify(a_n))  # 3*n - 1
```
