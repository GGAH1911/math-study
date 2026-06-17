---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 확률통계
grade: 확률과통계
prerequisites: [docs/concepts/probability-stats/prob-stats-elective/경우의_수.md]
enables: []
mastery: unknown
---

# 조건부 배치

## 정확한 진술

조건부 배치는 전체 $n$개의 원소를 일렬로 배열할 때, 특정한 제약 조건을 만족하도록 배치하는 경우의 수를 구하는 것입니다. 조건의 예로는 "특정 원소가 정해진 위치에 와야 함", "특정 원소들이 서로 인접해야 함", "특정 원소가 특정 위치에 오면 안 됨" 등이 있습니다.

## 직관과 의미

제약이 없다면 $n$개를 배열하는 경우의 수는 $n!$입니다. 하지만 현실의 많은 문제에서는 조건이 붙습니다. 예를 들어 버스에 몇 명이 타고 내리는데 특정 사람이 특정 위치에 서야 한다거나, 책을 책장에 꽂는데 같은 시리즈 책들은 함께 놓아야 할 때처럼요.

조건부 배치를 푸는 핵심 전략은 두 가지입니다:
1. **조건을 고정하기**: 조건을 만족하는 상황을 먼저 확정하고, 나머지 원소들의 배치만 센다.
2. **조건이 있는 부분을 묶기**: 같은 그룹이 인접해야 할 때, 그 그룹을 하나의 단위로 취급한다.

이를 통해 복잡한 문제를 단계별로 분해하여 계산합니다.

## 한 줄 예

5개의 서로 다른 책을 책장에 놓는데, A책과 B책이 반드시 인접해야 한다면: A와 B를 하나로 묶으면 4개 단위를 배열 $→ 4!$ 가지, 묶음 내에서 A, B 순서 $→ 2!$ 가지 $→$ 총 $4! \times 2! = 48$가지입니다.

```python
# 검산: 직접 세기로 확인
from itertools import permutations
books = ['A', 'B', 'C', 'D', 'E']
count = sum(1 for perm in permutations(books) 
            if abs(perm.index('A') - perm.index('B')) == 1)
print(count)  # 48
```
