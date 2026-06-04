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

# 범위 구하기

## 정확한 진술

삼각함수의 **범위**(치역)란 함수가 취할 수 있는 모든 $y$ 값들의 집합입니다. 기본 삼각함수들의 범위는 다음과 같습니다:

- $\sin x$의 범위: $[-1, 1]$
- $\cos x$의 범위: $[-1, 1]$  
- $\tan x$의 범위: $\mathbb{R}$ (모든 실수)

일반적으로 $y = a\sin(bx + c) + d$ 형태일 때, 범위는 $[d - |a|, d + |a|]$가 됩니다.

## 직관/기하적 의미

단위원 위의 점 $(\cos\theta, \sin\theta)$을 생각해봅시다. $\theta$가 변할 때, 이 점은 반지름 1인 원 위를 한 바퀴 도는데, $x$ 좌표와 $y$ 좌표는 항상 $[-1, 1]$ 범위 내에 있습니다. 즉, $\sin x$와 $\cos x$는 절대로 $-1$보다 작거나 $1$보다 클 수 없습니다.

반면 $\tan x = \frac{\sin x}{\cos x}$는 분자와 분모 모두 제한되어 있지만, 분모가 0이 되는 지점(수직 점근선)을 제외한 모든 실수값을 가집니다.

계수가 붙으면 범위가 확대됩니다. $y = 2\sin x$이면 진동폭이 2배이므로 범위는 $[-2, 2]$가 되고, $y = \sin x + 3$이면 중심이 위로 3칸 이동하므로 범위는 $[2, 4]$가 됩니다.

## 한 줄 예

$y = 3\cos x - 2$의 범위를 구하면, $\cos x \in [-1, 1]$이므로 $3\cos x \in [-3, 3]$이고, 따라서 $y \in [-5, 1]$입니다. (검증: `sympy.simplify(-3-2), sympy.simplify(3-2)` → $-5, 1$)
