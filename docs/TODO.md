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

## 완료 (2026-06-09)
- [x] **변수지수 plot 선 미렌더** — function-plot 기본 `interval` 샘플러가 `pow(interval,interval)`=변수지수 `(1+1/x)^x`·`a^x`·`x^x` 평가 못 해 선 통째로 미생성(에러 없음, hover 값만 뜸). `Graph.tsx`에서 변수지수 함수만 `graphType:'polyline'` 전환(상수지수·asymptote는 interval 유지, 회귀 0)
- [x] **엣지케이스 버그 전수 스윕 + 수정 (42건)** — 다중에이전트로 코드베이스 전체에서 "조용한 엣지케이스 실패" 탐색(14그룹) → 적대적 검증(42확인/20기각) → 파일분리 4버킷 병렬 수정. **HIGH 1**: `ingest_gyo3.py` 미설정 `image_path` KeyError로 회차 전체 인제스트 크래시(gyo12 패턴 이식). **MEDIUM**: promote.ts `$$`→single-`$` 손상(함수형 replacer), chat-context 대시보드 spoke 전량 드롭·compact헤더 `===`/`---`·searchConcepts 1글자개념, chat.ts SSE 한글 멀티바이트 청크경계 깨짐, ingest_v2 format 오분류, ConceptDAG NFC/NFD·대소문자 검색, Geometry angle 라벨 ±π 분기. **LOW 다수**: Numberline/StatsChart/Geometry 퇴화입력 NaN 가드, srs.ts KST off-by-one, answer_textlayer 선택N fallback, ingest_auto zip가드, build_solution_cache FORBIDDEN 오탐 등. 검증: 신규 타입에러 0(astro check 92=92 baseline), py_compile·esbuild 통과, dev서버 HMR 정상.

## 잔여 (난이도순)
- [x] **기존 타입부채 92건 정리 → astro check 0 errors** (03129aec) — 92건 중 59건이 단일 근본원인 `@types/node` 누락(process·node:fs·Buffer·NodeJS 등 + 그 cascade). 추가: content.config `z.record` 2인자, `source ?? {}` optional chaining, `source.number` string|number 산술 Number()·Entry 타입확장, ChatPanel KatexImpl·Graph MathEvalFn·MathField `<math-field>`(React19 react모듈 JSX)·astro.config remark 콜백 JSDoc 등. typescript+@astrojs/check devDep 고정 + `npm run check`.
  - 재누적 방지: **git pre-push 훅 설치됨**(`.git/hooks/pre-push` → `astro check`, 타입에러시 push 차단, 우회 `--no-verify`). `server.sh` 가 `astro dev` 직접 호출(npm 우회)이라 predev/prebuild 훅은 무의미해 push 경계를 게이트로. 훅은 로컬 전용(`.git/hooks` 미커밋).
- [x] **학습 길잡이 개념 검색 그라운딩** (ffcb8a0b) — `searchConcepts`(char-bigram) + chat.ts 가 질문 매칭 실존 개념을 "복사할 전체 URL"로 프롬프트 주입. 자연상수_e 등 전용 노드를 찾아 정확 경로 링크. 잔여(선택): Haiku 가 가끔 무링크/경로축약 → **결정적 안전망**(SSE 델타 버퍼링 또는 client 측 후보맵으로 `/concepts/<leaf>`→전체slug 교정)으로 100% 링크 보장. math `[` 엣지케이스 주의.
- [x] **개념 본문 flat-slug 링크 404** (aeb048d7) — 본문 `[이차함수](/concepts/이차함수)` 가 중첩 라우트(`functions/middle-3/이차함수`)와 안 맞아 전부 404. remarkRewritePaths 에 leaf→full 맵 재작성 + [...slug] prereq fallback. **잔여(경미)**: ① 본문 링크를 flat 으로 *생성*하는 곳(spoke body 생성기 등) 찾아 애초에 nested 로 쓰게 하면 remark resolver 가 belt-and-suspenders 가 됨 ② `build-concept-graph.mjs` slugFromRef 가 flat prereq 2개 파일(`_코사인_구하기` 등)을 못 풀어 엣지 누락 → 동일 leaf→full fallback 추가(빌드 재실행 필요).
- [ ] **랜덤 시험 객관식↔단답형 자리 뒤바뀜** (버그) — `/exam/random`에서 객관식 자리에 단답형이, 단답형 자리에 객관식이 나옴. 원인: `web/src/lib/exam-build.ts`가 **영역(대수/미적분1/확통)·난이도 tier로만** 30문제를 뽑고 **format(choice/numeric) 위치 구조를 안 지킴**. 수정: 뽑은 뒤 실제 수능 배치(공통: 1-15 객관식·16-22 단답 / 선택: 23-28 객관식·29-30 단답; 양식별 상이)에 맞게 format별로 슬롯 배정·정렬. ExamRunner.tsx 표시 순서도 확인. consistency_gate가 고친 정확한 format 기준으로.
- [ ] **섹션 라벨 박스 테두리 sliver 제거** — 섹션 시작 문제(#16·#22·#23·#29; 5지선다형/단답형 박스 바로 아래)에서 크롭 상단에 라벨 **박스 하단 테두리**가 살짝 걸림(28건, 자기검증 CLIP 8~32px). 본문은 온전(허용 범위)이라 우선순위 낮음. 해법: `bbox.py _section_label_bottoms`가 라벨 *텍스트* 하단이 아니라 **박스 테두리** 하단(박스 drawing의 y1)까지 천장으로 잡게 보정 → 박스 완전 제외. 대상 목록: 자기검증 `scripts/selfcheck_crop.py` 재실행으로 재생성.
- [ ] **크로스-스크립트 게이트/타일 일관성 감사** — 이번엔 *인제스트 4개 백엔드*만 균일화. 풀이캐시(build_solution_cache)·백필(backfill_solvers)·vision 폴백(vision_meta)·promote 가 동일 게이트/타일(D17) 규약 쓰는지 전수 대조 남음.
- [ ] **synthesis 페이지 그래프 렌더** — `docs/syntheses/` 의 promote된 plot/geometry 펜스가 Astro `<Content />`(plot 변환 플러그인 없음)에서 코드블록으로만 표시됨. remark 플러그인으로 실제 그래프 렌더 필요(튜터 런타임과 별개 경로).
- [ ] **PUA-silent 손상 감지** — text_meta 인제스트 시점에 PDF 텍스트레이어 PUA 디코드 이상 → 타일-vision 전사 승급. (silent라 감지 자체가 난제; 현 게이트는 loud 손상만)
- [ ] **신규 인제스트 full 솔버에 파라미터 변이 게이트** — 현재 backfill/promote만. build_one 객관식 수용에도 solve(**계수) 규약+param 게이트 적용.
- [ ] **brute-force 프롬프트 모드** — 조합/경우의수 단원 자동화(현재 수동 검증만).
- [ ] searchable_text 생성에 타일 적용(D17) — 속도 영향 검토 후.

## 사용자별 학습자 모델 (장기 · 서비스 확장)

> 회원관리 도입 시 **사용자별 수준 추적**이 필요. 지금은 시스템프롬프트의 하드코딩 수준
> (`자기 보고 수준: 2차방정식까지`)을 제거하고 "고정 가정 말고 mastery·대화에서 파악"으로
> 대체함(chat-context.ts 3곳). 이건 임시 — 진짜 동적 학습자 모델은 아래.

- [ ] **사용자별 동적 학습자 모델** — 현재 mastery는 개념 frontmatter에 *전역 1인분*으로만 저장(다중 사용자 불가). 회원관리 붙이면: ① 사용자별 mastery/진도 저장(DB, user_id 키) ② **정량 수준**=개념별 mastery에서 자동 도출(현재 frontier 학년) ③ **정성 프로필**(목표·약점패턴·학습페이스)을 튜터가 `promote`처럼 block으로 갱신 → 사용자별 프로필 파일/테이블 ④ 프롬프트는 그 사용자의 수준+프로필을 동적 주입(하드코딩 0). 하이브리드(정량 도출 + 정성 튜터갱신)가 목표.

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
