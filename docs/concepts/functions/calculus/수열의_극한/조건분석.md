---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 함수
grade: 미적분
prerequisites: [docs/concepts/functions/calculus/수열의_극한.md]
enables: []
mastery: unknown
---

# 조건분석

## 정확한 진술

**조건분석**이란 명제나 정의에서 주어진 조건들 사이의 논리적 관계를 명확히 파악하는 것입니다. 특히 수열의 극한 정의에서는, 주어진 $\epsilon > 0$에 대응하는 자연수 $N$의 존재성을 확인하거나, 역으로 극한값의 조건을 추출하는 과정을 말합니다.

극한의 정의 "$\lim_{n \to \infty} a_n = L$"는 다음과 같이 표현됩니다:
$$\forall \epsilon > 0, \exists N \in \mathbb{N} \text{ such that } n > N \Rightarrow |a_n - L| < \epsilon$$

조건분석은 이 정의의 각 부분을 분리하여 검증하는 기법입니다:
- **$\epsilon$ 조건**: 아무리 작은 오차한계를 정해도
- **$N$ 조건**: 충분히 큰 항 번호를 정하면
- **수렴 조건**: 그 이후의 모든 항이 오차범위 안에 들어온다

## 직관·의미

수열의 극한을 정확히 증명할 때는 "$a_n$이 $L$에 가까워진다"는 직관을 형식화해야 합니다. 조건분석은 이 형식화 과정입니다. 

예를 들어 $a_n = \frac{1}{n}$이 $0$으로 수렴함을 보이려면:
- "임의의 $\epsilon > 0$을 받으면" → $\epsilon = 0.01$이든 $0.0001$이든 상관없다
- "$n > N$이면 $|a_n - 0| < \epsilon$이 되는 $N$을 찾을 수 있는가?" → $N = \lceil 1/\epsilon \rceil$로 잡으면 된다

이렇게 조건을 역으로 분석하면, "극한이 존재한다"는 추상적 개념이 구체적인 부등식 조건으로 변환됩니다.

## 한 줄 예

$a_n = \frac{2n + 1}{3n - 1}$일 때, $\lim_{n \to \infty} a_n = \frac{2}{3}$을 보이려면 "$|a_n - \frac{2}{3}| < \epsilon$이 되려면 $n$이 어느 정도 커야 하는가"를 분석합니다.
