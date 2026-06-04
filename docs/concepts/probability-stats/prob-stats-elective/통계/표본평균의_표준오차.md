---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 확률통계
grade: 확률과통계
prerequisites: [docs/concepts/probability-stats/prob-stats-elective/통계.md]
enables: []
mastery: unknown
---

# 표본평균의 표준오차

## 정확한 진술

표본평균의 표준오차(표준오차, Standard Error)는 표본평균의 표본분포에서의 표준편차입니다. 모집단의 표준편차를 $\sigma$, 표본 크기를 $n$이라 하면:

$$SE = \frac{\sigma}{\sqrt{n}}$$

모집단의 표준편차 $\sigma$가 미지수인 경우에는 표본표준편차 $s$로 추정합니다:

$$SE = \frac{s}{\sqrt{n}}$$

## 직관과 의미

표본 여러 개를 뽑아서 각 표본평균을 구하면, 이 표본평균들이 나타내는 분포(표본분포)를 생각할 수 있습니다. 표본평균의 표준오차는 이 표본분포가 얼마나 산포되어 있는지를 측정합니다.

**핵심 아이디어**: 표본 크기 $n$이 커질수록 표준오차는 $\frac{1}{\sqrt{n}}$에 비례해 감소합니다. 이는 표본을 크게 뽑을수록 표본평균이 모평균 주변에 더 밀집한다는 의미이며, 중심극한정리와 일관성 있게 작동합니다.

예를 들어, $n$을 4배로 늘리면 표준오차는 절반으로 줄어듭니다 ($\sqrt{4}=2$).

## 구체적 예

어떤 모집단에서 표준편차가 $\sigma=10$일 때, 표본 크기 $n=100$인 표본평균의 표준오차는:

$$SE = \frac{10}{\sqrt{100}} = \frac{10}{10} = 1$$

표본 크기를 $n=400$으로 늘리면:

$$SE = \frac{10}{\sqrt{400}} = \frac{10}{20} = 0.5$$

(검산: `import math; se1 = 10/math.sqrt(100); se2 = 10/math.sqrt(400); print(f'n=100: {se1}, n=400: {se2}')`)

표본평균이 신뢰도 95%에서 모평균으로부터 대략 $\pm 1.96 \times SE$ 범위에 있다는 신뢰구간 계산의 기초가 됩니다.
