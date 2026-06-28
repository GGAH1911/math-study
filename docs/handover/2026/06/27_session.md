# 핸드오프 — 2026-06-27 · 필기 캔버스 밤샘 빌드(A/B/C 1단계) + ★CI/배포 빌드 복구

> **다음 세션 "부팅해" → 이 문서대로 이어받기.** 메모리 `project_handwriting_canvas`·`feedback_main_only_commit`·`reference_noauth_verify_port`·`feedback_shutdown_keep_server` 동반 참조.

## ★부팅 시 먼저 할 일
1. **상태 점검**: `git status`(깨끗해야), `git log --oneline -10`, `./server.sh status`(4323·4324 끄지 말 것). `git rev-parse HEAD` == `origin/main`(동기화 확인).
2. **서버 3종**: 4323(실시간)·4324(STABLE 학습용)·4325(noauth 검증포트). 죽었으면 아래 4325 복구절차.
3. **CI 상태**: 이번 세션에 CI/배포 빌드 복구함(아래). `gh run list --workflow=ci.yml -L 1`로 최신이 success인지 확인.
4. **이어받을 작업**: 필기 캔버스 남은 항목(아래) — **단, 실펜 테스트·설계 입력이 필요해 사장님 피드백 먼저**. 새 지시 대기.

## 이번 세션(2026-06-27) 한 일 — 전부 커밋·푸시됨

### 1. 필기 캔버스 밤샘 자율빌드 (사장님 '제일 중요한 기능') — ~40커밋
- **A**: 지우개 영역커서(점선원·호버)+크기(소/중/대) · **A3 갈무리**(올가미 선택→이동·복제·색·레이어이동·삭제·전체선택, undo 4종 add/remove/mutate/move, 점-선분 히트테스트)
- **B**: 📐직선도구+각도/격자 스냅 · **전체화면 문제 좌측절반분할**+세로→가로유도(헤드리스 시각검증✓) · 📷PNG내보내기(toDataURL, 튜터피드백 토대) · 펜/종이 설정영속(ink:prefs)
- **C 1단계**: `web/src/lib/shape-recognize.ts` 손그림→직선/원/타원/삼각형/사각형/다각형 분류(곡률코너+엣지직선성+균일리샘플, **합성 12/12**+`/dev/shape-gallery` 시각검증) + **⬡ 도형모드** 자동스냅
- 인프라: UI캔버스 분리(커서/선택박스=비desync z999, iOS 정적표시 안전) · 자가리뷰 3픽스
- ★**iOS 더블탭 3대버그**(콜아웃·필기사라짐·짝수획누락)는 이전 세션에 해결("작동한다" 확인). 상세 메모리 `project_handwriting_canvas`.
- **상세 보고서·테스트 체크리스트 = `docs/report/handwriting-overnight-report.md`** (필독).
- ★**실펜 미검증**(헤드리스라 펜입력 못 봄): A3 갈무리·⬡도형모드 자동스냅·지우개 커서가 아이패드 1순위 테스트.

### 2. ★CI/배포 빌드 복구 (15시간 #1~#23 계속 실패하던 것 → 그린)
원인 = **밤샘 필기작업과 무관한 3가지 선재 문제**:
1. **CI가 `npx astro check`를 직접 실행** → npm `prebuild`(concept-graph/summaries·syntheses-by-concept 생성, 전부 gitignore) 건너뜀 → '모듈 못 찾음' 8에러. → `.github/workflows/ci.yml`에 prebuild 단계 추가.
2. **Geometry.tsx 미커밋**(커밋된 figrender3d가 noLabelBg 의존) → 커밋.
3. ★**문제이미지 심링크 2584개가 절대경로**(`/home/insung/Projects/...`=로컬)로 커밋됨 → 클린 체크아웃(CI·배포)서 전부 댕글링→vite copyDir ENOENT. → `../../../db/raw/...` 상대경로로 변환(07a211ee6). **이게 프로덕션 배포도 동일하게 깨뜨렸음 — 같이 복구됨.**
- **★재발 방지 TODO**: 심링크를 *만드는* 인제스트 파이프라인(extract_figures 계열 추정, sync-assets 아님)이 여전히 절대경로로 생성하면 **새 회차 적재 시 다시 절대 심링크 발생**→빌드 재실패. 생성지점 찾아 상대경로화 필요(미완).

### 3. Gmail MCP — 보류
사장님이 메일 확인용 Gmail 플러그인 요청 → `@gongrzhe/server-gmail-autoauth-mcp` 후보. 단 Google OAuth 자격증명(gcp-oauth.keys.json) 생성+승인이 사장님 몫(~10분)이라 보류. "Gmail 설치해"하면 재개.

## 남은 항목 (사장님 피드백·기기테스트 필요 — 단독 강행 말 것)
- [ ] **필기 C 2단계**: 도형 자동스냅 후 **1탭 확정 UI** + **InteractiveSpec 슬라이더로 파라미터 실시간 조절**(슬라이더 파라미터·범위 설계는 사장님 입력 필요, [[project_concept_widgets]]·Geometry3D 엔진 재사용).
- [ ] **갈무리→튜터 이미지 피드백**: 📷 내보내기 됨; 채팅 이미지첨부+튜터 vision(chat.ts/ChatPanel 개조) 남음.
- [ ] **필기 DB 저장**(localStorage→기기간 동기화, 멤버십 백엔드).
- [ ] **★심링크 재발 방지**(인제스트 파이프라인 상대경로 생성 — 위 2번 후속).
- [ ] **실펜 테스트 후 버그픽스**(아이패드 피드백 받고).

## 4325(noauth 검증포트) 복구 절차 — 자주 죽음
원인: stop/start 반복으로 watchdog 좀비 누적(`pgrep -af 'server.sh __watchdog'`) + setsid 분리 꼬임. 복구:
```
# 4325 watchdog/astro 정리 (4324 STABLE 보존 — environ의 MATH_STUDY_PORT 로 구분)
for pid in $(pgrep -f 'server.sh __watchdog'); do port=$(tr '\0' '\n' </proc/$pid/environ|grep MATH_STUDY_PORT|cut -d= -f2); [ "$port" = 4325 ] && kill -9 $pid; done
pkill -9 -f 'astro dev.*4325'; rm -f /tmp/math-noauth.pid
cd web && nohup env DEV_NOAUTH=1 node node_modules/.bin/astro dev --host 127.0.0.1 --port 4325 > /tmp/4325_direct.log 2>&1 &
# 200 될 때까지: until curl -sm3 127.0.0.1:4325/ -o/dev/null -w '%{http_code}'|grep -q 200; do sleep 4; done
```

## 인제스트 파이프라인 (차기 회차 — 검증된 자동 흐름)
```
python scripts/ingest_kice/ingest_auto.py --run [--only <slug>]
  → 감지/스테이징 → 추출+크롭 → 교정[gemma×2 ∥ sonnet검증(캐시) ∥ 재교정]
  → box_backfill → concept_remap → build_solution_cache → post_ingest_sync
```
- 재교정 백엔드: 기본 agy. agy 다운 시 `RECORRECT_BACKEND=agent`. 솔버: auto 사다리 + 단답/killer/도형은 핸드솔브 큐→오케스트레이터 직접([[feedback_handsolve_orchestrator]], 서브에이전트 위임 금지). ★새 회차 적재하면 **위 심링크 재발 주의**.

## 커밋 정책 / 함정
- **main-only + 작업 끝나면 즉시 commit+push**([[feedback_main_only_commit]]). ★이번 세션 교훈: 밤샘 자율빌드 중 commit만 하고 push 누락 22커밋 발생 → 모니터링서 발견·일괄 푸시. **autonomous 작업도 push 챙길 것.**
- 미커밋 debris(내 것 아님, 건드리지 않음): `web/src/pages/dev/{figrender.astro 1줄, goldboard.astro(명시 비커밋 임시도구)}`·`web/public/problem-images/_tmp_*.png`·`concept-illustrations.json`(일일크론) — 다른 작업 산물.
- 서버 stop 금지(setsid·always-on, [[feedback_shutdown_keep_server]]). 서버 뜬 채 `astro check`/`npm install`→Vite stale→`server.sh restart`(또는 dep 재최적화 ~60s 대기). 로그 `>` 덮어쓰기 금지(append/타임스탬프).
- claude -p: clean cwd + `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS=1`(캐시 prefix 안정, [[project_claude_p_caching]]).

## 이전 세션 컨텍스트(요약)
2026-06-23 저녁: 3D 개념도식 전수(84)·수식가독성·오늘의페이지·claude -p DISABLE_GIT(`docs/TODO.md` "완료" 참조). 그 전: 인제스트 캐싱·2019수능 적재·노드다이어트·위젯 자율루프·상용화 하드닝. 상세 git log + 메모리.
