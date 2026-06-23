# TODO — 솔버/파이프라인 백로그

> 갱신: 2026-06-23(저녁) · 3D 도식·수식가독성·오늘의페이지·캐싱. **부팅·진행상태는 `docs/HANDOFF.md`**.

## 완료 (2026-06-23 저녁) — 3D·수식·오늘의페이지·캐싱
- [x] **3D 개념도식 전수(84개)** gen `--only-3d`+figure3d. 개념페이지 3D+2D 둘다 렌더. Geometry3D KaTeX 라벨(Label3D). 5카테고리 50점 전수검수(평균46.2, 미달 즉시교정16). 갤러리 `/dev/figgallery3d?src=cache`(Lazy3D).
- [x] **수식 줄바꿈 가독성**: 인라인 nowrap+오버플로우 CSS, 긴 등식 $$블록 프롬프트지침, \frac→\tfrac 후처리(728파일 `scripts/fix_inline_math.py`).
- [x] **오늘의페이지 그림 근본수정**: ETIMEDOUT 재시도3회+timeout180s, cron 06:00·12:00 보강.
- [x] **claude -p DISABLE_GIT 이중우회**: clean cwd + CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS=1(배치6곳, 튜터 제외). 실측 cache_read 고정. [[project_claude_p_caching]]

## 보류/후속
- [ ] (선택) 그래프 변경 시 오늘의페이지 폴백 노출 — 낮 시간대 그래프변경 시 다음 cron(최대~6h)까지 폴백곡선. 매시간 cron or 렌더시 즉시생성(무거움)은 미적용.
- [ ] (선택) 완전 캐싱 = Anthropic API 직접 cache_control(커스텀 system 포함). 현 CLI는 내장 base만.
- [ ] (선택) 3D 도식 ad-hoc 잔여 영어/카메라 미세조정 — 전수검수 통과했으나 일부 라벨 작음.

## 완료 (2026-06-23) — 인제스트 캐싱·루프·2019수능
- [x] **claude -p 프롬프트 캐싱 전수 적용**(clean cwd): verify_batch·corrector·ingest_round·build_solution_cache·chat.ts(튜터)·gen_daily·regenerate-body + cta-law. git-env churn 제거 → 콜당 ~10× 절약, 매핑 타임아웃 해소. `docs/CLAUDE_P_CACHING.md`.
- [x] **재교정 agent-loop**(corrector `CORR_BACKEND=agent`, claude --max-turns) — agy 다운 대체. ingest_auto `RECORRECT_BACKEND` override.
- [x] **교정 후처리 배선**: corrector→box_backfill(박스마커 결정적)→concept_remap(교정후 개념재매핑)→솔버캐시→sync. PAR_C=2.
- [x] **2019학년도 수능 완전 적재**(60/60: 교정·솔버·풀이·박스11·개념60). 핸드솔브 9건 직접풀이(변이테스트 통과, 가형30=p=-9π a²=27).
- [x] **ad-hoc 슬러그 정리**(`cleanup_adhoc_concepts.py`): 38종 기존개념 흡수·새개념0. build-problem-index flat→nested 폴백. 누락 668→0.
- [x] **핸드솔브 큐 vision_tiles 주입**(타일 직접 Read 강제).
- [x] gemma 솔버 테스트 → **미도입 결정**(상급 killer 무능). 기존 사다리 유지.

## 보류/미진행
- [ ] (사장님 결정) **검정고시 인제스트** — 이번엔 안 함.
- [ ] (선택) build_solution_cache usage 로깅 추가(캐싱 절약 직접 측정용 — 현재 corr/verify 로그로 간접측정).
- [ ] (선택) 완전 캐싱 = Anthropic API 직접 cache_control(커스텀 system 포함) — 현재 CLI는 내장 base만 캐시.

## 자율 도식 파이프라인 (2026-06-19) — 부팅·함정은 `docs/HANDOFF.md`
순서: 함수 gen → QA(area전수점검) → 3D(`Geometry3D`) → 기출 교정기. 하트비트 cron(세션전용, 부팅 시 재생성).
- [x] agy(Gemini Flash) gen·qa 백엔드 + 쿼터 자동재개(`withQuotaRetry`, 빈출력=쿼터) + setsid 분리.
- [x] area primitive·bareAxes·parametric dashed·드래그 라벨(앵커/leader)·세로패딩 (Geometry.tsx).
- [x] QA area 전수점검(RUBRIC+areaHint+PASS1 verdict 로깅).
- [x] 문제 재구성 탭(Gemini 교정 KaTeX+bareAxes, 문제→그림→선택지, fixes 백엔드보관) + `/dev/ingest-test`.
- [x] **함수 도메인 gen 완료**(figure 450·null 50·실패 2). 전체 캐시 839.
- [~] **QA --all 진행중**(agy·배치6, 839중 439 QA됨·334 미검수, 쿼터대기 자동재개). 완료 시 `concept-figures.json` 커밋.
- [ ] **3D/공간 76개** → `Geometry3D` 신규. ★렌더러 설계 결정 필요(사용자 보고 후). 현재 2D만(`--include-3d` 대상).
- [ ] **기출 Gemini 교정기**(전수 5h): 독립검증(블라인드재전사 diff+솔버게이트)→쿼터멱등→전수. 모듈(`geminiExtract`+`independentVerify`) → Gemini 인제스트 엔진 코어 재사용. [[project_gemini_corrector]].
- [ ] gen 실패 2개 재생성 + 라벨 leader 스냅 휴리스틱(아래).
- [ ] **dev 라우트 재게이팅**: `middleware.ts` 의 `/dev/concept-figures`·`/dev/figrender`·`/dev/ingest-test` TEMP 공개 → 작업 끝나면 admin 으로.
- [ ] (선택) equations·algebra·prob-stats 도메인(도식친화도 낮음, 후순위).
- [ ] **라벨 leader 스냅 휴리스틱 개선**: 자유 `text` 라벨(변 길이 숫자 8·10 등)은 어느 도형을 가리키는지 스펙에 없어, 드래그 시 **가장 가까운 변/점**으로 leader 를 스냅한다(`nearestOnSegs`). 라벨이 의도와 다른 요소에 더 가까우면 오스냅 가능. 근본 해결 = 생성 단계에서 변 길이를 **segment 라벨**(또는 polygon 변 라벨)로 붙여 명시 앵커를 갖게 함(현재 free text → 재생성 필요). 우선순위 낮음.

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

## 완료 (2026-06-14)
- [x] **한컴 PUA 재구성 결정론 위반 216→6 + 전수 백필(3564)** (1ca4a0d3) — 비전감사(확률·샘플)를 **결정론·전수 불변식 스캐너**(구조 `qa_invariant_scan.py` + KaTeX렌더 `qa_rawleak_scan.mjs`)로 교체. 8수정: ①분수 grab 연속밴드워크(표garble56+overline77 동시) ②`━`(U+2501) 추출제외(빈분수·구분선) ③doubled footer strip(공백허용) ④벡터 body 같은-y밴드+문장부호배제 ⑤cases 큰브레이스 E04B검출+인터리브판별(관계연산자2+)+닫는`}`가드(그룹/집합 오소비차단) ⑥행렬 분수바가드(좌표점 `(π/6,5/2)`·괄호분수 오검출, 수능엔 행렬無) ⑦backfill subject불일치(가형≠'공통') 번호폴백. 결과 위반 **216→6(0.17%)**, KaTeX 렌더실패 **0/2986**. 백필 3564처리/1626변경/0실패. 잔여6=깊은중첩분수~3+bbox crop-bleed~2+옛교육과정1(전부 렌더정상).
- [x] **재구성 뷰 어드민 전용** (de4d0a57) — 도형 라벨(이미지에 박힌 글자)이 재구성에선 이미지 밖으로 새 사용자엔 부적합 → `[...slug].astro` `reconHTML = isAdmin ? reconFull : ''`(isAdmin=`Astro.locals.user.is_admin`). 사용자는 원본 이미지(`<Content/>`)만, 어드민만 토글/재구성. 디코더 가치는 인제스트 결정론 searchable_text에.

## 완료 (2026-06-17) — UI/UX + 오늘의 페이지 + 튜터 그래픽/렌더
- [x] **튜터 채팅 UI 전면 정비** — 채팅 스크롤바 커스텀 드래그(모바일 네이티브 한계 우회); 컨텍스트 서랍 모바일 탭열기+위/아래 스와이프+그래버 손잡이(OS 홈제스처 충돌 해소); 채팅 **FAB화**(개념=전화면 FAB, 문제=md+컬럼·모바일FAB, 홈=FAB+태블릿 미표시 버그 수정); 데스크탑 FAB 본문 우측 hug; **데스크탑·태블릿 백드롭 제거→그래프 패널 동시 조작**; 메뉴 breakpoint lg→xl(태블릿도 ☰).
- [x] **브랜드·테마 통일** — 사이드바·헤더·favicon = 빨간 작도 인장(삼각자·점박스 폐지); 테마 토글 해/달 SVG.
- [x] **오늘의 페이지 = 매일 새 개념 + 그림 + 인사이트** — `daily-concept.mjs`(전체 풀 ~2800 고정셔플 순회); 개념별 LLM(Sonnet) figure spec + blurb 생성→`concept-illustrations.json` 캐시→**크론(23:40 KST) 내일치 미리 생성**; `PaperHero` 손그림 렌더(Catmull-Rom 스플라인, 좌표축 제거, 폴백=일반곡선); `/dev/daily-figures` 갤러리. `gen_daily_illustration.mjs`.
- [x] **튜터 도형 단계검증 강제** — 트리거 '문제재현'→'좌표 정확성 필요 전반(개념설명 포함)'; ★ChatPanel turn-1: python+그래픽 동시 시 미검증 그래픽 strip→sympy 검증 강제(이전 `hasGeometry break`로 검증 스킵되던 근본 차단). Haiku 비순응 대응.
- [x] **KaTeX/표 렌더 보정** — `\text{}` 안 수학 관계 유니코드(≠→×÷±≤≥⇒≈∈)→$math$ 섬(text-mode hard-throw 방지, `katex-normalize.mjs`); 박스드로잉 ASCII 표(코드펜스 ``` 안 포함)→HTML 표(`markdown.tryParseTable`+ChatPanel 펜스 분기). katex-harness 11→12.

## 잔여 (난이도순)
- [ ] **concept-illustrations.json 크론 dirty** — 매일 갱신돼 워킹트리 주기적 dirty(정상). 주기적 커밋 or gitignore 정책 결정.
- [ ] **히어로 figure 품질 들쭉** — 일부 개념(조건부명제 등) 약함. 캐시 id 삭제 후 `gen_daily_illustration.mjs <offset>` 재생성. 정확도 중요해지면 sympy 좌표→손그림 하이브리드(보류).
- [ ] **atlas(개념지도) 대시보드 채팅 인라인** — 홈만 FAB화함. 통일 검토.
- [ ] **Haiku 단계검증 비순응 모니터** — turn-1 strip로 강제 중이나 완벽치 않음.
- [ ] **재구성 도형 라벨 누출** (어드민 전용이라 보류) — 도형을 재구성에 넣으면 이미지에 픽셀로 박힌 라벨 글자가 이미지 밖 텍스트로 중복/누락. **재구성을 사용자에게 다시 노출하려면 선행 필요.** 현재 사용자=원본이미지라 영향 없음.
- [ ] **재구성 결정론 잔여 6/3564(0.17%, 표시 안 됨)** — 깊은 중첩분수 `\frac{\overline{N}}{…}`~3, **bbox crop-bleed ~2**(옆 문제 글자가 크롭경계 침범 → `bbox.py` 영역, 디코더 아님), 옛교육과정 1. 전부 렌더 정상이라 우선순위 낮음. 재검증=`qa_invariant_scan.py`(decoded_all 재생성 후).
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
