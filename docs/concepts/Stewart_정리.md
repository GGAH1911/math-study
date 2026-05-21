---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 도형
grade: 중3
prerequisites: [docs/concepts/원의_성질.md]
enables: []
mastery: unknown
---

# Stewart 정리

(개념 정의는 학습 시 채워집니다.)

## 정의

## 예시

## 관련 개념

## 본문

### 정확한 진술

삼각형 $ABC$에서 변 $BC$ 위의 한 점 $D$에 대해 선분 $AD$를 그었을 때, $AB = c$, $AC = b$, $BC = a$, $AD = d$이고, $BD = m$, $DC = n$이라 하면 다음 관계식이 성립합니다.

$$b^2 \cdot m + c^2 \cdot n = a(d^2 + mn)$$

이를 정리하면 cevian의 길이는:

$$d^2 = \frac{b^2 \cdot n + c^2 \cdot m}{a} - mn$$

---

### 직관과 기하적 의미

Stewart 정리는 삼각형의 한 꼭짓점에서 대변 위의 한 점으로 그은 선분(cevian)의 길이를 인접한 세 변의 길이로 표현하는 공식입니다. 코사인 법칙을 두 번 적용하면 유도할 수 있으며, **변의 길이만 알면 cevian의 길이를 계산할 수 있다**는 것이 핵심입니다.

특히 $D$가 $BC$의 중점(즉, $m = n = \frac{a}{2}$)일 때는 **중선의 길이 공식**이 되고, $D$가 각의 이등분선의 발일 때는 **각의 이등분선 길이 공식**이 됩니다. 이처럼 Stewart 정리는 삼각형 기하의 여러 상황을 통일적으로 다루는 도구입니다.

---

### 한 줄 예

$AB = 5$, $AC = 7$, $BC = 8$인 삼각형 $ABC$에서 $D$가 $BC$를 $3:5$로 내분하면 ($m = 3$, $n = 5$), $AD^2 = \frac{49 \cdot 3 + 25 \cdot 5}{8} - 15 = \frac{272}{8} - 15 = 19$이므로 $AD = \sqrt{19}$입니다.
```python
# sympy 검산: 49*3 + 25*5 = 8*(d**2 + 15) → d**2 = 19
from sympy import sqrt, solve
d_squared = (49*3 + 25*5)/8 - 15
print(f"d = {sqrt(d_squared)}")  # √19
```
