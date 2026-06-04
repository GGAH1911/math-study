---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 미적분
prerequisites: [docs/concepts/functions/calculus/도함수의_활용_심화.md]
enables: []
mastery: unknown
---

# 극댓값

## 정확한 진술

함수 $f(x)$가 $x = a$를 포함하는 열린 구간에서 정의될 때, $a$ 근처의 모든 $x$에 대해 $f(x) \leq f(a)$가 성립하면 $f(a)$를 **극댓값(local maximum value)**이라 합니다. 이때 $x = a$를 극댓점이라 부릅니다. 미분가능한 함수에서 $x = a$가 극댓점이면, $f'(a) = 0$입니다.

## 직관/기하적 의미

극댓값은 함수 그래프에서 "봉우리"처럼 보이는 지점의 함숫값입니다. 전체 최댓값(최솟값)과 달리, **국소적으로만** 최대입니다. 예를 들어 해발 높이 그래프에서 여러 산봉우리가 있을 때, 각 봉우리의 높이가 극댓값입니다. 도함수의 관점에서는, $x = a$를 지날 때 $f'(x)$가 양수에서 음수로 변하면 $x = a$는 극댓점입니다. 즉, 함수가 증가하다가 감소로 바뀌는 경계입니다.

## 한 줄 예

$f(x) = -x^2 + 4x + 1$에서 $f'(x) = -2x + 4 = 0$일 때 $x = 2$이고, $f(2) = 5$가 극댓값입니다.

```
from sympy import symbols, diff, solve
x = symbols('x')
f = -x**2 + 4*x + 1
f_prime = diff(f, x)
critical = solve(f_prime, x)  # [2]
print(f"극댓값:", f.subs(x, critical[0]))  # 5
```

**주의**: 극댓값과 최댓값은 다릅니다. 또한 $f'(a) = 0$이어도 극값이 아닐 수 있습니다(변곡점). 극값 판정은 $f'$의 부호 변화를 확인해야 합니다.
