---
sources: []
created: 2026-05-16
updated: 2026-05-16
auto_explained: true
concept_type: definition
grade: 미적분
domain: 함수
unit: 여러가지 함수의 극한과 연속
prerequisites: [docs/concepts/functions/calculus/여러가지함수의_극한.md]
enables: []
mastery: unknown
mastery_evidence: []
mastery_updated: 2026-05-16
review_state: new
next_review: 2026-05-17
---

# 자연상수 e

> **정의** · 미적분 · 단원: [여러가지 함수의 극한과 연속](/concepts/여러가지함수의_극한)

## 요약
$\lim_{x\to 0}(1+x)^{1/x}=e$의 정의

## 본문 (학습 시 채워짐)

### 정확한 진술

자연상수 $e$는 다음 극한으로 정의된다:
$$e = \lim_{x \to 0} (1+x)^{1/x}$$

또는 동치적으로:
$$e = \lim_{n \to \infty} \left(1 + \frac{1}{n}\right)^n$$

그 값은 약 $e \approx 2.71828\ldots$이며, 무리수이자 초월수이다.

### 직관과 의미

이 정의는 복리 이자의 개념에서 자연스럽게 나타난다. 연이율 100%에서 이자를 계산할 때, 한 해를 $n$등분하여 각 구간에 $(1/n)$배의 이율로 $n$번 복리 계산하면 총 $(1+1/n)^n$배가 된다. $n$을 무한히 크게 할수록 계산 주기가 짧아져 결국 연속으로 자라나는 상황에 도달하는데, 이 극한값이 $e$이다.

$e$의 중요성은 다음과 같다. 지수함수 $f(x) = e^x$는 미분해도 자기 자신이 되는 유일한 지수함수이다. 즉, $(e^x)' = e^x$이므로, 미적분학의 모든 영역에서 가장 자연스럽고 우아한 함수가 된다. 따라서 자연로그의 밑이자, 연속 성장을 설명하는 기본 도구이다.

### 한 줄 예제

몇 항 계산해 보면: $n=10$일 때 $(1+1/10)^{10} \approx 2.594$, $n=100$일 때 $\approx 2.705$, $n=1000$일 때 $\approx 2.7169$로 점점 $e$에 가까워진다.

```python
# sympy로 극한값 확인
from sympy import limit, Symbol, oo; n = Symbol('n'); limit((1 + 1/n)**n, n, oo)
# 출력: E (약 2.71828...)
```


## 학습 체크
- [ ] 정의/진술을 외울 수 있다
- [ ] 단순 예제를 풀 수 있다
- [ ] 응용 문제에서 인식할 수 있다
