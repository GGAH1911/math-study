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

# 신뢰도

## 정확한 진술

신뢰도(confidence level)는 통계적 추론에서 신뢰구간이 모수를 포함할 확률을 나타내는 값입니다. 일반적으로 $95\%$ 또는 $99\%$ 같은 백분율로 표현되며, 대표본에서 모평균을 추정할 때 다음과 같이 정의됩니다.

신뢰도가 $100(1-\alpha)\%$인 신뢰구간은 표본으로부터 만든 구간이 모수를 포함할 확률이 $1-\alpha$라는 의미입니다. 예컨대 신뢰도 $95\%$ ($\alpha=0.05$)인 모평균 신뢰구간은 다음과 같이 구성됩니다:

$$\left[\overline{X} - z_{\alpha/2} \cdot \frac{\sigma}{\sqrt{n}}, \quad \overline{X} + z_{\alpha/2} \cdot \frac{\sigma}{\sqrt{n}}\right]$$

여기서 $\overline{X}$는 표본평균, $\sigma$는 모표준편차, $n$은 표본크기, $z_{\alpha/2}$는 표준정규분포의 상위 $\alpha/2$ 분위수입니다.

## 직관/기하적 의미

신뢰도는 **측정의 신뢰성**을 나타냅니다. 신뢰도 $95\%$라는 것은 "같은 방법으로 표본을 반복 추출해서 신뢰구간을 만드는 작업을 100번 하면, 그 중 약 95번은 만든 구간이 참값(모수)을 포함한다"는 뜻입니다. 

신뢰도가 높을수록 (예: $99\%$) 신뢰구간의 폭이 넓어지고, 신뢰도가 낮을수록 (예: $90\%$) 폭이 좁아집니다. 이는 높은 신뢰도로 참값을 잡아낼 확률을 높이려면, 더 넓은 범위를 제시해야 한다는 의미입니다.

## 한 줄 예

어떤 모집단의 모평균을 신뢰도 $95\%$로 추정한 구간이 $[48, 52]$라면, 같은 표본 추출 방법을 반복할 때 약 95번 중 참 모평균이 이 범위 안에 들어간다고 예상할 수 있습니다.
