---
created: 2026-06-28
updated: 2026-06-28
status: DONE
priority: P2
owner: "@insung + 튜터"
---

# 500줄 초과 스크립트·컴포넌트 리팩토링

> 분류: Operations / Tech-debt. 2026-06-28 조사. **전수 리팩토링은 비추천** — 1순위(ChatPanel)만 별도
> 진행하고 나머지는 "그 파일 작업할 때 곁들이기".

## Context
500줄 초과 파일 16개 식별(스크립트 8 + 컴포넌트 8). 줄 수가 곧 복잡도는 아니므로, **분리 이득 > 리스크**인
것만 선별 진행한다. 콘텐츠 렌더러는 단일책임이라 보류.

### 식별 목록
**스크립트(py/mjs)**
| 줄 | 파일 | 판단 |
|---|---|---|
| 1674 | `scripts/ingest_kice/ingest_round.py` | ○ 단계별 모듈화 가치, 자주 안 건드림 → 만질 때 |
| 991 | `scripts/build_solution_cache.py` | ○ 단계 분리 가치, 작동 중 → 만질 때 |
| 718 | `scripts/ingest_kice/hancom_decode.py` | △ PUA 디코딩 단일목적 |
| 662·574·540 | `ingest_v2.py`·`bbox.py`·`web/scripts/extract_figures.py` | △ 만질 때 |
| 519·512 | `qa_concept_figures.mjs`·`gen_concept_figures.mjs` | △ 도식 생성/QA, 만질 때 |

**컴포넌트/lib(tsx/ts)**
| 줄 | 파일 | 판단 |
|---|---|---|
| **1972** | `web/src/components/ChatPanel.tsx` | ◎ **1순위** 저위험 추출 |
| 1238·1096 | `ConceptDAG.tsx`·`chat-context.ts` | △ chat-context는 프롬프트 SSOT(분할 신중) |
| 1087·1084·754 | `Geometry.tsx`·`Graph.tsx`·`Geometry3D.tsx` | ✗ 보류 — 단일책임 렌더러, 분리 이득<리스크 |
| 585·549 | `InkCanvas.tsx`·`AtlasMap.tsx` | △ InkCanvas는 메모리 함정 많음, 만질 때만 |

## 실행 (1순위 — ChatPanel.tsx). 회귀방지=베이스라인 캡처→순수이동→타입체커검증→체크포인트 커밋.

### ✅ Step 1·2 완료 (2026-06-28, 저위험·검증 green)
- [x] `lib/chat/types.ts`(ChatMessage) + `lib/chat/persistence.ts`(load/save·DB·상수). 커밋 `82f0cf2d3`.
- [x] `lib/chat/markdown.ts`(normalizeLlmMarkup·renderMarkdown·serializeFrag·latexFromSelection). 커밋 `c759f2a3a`.
- [x] 검증: astro check 0 errors·내 파일 경고0(베이스라인 일치)·컴파일 200·**런타임 스모크**(개념/문제 페이지 200·에러0).
- **결과**: ChatPanel **1972 → 1737줄** (235줄 추출, 동작 무변).

### ✅ Step 3·이후 완료 (2026-06-28) — 600줄 목표 달성
- [x] Message 클러스터(memo·MdSegment·QuotedChip·ErrorSegment·parseGraphSegments·sanitizeSvg·
      GraphicErrorBoundary·ChatModalState) → components/chat/Message.tsx. ChatScrollbar 분리.
- [x] 순수 검증 헬퍼(sanitizeForDisplay·evalArith·findArithErr·reconstructPastedMath) → verification.ts/markdown.ts.
- [x] BYOK 설정 패널 → ByokSettings.tsx, CSS → chat-styles.ts.
- [x] **send/검증 흐름(258줄) → useChatSend hook** (params destructure·deps 동일·body 무변).
- ★memo 함정 재평가: 회귀는 "부모가 prop을 *불안정 생성*"할 때 발생 — **컴포넌트를 그대로 옮기는 것은
  prop 생성 방식 불변이라 위험 낮음**. 순수 이동으로 진행, 타입체커+컴파일+런타임 스모크로 단계검증.

## ★최종 결과
ChatPanel **1972 → 582줄 (−70%)**. 모듈 8개:
- `lib/chat/`: types · persistence · markdown · verification · chat-styles · useChatSend
- `components/chat/`: Message · ChatScrollbar · ByokSettings

## 회귀 방지(전 단계 적용)
- 베이스라인 캡처(0 errors) → 순수이동 → 타입체커 배선검증 → 런타임 스모크 → 단계별 체크포인트 커밋(8개).
- ★1회 추출 실패(ByokSettings 경계 오매칭) **즉시 감지·revert** → 정확히 재추출(회귀방지 작동 실증).

## 잔여(별도)
- 컴포저(입력바) JSX는 props 25개라 추출 보류 — 결합 높아 ROI<리스크.
- 2~N순위 스크립트(ingest_round 등): 해당 작업 시 곁들이기. 렌더러: 보류.
