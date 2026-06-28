---
sources: []
created: 2026-06-28
updated: 2026-06-28
---

# 📝 00_PLANS — 계획 생애주기

> 분류: Operations / Planning. 무엇을 할지·진행상태의 SSOT. `TODO.md`(단일 파일) 대체.

## 폴더 = 생애주기 단계

| 폴더 | 의미 |
|---|---|
| `active/` | **지금 진행 중**. 착수한 작업. |
| `pending/` | 착수 대기. 다음에 할 후보(승인·입력 대기 포함). |
| `backlog/` | 장기·아이디어. 우선순위 낮거나 미정. |
| `completed/2026_MM/` | 완료. 월별 아카이브로 **이동**. |
| `reference/` | 상태 없는 영구 참조(로드맵·설계 SSOT·레거시 아카이브). |

## plan 문서 스키마 (`<TOPIC>_YYYY-MM-DD.md`)

```markdown
---
created: 2026-06-28
updated: 2026-06-28
status: ACTIVE        # ACTIVE | PENDING | BACKLOG | DONE
priority: P1          # P0 긴급 · P1 중요 · P2 일반
owner: "@insung + 튜터"
---
# <제목>
## Context — 왜·배경
## 실행 — 단계/체크박스
## 검증 — 완료 기준
```

## 규칙
- 착수 → `active/`. 완료 시 frontmatter `status: DONE` + **`completed/2026_MM/`로 이동**(폴더가 곧 상태).
- 작은 할 일은 plan 문서까지 안 만들고 해당 단계 폴더의 `00_*.md` 인덱스에 한 줄로 둬도 됨.
- 자동인덱스(`00_*.md`)는 `scripts/ensure-doc-indices.mjs`가 갱신 — 직접 편집한 설명은 보존됨.

---
## 🔗 지식망 연결
- **상위 분류**: [[index]]
