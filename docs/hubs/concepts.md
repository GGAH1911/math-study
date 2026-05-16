---
sources: []
created: 2026-05-16
updated: 2026-05-16
hub_type: concepts
counts:
  total: 3
  by_type:
    definition: 3
    theorem: 0
    lemma: 0
    example: 0
  by_mastery:
    unknown: 2
    learning: 1
    proficient: 0
    mastered: 0
---

# 🧮 Concepts Hub

수학 개념의 1차 허브. 모든 concept spoke는 이곳에 등록되어야 하며 (D1), `concept_type` (D3)과 `mastery` (D13)별로 분류된다.

> **Librarian 주의**: 신규 concept 추가 시 `prerequisites`/`enables` 양방향 매칭(D12) + mastery 카운터 갱신(D13) + `docs/concept_graph.md` regeneration을 함께 수행.

---

## 📊 Mastery 분포

| Mastery | Count | Pages |
| :--- | ---: | :--- |
| 🟦 `mastered` | 0 | *(none yet)* |
| 🟩 `proficient` | 0 | *(none yet)* |
| 🟧 `learning` | 1 | [미분계수](../concepts/미분계수.md) |
| 🟥 `unknown` | 2 | [극한](../concepts/극한.md), [도함수](../concepts/도함수.md) |

---

## 📖 By Concept Type

### Definitions (정의)
| Page | Korean Name | Prerequisites | Mastery | Updated |
| :--- | :--- | :--- | :--- | :--- |
| [극한](../concepts/극한.md) | 극한 (Limit) | — (기초 노드) | 🟥 unknown | 2026-05-16 |
| [미분계수](../concepts/미분계수.md) | 미분계수 (Derivative at a point) | [극한](../concepts/극한.md) | 🟧 learning | 2026-05-16 |
| [도함수](../concepts/도함수.md) | 도함수 (Derivative function) | [미분계수](../concepts/미분계수.md) | 🟥 unknown | 2026-05-16 |

### Theorems (정리)
| Page | Korean Name | Prerequisites | Mastery | Updated |
| :--- | :--- | :--- | :--- | :--- |
| *(empty)* | | | | |

### Lemmas (보조정리)
| Page | Korean Name | Prerequisites | Mastery | Updated |
| :--- | :--- | :--- | :--- | :--- |
| *(empty)* | | | | |

### Examples (예제·반례)
| Page | Korean Name | Related Concepts | Mastery | Updated |
| :--- | :--- | :--- | :--- | :--- |
| *(empty)* | | | | |

---

## 🔗 Navigation
- **Concept Graph (Mermaid DAG)**: [../concept_graph.md](../concept_graph.md)
- **Problems Hub**: [problems.md](problems.md)
- **Mistakes Hub**: [mistakes.md](mistakes.md)
- **Tools Hub**: [tools.md](tools.md)
