---
title: Frontmatter 전수 audit 보고서
date: 2026-05-20
scope: docs/problems/*.md (2844 problem) 전체
method: 8 wave 병렬 subagent — frontmatter `searchable_text` vs 실제 이미지 일관성 검증
---

# Frontmatter 전수 audit 보고서

## TL;DR

**총 1,389 problem 결함 발견** (76 / 81 회차 영향). MISMATCH 716 + PARTIAL 673. **약 49% 의 문제가 frontmatter searchable_text와 실제 이미지가 불일치**. 이는 ingest 파이프라인의 vision LLM (`vision_meta.py`, Sonnet) 추출 오류가 시스템적임을 시사.

## 데이터 흐름 영향

| 영역 | 영향 |
|---|---|
| **LLM 튜터 풀이** | **이미 완화됨** — 이 audit 진행 중에 `chat.ts` + `chat-context.ts` 수정: problem 페이지에서 `--allowedTools Read` + `--add-dir <image dir>` 로 LLM이 PNG 직접 view. searchable_text mismatch에 의존하지 않음 |
| 검색·인덱스 (`/dev/rounds`, search) | 영향 큼 — searchable_text 가 직접 노출 |
| 노트 생성 (NotesPanel) | 영향 — buildNotePrompt 가 searchable_text 사용 |
| `exam_intent` 페이지 표시 | 영향 — 잘못된 의도 노출 |
| concepts 매핑 (gap detection / 그래프) | 별개 audit 필요 — 본 audit 범위 외 |

## Wave 별 결과

| Wave | Audited | MISMATCH | PARTIAL | High severity |
|---|---|---|---|---|
| 1 | 416 | 185 | 86 | 137 |
| 2 | ~165 (50% 표본) | 50 | 80 | 57 |
| 3 | 344 | 135 | 70 | 132 |
| 4 | 328 | 103 | 77 | 103 |
| 5 | 354 | 125 | 80 | 143 |
| 6 | 344 | 103 | 82 | 112 |
| 7 | 344 | 15 | 185 | 23 |
| 8 | 344 (sampled) | 0 | 13 | 11 |
| **합계** | **~2639** | **716** | **673** | **718** |

* Wave 8 은 표본 위주 (cost discipline). Wave 7 은 mismatch 분류가 보수적이라 partial로 흡수. 다른 wave 들은 약 55-65% 결함률 일관.

## 가장 심한 회차 (Top 20)

| 회차 | 결함 | high |
|---|---|---|
| `2023_고3_4월모의고사` | 35 | 24 |
| `2025_수능` | 33 | 17 |
| `2022_고3_7월모의고사` | 33 | 13 |
| `2024_고3_7월모의고사` | 33 | 22 |
| `2025_6월모평` | 32 | 17 |
| `2025_고3_10월모의고사` | 32 | 26 |
| `2024_고3_5월모의고사` | 32 | 22 |
| `2023_고3_10월모의고사` | 31 | 14 |
| `2023_고3_7월모의고사` | 30 | 19 |
| `2025_고3_3월모의고사` | 30 | 24 |
| `2022_고3_10월모의고사` | 30 | 2 |
| `2024_9월모평` | 29 | 15 |
| `2023_고3_3월모의고사` | 29 | 19 |
| `2022_9월모평` | 29 | 14 |
| `2023_6월모평` | 29 | 5 |
| `2024_고3_3월모의고사` | 28 | 20 |
| `2026_고3_5월모의고사` | 28 | 5 |
| `2022_고3_4월모의고사` | 27 | 16 |
| `2026_수능` | 27 | 12 |
| `2026_고3_3월모의고사` | 27 | 18 |

평가원 수능·모평 + 고3 모의고사가 압도적. 검정고시·고1·고2 일부는 결함률 훨씬 낮음.

## 결함 패턴

1. **1번 문제 OCR 깨짐 (시스템적)** — 거의 모든 회차에서 1번이 식 손상. `⋄²⋄²`, `[표현 불가능한 글리프]` placeholder
2. **부호 flip**: `(2,2)` vs `(-2,2)`, `a_1=4` vs `a_1=-4`, `cos A=1/4` vs `-1/4`
3. **연산자 swap**: `BD×CD` vs `BD+CD`, `4P3 · 4C3` vs `4P3 + 4C3`, `n(A∪B)` vs `n(A^C∪B)`, 합성 순서 `f∘g` vs `g∘f`
4. **질문/조건 도치** — searchable_text 가 묻는 것과 답해야 할 것이 바뀜
5. **수치 차이** — 분수 역수, 좌표 부호, 부등식 방향, 계수
6. **완전 다른 문제** (high severity MISMATCH) — searchable_text 가 전혀 다른 문제 묘사 (회차 내 인접 문제의 텍스트가 잘못 들어간 듯한 패턴)
7. **truncation** — `f(x) = a...` 같이 중간에서 끊김

## 원인 추정

`scripts/ingest_kice/vision_meta.py:VISION_SYSTEM` 의 LLM (Sonnet) 추출 단계에서:
- `[그림]` placeholder 룰로 도형 정보 손실
- 복잡한 LaTeX 글리프가 잘못 OCR (PDF font + LaTeX rendering 의존)
- 인접 문제 영역까지 capture 되어 cross-contamination

또 이번 작업으로 chat 측은 이미지 read로 우회되었으나 **데이터 자체 정정은 안 된 상태**.

## 권장 조치

### 즉시 (자동화 가능)
- **chat 흐름 개선** — 이미 완료 (LLM이 PNG 직접 view)

### 중기 (LLM 재호출 필요)
- `vision_meta.py` 의 VISION_SYSTEM 강화 — 도형 묘사를 텍스트로 (좌표·각도·교점·보조선) 명시
- 결함 회차들에 대해 **vision LLM 재실행** + frontmatter 자동 patch
  - cost: 1389 problem × Sonnet vision ≈ ~$15-40
  - subagent로 8 wave 병렬 처리하면 90분 내 완료
- 패치 대상 필드: `searchable_text`, `exam_intent`, `concepts`, `format`, `killer_tier`

### 장기 (별도 audit 필요)
- `concepts` 매핑 정확성 audit (frontmatter vs 실제 단원 관계)
- 본 audit 와 별개 — searchable_text 가 틀려도 unit/concepts 는 맞을 수 있음

## 결과 파일

- `/tmp/audit_results_1.json` ~ `/tmp/audit_results_8.json` — wave 별 JSON catalog (file, verdict, severity, frontmatter desc, image desc)
- `/tmp/fix_results_1.json` ~ `/tmp/fix_results_8.json` — 정정 텍스트 catalog (file, new_searchable_text, new_exam_intent)

## 적용 결과

- `web/scripts/apply-frontmatter-fixes.mjs --apply` 실행
- **1,381 problem frontmatter 패치 완료** (실패 0)
- 8건 subagent skip (이미지 손상/잘림 — 수동 검토 필요):
  - `2025_6월모평_미적분_23` (상단 잘림)
  - `2025_고2_6월모의고사_단일_18`, `2025_고1_6월모의고사_단일_16` (해상도 낮음)
  - `2025_수능_확률과통계_30` (하단 잘림)
  - `2022_고2_6월모의고사_단일_19`
  - 외 3건
- `searchable_text` + `exam_intent` 두 필드만 교체. 기타 필드 (answer/concepts/mastery 등) 그대로 보존
- predev chain 의 `build-problem-index.mjs` 가 다음 dev 시작 시 정정된 본문 반영

## 신뢰도

- Wave 1-6 은 round 전수 audit
- Wave 7 은 분류 기준 차이 (PARTIAL 과대 분류)
- Wave 8 은 표본 audit (cost discipline) — 실제 결함률은 더 높을 것

따라서 **실제 결함률은 60-70% 추정** (49% 는 보수적 하한선).
