# TODO — 솔버/파이프라인 백로그

> 갱신: 2026-06-07 · 튜터 그래프 정확도(plot 교점·geometry 방향) + 크롭/게이트 4개 백엔드 균일화 후 잔여.

## 완료 (2026-06-06)
- [x] 백필 blind→open-book + 하드코딩 게이트(변이테스트) + 인제스트 본류 반영
- [x] 단답형 additive 솔버 + lite→full 승격(파라미터 변이 게이트)
- [x] KEEP-GOLD 51개 → **100% 솔버화** (회복백필 43 + 승격 29 + 수동 8)
- [x] 텍스트 품질 게이트(글리프 자동 재전사) + agent.md D17(타일 규칙)
- [x] 무결성 가드(audit_solvers) + 일관성 게이트(consistency_gate: format·답 오분류) + post_ingest_sync 자동화
- [x] regen_one 에러출력 검증 / 객관식 CANDIDATE↔gold 매핑 강제
- [x] 게이트가 찾은 추가 결함 수정: 2022·2023 기하 23/24, 단일_06/18 (format 오분류)

## 완료 (2026-06-07)
- [x] **튜터 그래프 점 정확도** — plot 교점/근을 LLM 손계산 대신 렌더러 이분법 계산(Graph.tsx `intersections`/`roots` + bisectRoot), geometry 자기닮음 방향 게이트(sympy.ts `assert_segments_disjoint`/`_cross`, chat-context 규칙), plot JSON sanitize 강화(LaTeX 백슬래시 보존·배열 수식 평가)
- [x] **상단 크롭 보정** — `crop_problem`(원래경계+headroom 18px, 스캔 제거) 전 3056문제 적용 + 인제스트 4개 백엔드 반영(**gyo3 누락분 포함**) + recrop_v3 footgun 제거 → `crop_by_gap` 호출자 0(은퇴)
- [x] **백엔드 게이트 균일화** — text_quality_gate(v2·gyo3 누락분)·consistency_gate 캐시前 인라인·풀이캐시 체이닝(gyo3 누락분) 추가 → 4개 백엔드(v2/ganah/gyo12/gyo3) 동일 템플릿

## 잔여 (난이도순)
- [ ] **섹션 라벨 박스 테두리 sliver 제거** — 섹션 시작 문제(#16·#22·#23·#29; 5지선다형/단답형 박스 바로 아래)에서 크롭 상단에 라벨 **박스 하단 테두리**가 살짝 걸림(28건, 자기검증 CLIP 8~32px). 본문은 온전(허용 범위)이라 우선순위 낮음. 해법: `bbox.py _section_label_bottoms`가 라벨 *텍스트* 하단이 아니라 **박스 테두리** 하단(박스 drawing의 y1)까지 천장으로 잡게 보정 → 박스 완전 제외. 대상 목록: 자기검증 `scripts/selfcheck_crop.py` 재실행으로 재생성.
- [ ] **크로스-스크립트 게이트/타일 일관성 감사** — 이번엔 *인제스트 4개 백엔드*만 균일화. 풀이캐시(build_solution_cache)·백필(backfill_solvers)·vision 폴백(vision_meta)·promote 가 동일 게이트/타일(D17) 규약 쓰는지 전수 대조 남음.
- [ ] **synthesis 페이지 그래프 렌더** — `docs/syntheses/` 의 promote된 plot/geometry 펜스가 Astro `<Content />`(plot 변환 플러그인 없음)에서 코드블록으로만 표시됨. remark 플러그인으로 실제 그래프 렌더 필요(튜터 런타임과 별개 경로).
- [ ] **PUA-silent 손상 감지** — text_meta 인제스트 시점에 PDF 텍스트레이어 PUA 디코드 이상 → 타일-vision 전사 승급. (silent라 감지 자체가 난제; 현 게이트는 loud 손상만)
- [ ] **신규 인제스트 full 솔버에 파라미터 변이 게이트** — 현재 backfill/promote만. build_one 객관식 수용에도 solve(**계수) 규약+param 게이트 적용.
- [ ] **brute-force 프롬프트 모드** — 조합/경우의수 단원 자동화(현재 수동 검증만).
- [ ] searchable_text 생성에 타일 적용(D17) — 속도 영향 검토 후.

## 아이패드 앱 출시 (장기 · 제품 방향)

> 비전: 기출문제를 보면서 **애플펜슬로 풀이를 직접 필기** → **LLM이 풀이 *과정*을 평가**(정답뿐 아니라 논리 단계까지). 검증된 풀이 캐시(3324/3324)가 채점 기준(rubric)이라 "일반 AI 채점"과 차별화.

**개발 가능성: 높음.** 어려운 코어(콘텐츠·검증풀이·sympy 검증·LLM 튜터)는 이미 완성돼 웹 API로 노출됨. 신규 작업은 ① 아이패드 UI ② 펜슬 필기 캔버스 ③ 필기→평가 파이프라인 ④ 호스팅 백엔드뿐.

- [ ] **아키텍처 결정** (3안):
  - (A) **네이티브 SwiftUI + PencilKit** — 펜슬 UX 최상(저지연·압력·tilt), 단 Swift 신규 코드베이스. 콘텐츠/그래프/튜터는 WKWebView로 기존 웹 재사용 + PencilKit 오버레이.
  - (B) **Capacitor 래핑(기존 Astro 웹 그대로)** + PencilKit 플러그인 — 기존 UI(문제브라우저·튜터챗·그래프) 최대 재사용, 최단 출시. 펜슬은 네이티브 플러그인으로.
  - (C) PWA(홈화면 추가) + 웹 canvas pointer events — 가장 빠르나 App Store 출시 아님 + Safari 펜슬 한계.
  - → **추천: B(빠른 출시) 또는 A(펜슬이 핵심 차별점이면)**. 핵심은 "필기 표면"만 네이티브, 나머지는 웹 재사용.
- [ ] **필기→평가 파이프라인**: 펜슬 필기 → PNG 래스터화 → **비전 LLM**(Claude vision)에 [문제 + 검증된 solution.steps + gold answer + 학생 필기이미지] 전달 → 단계별 채점(맞음/어디서 틀림/누락단계/최종답 검증). 최종답은 `sympy.ts`로 교차검증. **타일 규칙(D17) 적용** — 필기 이미지도 타일로.
- [ ] **호스팅 백엔드** (출시 차단요소): 현재 `chat.ts`는 노트북 `claude` CLI spawn(Tailscale 자가호스팅). 출시엔 Anthropic API 직결 + 클라우드 서버 필요. chat.ts의 프롬프트인젝션 방어·모델락(haiku)·slug 검증을 그대로 이식. 비전 평가 호출당 API 비용 산정.
- [ ] **리스크/검증 선행**: (1) 비전 LLM이 **손글씨 한글 수식**을 얼마나 정확히 읽나 — 소수 샘플로 PoC 먼저(가장 큰 불확실성). (2) PencilKit vs 웹 canvas 지연 비교. (3) 채점 프롬프트는 튜터(대화형)와 별개 — *완성된 시도를 루브릭 대비 채점*하는 전용 프롬프트 필요.
- [ ] **재사용 자산 확인됨**: API(chat·sympy·attempt·problem-state·progress·mastery-promote), 검증풀이 3324, 크롭 이미지, searchable_text, SRS 상태. UI(ProblemAttemptPanel·ChatPanel·Graph)도 웹뷰로 재활용 가능.
