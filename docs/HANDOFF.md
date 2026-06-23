# 핸드오프 — 2026-06-23(저녁) · 3D 도식 전수 + 수식 가독성 + 오늘의페이지 + claude -p DISABLE_GIT

> **다음 세션 "부팅해" → 이 문서대로 이어받기.** 메모리 `project_claude_p_caching`·`project_concept_figures`·`project_daily_concept_hero`·`feedback_main_only_commit`·`reference_noauth_verify_port` 동반 참조. (인제스트/2019수능 핸드오프는 아래 "이전 세션(낮)" 참고.)

## ★부팅 시 먼저 할 일
1. **상태 점검**: `git status`(깨끗해야), `git log --oneline -10`, `./server.sh status`(4323·4324 끄지 말 것).
2. **서버 3종 확인**: 4323(실시간)·4324(STABLE)·4325(noauth 검증포트). ★**4325는 오케스트레이터 검증의 핵심**(사용자 지정) — 죽었으면 반드시 복구. 자꾸 죽는 원인=watchdog 좀비 누적 → 아래 4325 복구절차.
3. **이어받을 작업 없음(이번 세션 전부 완료·커밋)** — 새 지시 대기.

## 이번 세션(2026-06-23 저녁) 한 일 — 전부 커밋·푸시됨 (7b0c68e4c 까지)
1. **3D 개념 도식 전수(84개)** — gen_concept_figures `--only-3d` + figure3d 캐시(gemma 73 + sonnet 11). 개념페이지([...slug].astro) **3D+2D 둘 다 렌더**(구가 2D로만 보이던 버그 수정). Geometry3D **KaTeX 라벨 렌더**(Label3D: \vec·첨자·그리스·한글+$수식$ 혼합). **5카테고리(평면입체정합·완전성·KaTeX·좌표정확·충실성)×10=50점 전수검수**: 74채점 전부≥45(평균46.2), 미달 즉시 직접교정 16건(외적→평행사변형, 회전체/원기둥 곡면 미정의변수 복구, 영어라벨 13 한글화, label?물음표키 5, 카메라각도 등). 검수=figrender3d(2D+3D+READY신호) 헤드리스 캡처, 갤러리 `/dev/figgallery3d?src=cache`(Lazy3D=IntersectionObserver로 WebGL 컨텍스트 한계 회피). ★헤드리스 WebGL 캡처=`--headless=new --use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader`.
2. **수식 줄바꿈 가독성**(사용자 지적) — ①인라인 .katex nowrap+inline-block max-width 오버플로우(중간 안쪼개짐, 긴건 자체 가로스크롤) ②긴 등식체인 $$블록 생성프롬프트 지침(regenerate-body·fill_spoke_bodies) ③인라인 \frac→\tfrac 후처리 728파일 2036개(scripts/fix_inline_math.py, 블록 \dfrac 보존). global.css.
3. **오늘의 페이지 그림 근본수정** — gen_daily_illustration: ETIMEDOUT 자동재시도 3회(5s·12s)+timeout 120→180s, cron 06:00·12:00 day+0 보강 추가(23:40 미리생성 유지). 원인=①claude 응답시간 편차 ETIMEDOUT ②그날 그래프 변경 시 pickDailyConcept 결과 바뀌어 cron 캐시 무효. 오늘·내일·모레·+3 그림 채움.
4. **claude -p DISABLE_GIT 이중우회**(토론→측정→적용) — git status가 system prompt prefix 깨는 **알려진 이슈**(커뮤니티 동일 인식). clean cwd(기존)+`CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS=1`(신규) 벨트+멜빵. ★실측: git켜짐 cache_read 호출마다 변동(17506→25092), DISABLE_GIT 반복 23478 고정. 적용 6곳(corrector·verify_batch·build_solution_cache·ingest_round·gen_daily·gen_concept_figures), **튜터 chat.ts 제외**(clean cwd만). [[project_claude_p_caching]]

## 4325(noauth 검증포트) 복구 절차 — 자주 죽음
원인: stop/start 반복으로 watchdog 좀비 누적(`pgrep -af 'server.sh __watchdog'` 으로 PORT별 확인) + setsid 분리 꼬임. 복구:
```
# 4325 watchdog/astro 정리 (4324 STABLE 보존 — environ의 MATH_STUDY_PORT 로 구분)
for pid in $(pgrep -f 'server.sh __watchdog'); do port=$(tr '\0' '\n' </proc/$pid/environ|grep MATH_STUDY_PORT|cut -d= -f2); [ "$port" = 4325 ] && kill -9 $pid; done
pkill -9 -f 'astro dev.*4325'; rm -f /tmp/math-noauth.pid
# 직접 기동(watchdog 우회가 가장 확실) — content store 재로딩 ~60초 대기
cd web && nohup env DEV_NOAUTH=1 node node_modules/.bin/astro dev --host 127.0.0.1 --port 4325 > /tmp/4325_direct.log 2>&1 &
# 200 될 때까지: until curl -sm3 127.0.0.1:4325/ -o/dev/null -w '%{http_code}'|grep -q 200; do sleep 4; done
```
★pgrep는 자기 명령문 매칭 false-positive 잦음 → 실제 프로세스는 `ss -tlnp|grep :4325`(포트) 또는 `ps`로 확인.

## 이전 세션(2026-06-23 낮) — 인제스트 캐싱·2019수능 (bc2888ab0 까지)
1. **claude -p 프롬프트 캐싱 전수 적용** (핵심). 레포 cwd면 git-env 블록 churn으로 캐시가 깨짐 → 모든 claude -p 호출을 **clean cwd**(`/tmp/claude_p_clean`)에서 spawn. 적용 경로: verify_batch·corrector·ingest_round(claude_p)·build_solution_cache(5곳)·chat.ts(튜터)·gen_daily_illustration·regenerate-body + cta-law llm_client. 실측 콜당 cache_read≈43k·plain in~0 → 프리픽스 ~10× 절약. **개념매핑 60초 타임아웃도 해소**(거대 env 제거). 한계: 커스텀 `--system-prompt`는 CLI가 캐시 안 함(내장 base만) → 완전캐싱은 API 직접 cache_control 필요(미실행). 상세 `docs/CLAUDE_P_CACHING.md`.
2. **재교정 agent-loop 백엔드**: corrector.mjs 에 `CORR_BACKEND=agent`(claude -p `--max-turns`, 이미지 Read→교정→자가검증). agy(쿼터다운) 대체. ingest_auto `RECORRECT_BACKEND` env override. gemma 격리 하드테일 자동복구 실증.
3. **교정 후처리 배선**(ingest_auto): corrector → **box_backfill**(결정적 박스마커, LLM0) → **concept_remap**(교정된 텍스트로 개념 재매핑, '매핑前 교정' 원칙, haiku·캐시) → 솔버캐시 → sync. PAR_C 기본 2(gemma 2병렬). corrector validate 길이비에서 `[그림:]` 제외(false-positive 격리 방지)+재교정 성공시 격리마커 해제.
4. **2019학년도 수능 완전 적재**: 60문제(가/나형 각30). corrector_verify 60/60 ok·솔버 60/60·verified 60/60·박스11·개념60. **핸드솔브 9건 오케스트레이터 직접풀이**(변이테스트 ±1→FAIL 전수통과): 가형22/23/24/27/28/30·나형22/29/30. 하이라이트 **가형30(킬러)=p=-9π 닫힌형 a²=27**, 가형28(타원)=수치검증11.
5. **ad-hoc 슬러그 정리**: 개념그래프에 없는 즉석 슬러그(LLM 매핑 부산물, 전 회차 누적)를 `scripts/cleanup_adhoc_concepts.py`로 정리. 38종 기존개념 흡수(정규화+의미매핑)·1종 제거·레거시 멀티라인2건·빈concepts1건 수정. **새 개념 생성 0**(사장님 지침: 최대한 기존 노드 연결). build-problem-index에 flat-slug→nested 폴백 추가. 누락 668→**0**, 빈concepts 0, audit_solvers orphan/누락 0.
6. **핸드솔브 큐 vision_tiles 주입**: `_queue_entry`가 타일경로+instruction을 큐 json에 넣어, 오케스트레이터가 통이미지 대신 **타일을 Read로 직접** 보게 강제. scripts/CLAUDE.md 프로토콜 명시. [[project_handsolve_tiles]]

## 결정 사항 (사장님 지시)
- **gemma 솔버 도입 안 함** — 테스트 결과 상급 killer(가형30) 🔴 완전실패(답·솔버 0). 기존 사다리(Haiku→Sonnet→Opus + 오케스트레이터 핸드솔브) 유지. (난이도별 예상 하🟢/중🟡/상🔴 실증.)
- **검정고시 인제스트 안 함** (이번엔).

## 인제스트 파이프라인 (차기 회차 — 검증된 자동 흐름)
```
python scripts/ingest_kice/ingest_auto.py --run [--only <slug>]
  → 감지/스테이징 → 추출+크롭 → 교정[gemma×2 ∥ sonnet검증(캐시) ∥ 재교정]
  → box_backfill → concept_remap → build_solution_cache → post_ingest_sync
```
- 재교정 백엔드: 기본 agy. agy 다운 시 `RECORRECT_BACKEND=agent`(claude 에이전트루프).
- 솔버: auto 사다리 통과분 자동 + **단답 gold-match·killer·도형은 핸드솔브 큐 → 오케스트레이터 직접**(서브에이전트 위임 금지, [[feedback_handsolve_orchestrator]]). 큐 json `vision_tiles` 를 Read 로 보고 변이테스트 통과 솔버 작성.
- 멱등: corrector_verify:ok·skip-cached 자동 스킵.

## 커밋 정책 / 미커밋
- main-only + 작업 끝나면 commit+push. git 상태 현재 깨끗.
- 미추적 debris(내 것 아님, 건드리지 않음): `web/{scratch_tangent.png,test_*.py,verify*.py}` — 이전 세션 산물.

## 함정 (이번 세션 + 기존)
- **clean cwd 안전조건**: 파일 접근은 반드시 `--add-dir`(절대경로). 상대경로 의존 호출은 clean cwd로 옮기면 깨짐(verify 실행 `_run_code` 등은 cwd 안 바꿈).
- **build-problem-index 누락 경고**: 문제 frontmatter가 flat slug(`docs/concepts/X.md`) 참조인데 개념은 nested 저장 → leaf 유일 시 폴백. leaf 중복이면 모호로 남김.
- **레거시 멀티라인 concepts**: 구형 문제는 `concepts:\n  - 슬러그`(경로없음) 형식 — 단일라인 `[...]` 정규식이 못 잡음. 정리 시 둘 다 처리.
- **가짜솔버 방지**: 변이테스트(CANDIDATE ±1→FAIL) 필수. 객관식은 게이트 약함→realmath+원본통과만, 도형은 타일 직접보고 검증.
- gemma 상급 killer 무능(닫힌형 추론·도형판독 불가). 서버 stop 금지(setsid). 서버 뜬 채 `astro check`/`npm install`→Vite stale→`server.sh restart`. 로그 `>` 덮어쓰기 금지(append/타임스탬프).

## 이전 컨텍스트 (도식 파이프라인 — 보류, 별도 재개 시)
함수 개념도식 gen 완료(figure 450)·QA(area전수점검) 진행중이었음 → 3D(Geometry3D, 설계대기) → 기출 Gemini 교정기. 상세 [[project_concept_figures]]·[[project_gemini_corrector]]. 재개하려면 git 이력 9ad32dec6 근방 + 당시 하트비트 cron 프롬프트 참조(git log).
