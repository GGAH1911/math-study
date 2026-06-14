# 📝 Operation Log

> Append-only. Every Ingest, Merge, Prune, and Lint operation is recorded here.
> Format: `## [YYYY-MM-DD] operation | Subject`

This file is the chronological backbone of the wiki. Even when pages are deleted (Pruned), the fact that they existed and why they were removed is preserved here. The Agent appends entries; the Human reads them to understand the wiki's evolution.

---

<!-- Entries below this line. Do not edit above. -->

## [2026-05-16] init | LWIP starter kit installed; customized for math-study (Chapter 7 D1-D16); seeded hubs: concepts/problems/tools/mistakes; concept graph + learning paths + graphics pipeline (KaTeX/Mermaid/matplotlib JIT + TikZ escape, no Manim) ready. Source: 대한민국 수능·평가원·교육청 기출. Postgres ingest는 후속 작업.

## [2026-05-16] smoke | seed | 3 concepts (극한 / 미분계수 / 도함수) — bidirectional prerequisites/enables, mastery 분포 unknown:2 / learning:1. concept_graph.md regenerated (DAG depth=2, 0 cycles, 0 broken edges).

## [2026-05-16] smoke | D11+D16 L3 | matplotlib JIT generated docs/assets/미분계수/tangent_secant.svg (+ .py). sympy verified f'(1) = 2 via 한계 정의 직접 평가.

## [2026-05-16] smoke | D14 | fake problem (tangent_secant_smoke) + fake mistake (smoke_d14_gap_detection) created. Gap Detection reverse-BFS correctly identified 극한 (depth=1, mastery=unknown) as root hole over 미분계수 (depth=0, mastery=learning).

## [2026-05-16] env | added project-local .venv (uv) with sympy 1.14 + matplotlib 3.10 + numpy 2.4; .gitignore + requirements.txt updated.

## [2026-05-16] init | web/ Astro 5 + Tailwind v4 + React + react-flow scaffold. 13 pages (dashboard / fullscreen DAG / concepts·problems·mistakes·tools list+detail / paths / log). docs/ remains SSOT; web reads via content collections. SVG assets synced docs/assets/ → public/assets/ at build. Initial production build = 2.2MB, all routes HTTP 200, KaTeX/Mermaid/SVG render verified.

## [2026-05-16] deploy | exposed dev server via Tailscale. Astro bound to 0.0.0.0:4321 (HTTP via tailnet IP). Added `tailscale serve --https=8443 http://127.0.0.1:4321` for HTTPS at tme-laptop.tailf47aa4.ts.net:8443. astro.config.mjs allowedHosts includes `.ts.net` and the specific tailnet. Existing :8000 serve preserved.

## [2026-05-16] curriculum | Phase 1 concept skeleton 시드. 중1(8)+중2(8)+중3(7)+고1(6)+수학Ⅰ(4)+수학Ⅱ(3)+확률통계(3) = 39 unit 노드 + 기존 미적분 정의 3개 = **42 nodes, 62 edges, 0 cycles**. 사용자 현재 위치(이차방정식)~목표(수학Ⅱ 미분)까지 한 그래프로 연결. agent.md D3에 `unit` concept_type + `grade`/`unit`/`subunit` frontmatter 추가. web 스키마/DAG/concepts list 모두 학년별 그루핑·필터 지원. 모두 mastery=unknown(미분계수만 learning) — D14 gap detection의 토양 마련.

## [2026-05-16] feat | 단원별 LLM 튜터 채팅창 추가. 각 `/concepts/<slug>` 페이지 하단에 ChatPanel(React island) 통합. 백엔드는 Astro hybrid SSR + Node adapter, `/api/chat`이 `claude -p --output-format stream-json --include-partial-messages`를 subprocess로 spawn해 토큰 스트리밍 SSE로 프록시. 시스템 프롬프트에 페이지 본문+선수 단원 학습목표+사용자 mastery 전체+Chapter 7 D1-D16 거버넌스 자동 주입(~3-5k 토큰, prompt cache hit 시 재사용). 모델은 haiku/sonnet 토글 가능. 대화 영구화 = localStorage(`math-study:chat:<slug>`), 좋은 답변은 'Promote' 버튼으로 `/api/promote` → `docs/syntheses/<date>_<slug>_<title>.md` 영구 wiki 노드로 저장(LWIP Query & Promote, lifecycle.md §Query-Promote). API key 별도 관리 불필요 — 사용자 Claude Code OAuth 그대로 사용.

## [2026-05-16] feat(chat) | 컨텍스트 가드 추가. system prompt에 "대화 범위" 섹션: 수학·시험전략·수학자 일화·학습법 허용, 연예인/게임/정치/개인상담 거부. 거부 형식 — 한 줄 + 단원 질문 제안. 검증: 점심 추천 거부, 가우스 일화 허용, 오답노트 정리법 허용, BTS 앨범 거부.

## [2026-05-17] feat | 학습 자료 링크 보강 3종 동시 적용. **(A)** 모든 unit 페이지 본문의 "다룰 정의/정리/예제" 글머리표를 자동으로 실제 spoke 파일 링크로 변환 — 125 bullets relinked across 49 units (휴리스틱: spoke의 label이 글머리표 시작에 매칭). 매칭 안 된 항목 커버용으로 **각 unit 페이지 끝에 "이 단원의 모든 노드" 섹션 추가** — 모든 정의/정리/예제 spoke를 type별로 그루핑 + 직접 링크. 49 unit 모두 업데이트. **(B)** Tools 시드 — 한국 수능 표준 자료 17개(자이스토리·마더텅·EBS 수능특강/완성·일품·쎈·정석·개념원리·현우진·정승제·한석원·EBSi·KICE·Desmos·GeoGebra·SymPy·오르비). 각 자료에 frontmatter(kind/title/url/concepts) + 요약·활용법·관련 단원 링크. D5 원칙(raw 텍스트 복붙 금지) 준수. **(C)** 진단 문제 concepts 매핑 보강 — 98개 diag_*.md의 `concepts:` 필드에 단원 unit + 모든 theorem spoke + 첫 definition + 첫 example 추가. D14 gap detection 정밀도 향상. tools hub 재생성 (kind별 그루핑 + URL 테이블). JIT audit ✅, 빌드 ✅.

## [2026-05-16] curriculum(complete) | **Phase 1+2+3 완전 시드** (사용자 "남은 모든 단계 다 실행" 요청). 추가 작업:
  - **선택과목 단원 추가** (Phase 1 확장): 미적분 7개(수열의극한, 여러가지함수의극한·미분, 합성함수의미분, 도함수의활용심화, 여러가지적분법, 정적분의활용) + 기하 3개(이차곡선, 평면벡터, 공간도형과공간벡터) = **49 units 총**
  - **Phase 2 spokes**: 모든 단원의 정의/정리/예제 시드. 정의 115 + 정리 102 + 예제 124 = **341 spokes**. 본문은 stub (페이지 채팅에서 학습 시 채움).
  - **Phase 3 진단 problems**: 단원당 2개씩, 자체-진단 출처로 **98 problem stubs** (단원당 2 × 49 + 기존 smoke 1 = 99). 본문은 평가원 기출 매핑 또는 자체 출제로 학습 시 채움.
  - **grade enum 확장**: `미적분`, `기하` 추가 (web schema + ConceptDAG + concepts list).
  - **hub 자동 재생성**: hubs/concepts.md = 390 노드를 학년별·타입별로 정리. hubs/problems.md = 49 단원별로 그루핑.
  - **JIT audit 통과**: ✅ 0-Isolation (490 spokes 모두 hub 또는 concept 페이지에서 inbound), ✅ DAG 양방향 매칭 (417 edges), ✅ Acyclic.
  - 결과 **390 concept nodes + 99 problem nodes + 1 mistake**. Mastery 모두 unknown(미분계수 learning만 예외). D14 gap detection의 토양이 한국 수능 전 범위로 깔림.

## [2026-05-20] promote | chat → synthesis: "그럼 방금 주사위 3가지 조건은 간단하니까 해보자 
3+2+1-1-0-0+0=5 
이게 맞아?" from 확률_중2

## [2026-05-22] restructure | LWIP shutdown — concepts → docs/concepts/<domain>/ (2786 files, 7 domains: functions/geometry/probability-stats/algebra/equations/logic/uncategorized), problems → docs/problems/<year>/<round>/ (2844 files, 81 rounds, 7 years). Sub-hub auto-gen (build-concept-hubs + build-problem-hubs). URL path-aware (`/concepts/algebra/근의_공식`, `/problems/2025/수능/2025_수능_미적분_30`). audit-lwip emits entropy=0 (isolated 5265→0, missing fm 4→0, flat hard 0, congested hard 0). Dashboard HealthCards shows entropy live.

## [2026-05-22] promote | chat → synthesis: "정리 및 평가문제" from logic/high-1/집합과_명제/논리

## [2026-05-22] promote | chat → synthesis: "지금 까지 학습한거 총정리 해줘. 나한테 특화해서" from logic/high-1/집합과_명제/논리

## [2026-05-22] promote | chat → synthesis: "[학습 노트 요청] 위 노트를 절반 길이로 다시 정리해줘. 같은 4섹션 구조는 유지." from algebra/math-1/지수와_로그/n제곱근의_정의

## [2026-05-23] promote | chat → synthesis: "[학습 노트 요청] "logic/high-1/집합과_명제/논리" 페이지에서 지금까지 한 대화를 정리해 학습 " from logic/high-1/집합과_명제/논리

## [2026-06-02] prune | 검정고시(고졸) 전체 제거 — 260문제 / 13회차(2020~2026 고졸 1·2회). 삭제: docs/problems/*/고졸_*회/ (260 md), web/public/problem-images/*고졸* (260), db/solutions/*고졸* (243 검증기), verified-rounds.json 고졸 13건. 보존: db/raw/*고졸* 원본 PDF 13회차 (향후 별도 검정고시 인제스트용). 이유: 메인 수능 학습과 분리 + 정답키 오류 다수(예: 2020_2회 회차 통째 오답키, 01번=①인데 gold=4). 아카이브(복구 가능): archive/검정고시_고졸_20260602-085715.tar.gz. 결과: 문제 2844→2584, 회차 81→68.

## [2026-06-03] promote | chat → synthesis: "다음단계" from 2023/6월모평/2023_6월모평_미적분_30

## [2026-06-08] promote | chat → synthesis: "[학습 노트 요청] "여러가지 함수의 극한과 연속" 페이지에서 지금까지 한 대화를 정리해 학습 노트를 작성해" from functions/calculus/여러가지함수의_극한/자연상수_e

## [2026-06-14] fix(decode) | 한컴 PUA 재구성 결정론 위반 216→6 + 전수 백필(3564). 비전감사(확률·샘플)→**결정론·전수 불변식 스캐너**(구조 `qa_invariant_scan.py`+KaTeX렌더 `qa_rawleak_scan.mjs`) 전환. 8수정: 분수 연속밴드워크(표garble56+overline77)·━추출제외(빈분수)·doubled footer strip·벡터 같은-y밴드+문장부호배제·cases E04B검출+인터리브판별+닫는}가드·행렬 분수바가드(좌표점·괄호분수)·backfill subject불일치 번호폴백(가형/나형578). KaTeX 렌더실패 **0/2986**. 백필 3564/1626변경/0실패. (1ca4a0d3)

## [2026-06-14] feat(problems) | 재구성 뷰 어드민 전용 — 도형 라벨이 이미지 밖으로 새는 엣지케이스로 사용자엔 부적합 → reconHTML=is_admin 게이팅, 사용자는 원본 이미지만. 디코더 가치는 인제스트 결정론 searchable_text에. 핸드오프 `docs/HANDOFF.md`. (de4d0a57)
