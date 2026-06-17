---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 수학2
prerequisites: [docs/concepts/functions/math-2/함수의_극한과_연속.md]
enables: []
mastery: unknown
---

# 극한값의 존재 조건

## 정확한 진술

함수 $f(x)$가 $x = a$에서 극한값 $L$을 가질 **필요충분조건**은 다음과 같습니다:

임의의 $\varepsilon > 0$에 대해, $\delta > 0$이 존재하여
$$0 < |x - a| < \delta \implies |f(x) - L| < \varepsilon$$

이를 $\lim_{x \to a} f(x) = L$로 표기합니다.

더 실질적으로는, **극한이 존재한다** ⟺ **좌극한과 우극한이 모두 존재하고 같다**입니다:
$$\lim_{x \to a} f(x) = L \iff \lim_{x \to a^-} f(x) = \lim_{x \to a^+} f(x) = L$$

## 직관과 기하적 의미

$x$가 $a$에 가까워질 때, $f(x)$가 $L$에 가까워져야 한다는 뜻입니다. 좌극한은 $a$의 왼쪽에서 접근할 때, 우극한은 오른쪽에서 접근할 때를 봅니다. 극한이 존재하려면 **양쪽 방향에서 같은 값으로 수렴**해야 합니다.

예를 들어 절댓값 함수 $f(x) = \begin{cases} -x & (x < 0) \\ x & (x \geq 0) \end{cases}$는 $x = 0$에서:
- 좌극한: $\lim_{x \to 0^-} f(x) = 0$  
- 우극한: $\lim_{x \to 0^+} f(x) = 0$  
- 따라서 $\lim_{x \to 0} f(x) = 0$ (존재함)

반면 부호함수 $f(x) = \begin{cases} -1 & (x < 0) \\ 1 & (x > 0) \end{cases}$는 $x = 0$에서:
- 좌극한: $-1$, 우극한: $1$ → **서로 다르므로 극한이 존재하지 않음**

## 한 줄 예

$\lim_{x \to 2} (x^2 - 1) = 3$은 존재합니다. (좌극한 = 우극한 = 3)

```python
# 검증: 우극한과 좌극한 확인
import sympy as sp
x = sp.Symbol('x')
f = x**2 - 1
print(f"x→2에서 함수값:", f.subs(x, 2))  # 극한값 3
```
