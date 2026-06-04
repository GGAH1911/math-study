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

# 주기

## 정확한 진술

함수 $f(x)$가 **주기함수**(periodic function)라는 것은, 어떤 양수 $T$가 존재하여 모든 정의역 $x$에 대해

$$f(x + T) = f(x)$$

를 만족하는 경우를 말합니다. 이때 이 양수 $T$를 함수 $f$의 **주기**(period)라고 부릅니다. 주기 중 가장 작은 양수를 **기본 주기**(fundamental period)라 하며, 보통 "주기"라 하면 기본 주기를 의미합니다.

삼각함수의 기본 주기는:
- $\sin x$, $\cos x$: 기본 주기 $2\pi$
- $\tan x$, $\cot x$: 기본 주기 $\pi$  
- $\sin(ax)$, $\cos(ax)$ (단, $a \neq 0$): 기본 주기 $\dfrac{2\pi}{|a|}$

## 직관/기하적 의미

원 위를 도는 점을 상상해봅시다. 한 바퀴 도는 데 $2\pi$ 라디안이 필요하므로, 각도가 $2\pi$만큼 증가하면 정확히 같은 위치에서 같은 높이를 갖습니다. 따라서 $\sin(x + 2\pi) = \sin x$입니다.

**기하학적으로**, 주기함수의 그래프는 수평으로 주기만큼 평행이동해도 정확히 같은 모양을 반복합니다. 이는 물결파, 진동, 계절 변화처럼 자연에서 반복되는 현상을 수학으로 모델링할 때 본질적인 성질입니다.

주기 $T$가 작을수록 변화가 빠르고, 주기가 클수록 변화가 느립니다. 예를 들어 $\sin(2x)$는 $\sin x$보다 두 배 빠르게 진동하므로 기본 주기가 $\pi$로 더 짧습니다.

## 한 줄 예

$\sin\left(\dfrac{\pi}{4} + 2\pi\right) = \sin\left(\dfrac{\pi}{4}\right) = \dfrac{\sqrt{2}}{2}$는 $\sin x$가 주기 $2\pi$를 갖는 구체적 예입니다. (`sympy.simplify(sympy.sin(sympy.pi/4 + 2*sympy.pi) - sympy.sin(sympy.pi/4))` → `0`)
