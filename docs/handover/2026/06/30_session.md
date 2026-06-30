# 2026-06-30 세션 핸드오버 — math-study 를 tme 서버로 이전

> ★다음 세션은 **tme 서버에서** 시작한다(`ssh tme && cd ~/math-study && claude`). tme-laptop 은 은퇴 진행 중.

## 부트 / 상태 점검 (tme 세션 기준)
```bash
cd ~/math-study
git rev-parse --short HEAD          # origin/main 과 같아야
cd deploy && docker compose ls       # "deploy" 프로젝트 db+web 둘 다 running(healthy) 이어야
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:4324/api/health   # 200
```
- 접속: **http://100.67.69.121:4324** (Tailscale). 로그인 hwangi0404@gmail.com.
- **현재 dev 모드**(astro dev + 소스 바인드마운트) → 코드 편집/`git pull` 시 **HMR 즉시반영**(재빌드 X).

## 이번 세션에 한 일
**1) math-study 를 tme-laptop → tme 서버로 이전(자가호스팅).** tme(100.67.69.121, 12코어/24GB, 상시가동)는 부동산 포렌식(출시 전)도 같이 도는 사장님 서버. 둘 다 정식 출시 예정 → mem_limit 격리(web 6g/db 4g)·DB 내부 노출만으로 공존.
- 위치 **`~/math-study`** (★`~/projects` 는 포렌식 레포라 거기서 분리함). `deploy/` 에 compose + `.env`(미커밋).
- db=postgres16 컨테이너(볼륨 deploy_ms_pgdata), web=astro(claude CLI 내장 + `~/.claude` 마운트로 구독인증·캐싱).
- DB 이전: laptop 5434 → plain SQL 복원. **problems 4944·users 3** 등 정상.
- 콘텐츠 크론(그림×3·위젯×1) laptop 정지 → **tme crontab 이전**(node+claude, DB불요). gen_daily 실행검증 OK.

**2) 이전 중 잡은 prod-only 버그 + UI 픽스 (커밋들):**
- `1b2629d4` CSRF 403 로그인 불가 — isSameOrigin 을 Host 헤더 기준으로(@astrojs/node standalone 이 request.url 을 localhost:8080 으로 잡던 문제). **dev엔 없고 prod빌드에만 나던 대표 환경차 버그.**
- `650d6ec3` Dockerfile: claude CLI 설치 + problem-images 심링크(→db/raw) 실파일로 풀기.
- `93e8d96a` 재빌드 5.5분 단축(chown -R 제거·claude 캐시화). `8bda430f` dev 모드(즉시반영).
- `5ba88439` 복습 리스트 slug 중복 key 경고 — 프론트 dedupe + **DB 중복 problems 272행 제거**(laptop·tme 양쪽, user데이터 무손실).
- 그 외(이전 세션 연속): KaTeX 인라인 lim/∑ 첨자 쌓기, 드래그 인용 분수깨짐(recoverBareMath annotation 오염 근본수정), 모바일 인용 버튼 portal·핸들유지.

## 운영 명령 (tme)
```bash
cd ~/math-study/deploy
# dev(즉시반영, 현재):  docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build web
# prod(빌드, 출시용):   docker compose -f docker-compose.yml up -d --build web
docker compose logs -f web        # 로그
```
코드 반영: tme에서 편집(HMR) 또는 `cd ~/math-study && git pull`. 커밋/푸시도 tme에서(git SSH OK).

## 남은 일 (우선순위)
1. **exams 테이블 중복 정리(권장)** — 같은 회차가 두 agency로 들어가 분산(검정고시가 검정원·평가원 양쪽=평가원 오기). 회차별 정답 agency로 problems repoint + 잘못된 exam 삭제 + 인제스트 agency 정규화(재발방지). *콘솔에러 자체는 이미 해결(problems dedup).*
2. **출시 전 prod 빌드 모드 전수검증** — 지금 dev 모드는 prod-only 버그(CSRF류)를 가림. 출시 직전 `up -d --build`(빌드모드)로 전환해 로그인·튜터·인용·그래프·필기 재검증 필수.
3. **TLS 리버스 프록시 + 도메인** → `MS_SECURE_COOKIES=true`. (지금 http 직접접속이라 false)
4. **자동 백업**(db 일일 pg_dump) + **단일장애점 대비**(한 박스에 두 서비스).
5. 튜터 다중유저 정식화 시 claude CLI → Anthropic API(메모리 출시 차단요소).
6. tme-laptop 완전 은퇴: dev서버 4323/4324/4325(전환기간 fallback 유지 중)·agy keepalive·cta-law/lwip(별도 프로젝트)는 따로.

## 주의/교훈
- **dev/prod 환경차로 동작 갈라질 수 있음**(CSRF가 증거). "완전 똑같다" 가정 금지 — prod 모드로 따로 검증.
- compose 프로젝트명 "deploy"(폴더명). 볼륨 deploy_ms_pgdata/devnode. 위치 옮겨도 폴더명 같으면 볼륨 보존.
- tme-laptop(이 핸드오버 작성 머신) dev서버는 **끄지 않음**([[feedback_shutdown_keep_server]]). MacBook OCR/gemma 비전 별개 유지.
- 상세: 메모리 `project_tme_deploy`.
