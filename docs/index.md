---
health: Optimal
pages: 44
orphans: 0
conflicts: 0
due_today: 0
mastery_unknown: 41
mastery_learning: 1
mastery_proficient: 0
mastery_mastered: 0
dag_integrity: ok
suggested_action: "Phase 1 골격 완료 (42 concept). 다음: 사용자가 학습 시작하는 단원의 정의/정리/예제 spoke 추가 (Phase 2). 권장 출발점: 이차방정식 단원."
last_updated: 2026-05-16
---

# 📚 Math Study — Knowledge Index

> Health: {{health}} | Pages: {{pages}} | Orphans: {{orphans}} | Conflicts: {{conflicts}} | Due Today: {{due_today}}
> Mastery: 🟥{{mastery_unknown}} 🟧{{mastery_learning}} 🟩{{mastery_proficient}} 🟦{{mastery_mastered}} | DAG: {{dag_integrity}}
> Suggested action: {{suggested_action}}

이 파일은 wiki의 마스터 카탈로그다. Librarian은 매 Ingest·Merge·Prune·Mastery 변동마다 헤더와 테이블을 갱신한다. Human은 이 파일 한 장으로 학습 상태 전체를 본다.

---

## 🗂️ Categories

### Concepts (개념)
*(타입별 상세 분류는 [hubs/concepts.md](hubs/concepts.md) 참조)*

| Page | concept_type | Mastery | Prerequisites | Sources |
| :--- | :--- | :--- | :--- | :--- |
| [극한](concepts/극한.md) | definition | 🟥 unknown | — | — |
| [미분계수](concepts/미분계수.md) | definition | 🟧 learning | [극한](concepts/극한.md) | — |
| [도함수](concepts/도함수.md) | definition | 🟥 unknown | [미분계수](concepts/미분계수.md) | — |

### Problems (기출 문제)
*(상태별 상세 분류는 [hubs/problems.md](hubs/problems.md) 참조)*

| Page | Source | Subject | Status | Concepts |
| :--- | :--- | :--- | :--- | :--- |
| [tangent_secant_smoke](problems/tangent_secant_smoke.md) | 자체-smoke 2026 | 미적분 | solved | [미분계수](concepts/미분계수.md) |

### Tools (학습 자료)
*(종류별 상세는 [hubs/tools.md](hubs/tools.md) 참조)*

| Page | Kind | Title | Useful For |
| :--- | :--- | :--- | :--- |
| *(empty)* | | | |

### Mistakes (오답노트)
*(error_type별 상세는 [hubs/mistakes.md](hubs/mistakes.md) 참조)*

| Page | error_type | Root Hole Concept | Revisit |
| :--- | :--- | :--- | :--- |
| [smoke_d14_gap_detection](mistakes/smoke_d14_gap_detection.md) | concept_gap | [극한](concepts/극한.md) | 2026-05-19 |

### Syntheses & Analyses (Q&A → 영구 페이지)
*(lifecycle.md의 Query & Promote 결과)*

| Page | Summary | Sources |
| :--- | :--- | :--- |
| *(empty)* | | |

---

## 🔗 Navigation
- **Hubs**: [Concepts](hubs/concepts.md) · [Problems](hubs/problems.md) · [Tools](hubs/tools.md) · [Mistakes](hubs/mistakes.md)
- **Concept Dependency Graph**: [concept_graph.md](concept_graph.md)
- **Learning Paths**: [paths/](paths/)
- **Operation Log**: [log.md](log.md)
- **Constitution**: [../agent.md](../agent.md) (Chapter 7 D1-D16 포함)
- **Lifecycle**: [../lifecycle.md](../lifecycle.md)
