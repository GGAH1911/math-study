# 핸드오프 — 2026-06-19 · agy(Gemini) 도식 파이프라인 + 자율 운영

> **다음 세션 "부팅해" → 이 문서대로 이어받기.** 메모리 `project_concept_figures`·`project_gemini_corrector`·`feedback_main_only_commit` 동반 참조.

## ★부팅 시 먼저 할 일 (순서대로)
1. **상태 점검**: `pgrep -af 'gen_concept_figures|qa_concept_figures' | grep node`(실행 중 프로세스), `tail /tmp/ingest_logs/qa_all*.log`, `./server.sh status`(서버는 끄지 말 것).
2. **하트비트 cron 재생성** — cron 은 세션 전용이라 이전 세션 종료 시 죽음. 맨 아래 "하트비트 cron 프롬프트"로 `CronCreate(cron:"37 */3 * * *", recurring:true)` 다시 걸기.
3. **수정대상 패턴 집계 대기분**: QA PASS1 이 돌면 `/tmp/ingest_logs/qa_pass1_verdicts.json` 에 verdict 쌓임 → 사용자가 물으면 카테고리 집계(축/라벨겹침/area/좌표/충실성/range/점선).

## 현재 상태 (자율 도식 파이프라인 진행 중)
- **순서**: 함수 개념도식 gen ✅완료 → **QA(area 전수점검) 🔄진행중** → 3D(`Geometry3D`) ⏸설계대기 → 기출 교정기 ⏸.
- **gen 완료**: 함수 도메인 502개 처리 → figure 450 + null 50, 실패 2(추후 재생성). 전체 캐시 839 항목.
- **QA 진행중**: `qa_concept_figures.mjs --all`(agy·배치6, setsid 분리 — Claude 꺼져도 돌고 쿼터 자동재개). 839 중 **QA체크 439·미검수 334**. 현재 **쿼터 소진→자동대기**(리필 추정 ~10:00경). 리필 시 PASS1 나머지+PASS2(개별 수정·area변환·dashed) 자동 진행.
- **dev 서버**: `0.0.0.0:4323` setsid+watchdog — **끄지 말 것**, `./server.sh status`로만.
- **쿼터**: agy=Google AI Pro $20(Claude 한도와 분리). 5h 창, 소진 시 **빈 출력**(에러 아님). 정확한 리필시각은 Antigravity 앱 "Model Quota" 화면만 노출.
- **LLM 크론**: 한도절약 OFF(월 2026-06-22 03:30 자동재개 타이머) — 변동 없음.

## 미커밋 / 커밋 정책
- **옵션A 위임**: 이 자율 파이프라인 동안 **단계 마일스톤마다 commit+push 가능**(매번 안 물어봄). 그 외 일반작업은 "허락받고만"([[feedback_main_only_commit]]).
- `concept-figures.json` 은 QA 가 계속 쓰므로 **QA 완료 시 커밋**(도는 중 git add 하면 torn). QA 가 쿼터대기(쓰기 안 함)일 땐 안전.
- 미추적 debris(내 것 아님, 건드리지 않음): `web/{scratch_tangent.png,test_layout.py,verify.py,verify2.py}`.

## 이번 세션 한 일 (커밋·푸시됨, 9ad32dec6 까지 + 셧다운 커밋)
- **agy(Antigravity CLI) 백엔드**: gen·qa 를 Gemini 3.5 Flash 로(`LLM_BACKEND=agy`/`QA_BACKEND=agy`). Claude 한도 분리. `agy -p <프롬프트>`(프롬프트=값), plain text→parseEnvelope, `setEncoding('utf8')`, **쿼터 자동재개 `withQuotaRetry`**(빈출력→10분 probe→리필 재개, `QUOTA_PROBE_MIN`/`QUOTA_MAXWAIT_H`).
- **area primitive**(Geometry.tsx): 곡선/baseline 사이 면 채움(적분·넓이·부등식영역). **bareAxes** 모드(기출 스타일 축선+화살표+x/y/O, 격자·눈금 없음). **parametric dashed** 렌더 수정(엄격부등식 경계 점선). 라벨 **드래그+조건부 leader**(모든 도형 앵커·라벨 중앙·자유text 최근접 스냅). 세로형 좌우 패딩.
- **QA area 전수점검**: RUBRIC 확장(영역/넓이를 점·선다발·미표시 등 어떤 방식이든 area 누락→area 교체) + `areaHint`(키워드+area없음 감지) + **PASS1 verdict 로깅**(`qa_pass1_verdicts.json`).
- **문제 재구성 탭**(`problems/[...slug].astro`): Gemini 교정본 KaTeX($제거·[N점]제거) + bareAxes 도식, **문제→그림→선택지** 순. fixes 는 백엔드(`problem-reconstructions.json`) 보관·프론트 미노출. agy 교정+도식 테스트 `/dev/ingest-test`.

## 다음 단계 / 결정 필요
- **QA 완료 후 → 3D(`Geometry3D`)**: 76개 3D 개념. **렌더러 설계 결정 필요**(2D 투영 방식 등) → 블라인드로 짓지 말고 **사용자에게 옵션 보고**.
- **그 후 기출 교정기**(전수, 5h): ★**독립검증**(교정 맥락 안 받음 — 블라인드 재전사 diff + 솔버게이트) → 쿼터멱등 → 전수. **모듈로 빌드**(`geminiExtract`+`independentVerify`) — 나중에 Gemini 전용 인제스트 엔진 코어로 재사용. figure 축 3분기(도형=축없음/그래프=bareAxes/격자눈금-드묾). 상세 [[project_gemini_corrector]].
- gen 실패 2 + QA 미검수분은 자동/재실행으로 수렴.
- (보류) dev 라우트 재게이팅: `middleware.ts` 의 `/dev/concept-figures`·`/dev/figrender`·`/dev/ingest-test` TEMP 공개 → 작업 끝나면 admin.

## 함정 (이번 세션 새로 배운 것 + 기존)
- **agy 쿼터 소진 = exit 0 + 빈 stdout**(에러 없음). 빈출력=`quota-empty` 태그로 던져야 자동재개 인식.
- **gen·QA 이중실행 = concept-figures.json 클로버**. 재시작 시 bash 래퍼만 죽고 node 자식이 살아남음 → `pgrep ...|grep node` 로 옛 node kill 확인.
- agy CLI 는 **임의 파일 무단 Read**(보안) → gen·qa·교정기(관리자 오프라인)는 OK지만 **튜터(학생입력)는 agy 절대 금지**(`claude --tools ""` 유지).
- bareAxes 축라벨은 명시 앵커+fixed 필요(soft 면 leader 오스냅·de-overlap 밀림).
- 서버 stop 금지(setsid). 서버 뜬 채 `astro check`/`npm install` → Vite stale → `server.sh restart`. zsh `$VAR` 미분할→`${=VAR}`. 로그 `>` 덮어쓰기 금지.

## 하트비트 cron 프롬프트 (부팅 시 CronCreate `37 */3 * * *` recurring 로 재생성)
```
[자율 도식 파이프라인 하트비트 — math-study] 메모리 project_concept_figures·project_gemini_corrector 참고. 순서: 함수 gen → QA(area전수점검) → 3D(Geometry3D) → 교정기. 먼저 pgrep 확인:
① gen(pgrep gen_concept_figures|grep node) 실행/대기중이면 → 손대지 말고 종료.
② QA(pgrep qa_concept_figures|grep node) 실행/대기중이면 → 진척만 확인, 절대 새로 실행 금지(이중실행=클로버), 종료.
③ gen·QA 없고 미검수 figure 남았으면 → QA 단일실행: cd web && setsid bash -c 'QA_BACKEND=agy QA_BATCH=6 node scripts/qa_concept_figures.mjs --all --concurrency 2 > /tmp/ingest_logs/qa_allN.log 2>&1' </dev/null & ; pgrep 으로 단일 node 확인(중복이면 옛것 kill).
④ 미검수 0(전부 QA)이면 → 3D 단계: 렌더러 설계 사용자 보고 후 대기. 그 후 교정기.
규칙: 단계 전환 시 한 줄 보고. 마일스톤 커밋 위임. 갈림길 멈추고 보고. 할일 없으면 종료. 서버 stop 금지. concept-figures.json 은 gen/QA 도는 동안 직접 편집 금지.
```
