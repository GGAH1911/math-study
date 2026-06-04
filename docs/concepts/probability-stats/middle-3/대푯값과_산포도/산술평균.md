---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 확률통계
grade: 중3
prerequisites: [docs/concepts/probability-stats/middle-3/대푯값과_산포도.md]
enables: []
mastery: unknown
---

# 산술평균

## 정확한 진술

$n$개의 수 $x_1, x_2, \ldots, x_n$에 대하여, **산술평균**(arithmetic mean)은 다음과 같이 정의됩니다.

$$\bar{x} = \frac{x_1 + x_2 + \cdots + x_n}{n}$$

모든 데이터 값을 더한 후 개수로 나누어 얻는 값입니다. 일반적으로 $\bar{x}$ (엑스 바)로 표기합니다.

## 직관과 기하적 의미

산술평균은 **데이터의 전형적인 크기를 나타내는 대푯값**입니다. 수직선 위에 $n$개의 점을 표시했을 때, 이들의 무게중심이 정확히 산술평균입니다. 각 데이터가 같은 비중을 가질 때, 전체 데이터를 하나의 값으로 대표하는 가장 자연스러운 방식입니다.

산술평균은 다음과 같은 핵심 성질을 만족합니다:
- **합 보존**: 모든 데이터를 평균으로 바꾼 후 더하면, 원래의 합과 같습니다. 즉, $n \cdot \bar{x} = \sum_{i=1}^{n} x_i$
- **선형성**: 모든 데이터에 상수 $c$를 더하면 평균도 $c$만큼 증가하고, 상수 $k > 0$를 곱하면 평균도 $k$배가 됩니다.

## 한 줄 예

수학 시험 점수 $70, 80, 90$의 산술평균은 $\bar{x} = \frac{70 + 80 + 90}{3} = 80$점입니다.
