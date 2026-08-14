# CLAUDE.md — math-study 운영 규칙

> 이 파일은 **어느 기계에서 세션을 열든** 자동으로 읽힌다(맥북 원격개발 / tme 직결 공통).
> 여기는 **운영**만 적는다. 거버넌스는 [`agent.md`](agent.md)(Chapter 1~6 + D1~D17),
> 프로젝트 비전은 [`README.md`](README.md), 셧다운 판정 기준은
> [`docs/ops/SHUTDOWN.md`](docs/ops/SHUTDOWN.md) 가 정본이다.

---

## 1. 실행 실체는 tme 하나뿐이다

**서비스·PostgreSQL·크론·백업이 전부 tme 에만 있다.** 맥북에는 편집용 사본만 있다.
DB 는 복제하지 않는다 — 학습 기록·필기·채팅이 들어 있는 유일본이다.

| | 경로 |
|---|---|
| tme (실행 실체) | `/home/insung/math-study` |
| 맥북 (편집 사본) | `/Users/insung/projects/math-study` |
| 원격(GitHub) | `git@github.com:GGAH1911/math-study.git` · 기본 브랜치 `main` |

### 세션 모드 두 가지

- **tme 직결** — tme 에서 Claude Code 를 연다. 편집·실행이 같은 자리라 동기화가 필요 없다.
- **맥북 원격개발** — 맥북에서 편집 → `git push` → tme 에서 `git pull` → 확인.
  맥북에서 tme 접속은 `ssh -o BatchMode=yes tme` 만 쓴다. **tme 에 장기 프로세스를 띄우지 않는다**
  (Claude Code 도 tme 에서 실행하지 않는다). tme 에서는 배포·실행·확인만 한다.

### 어느 기계에서든 같은 명령 — `scripts/ops/on_tme.sh`

```bash
bash scripts/ops/on_tme.sh 'docker compose -f deploy/docker-compose.yml ps'
```

tme 에서는 레포로 `cd` 후 그대로 실행하고, 그 밖에서는 `ssh tme` 로 넘긴다.
헬스체크·게이트는 **전부 이걸 통해서** 부른다. 그래야 프로토콜이 두 벌로 갈라지지 않는다.

> ⚠️ 원격 페이로드는 `bash -c '<...>'` 한 겹으로 감싸져 있다. 날것의 `cd X && cmd` 는
> 중간의 명령 재작성 계층(rtk 래퍼 등)이 선행 `cd X &&` 를 삼켜 cwd 가 홈으로 떨어진다.
> 직접 `ssh tme '...'` 를 쓸 때도 같은 함정을 밟는다 — `cd` 가 필요하면 `bash -c` 로 감싸라.

---

## 2. 코드 변경 반영 흐름

```bash
# 맥북에서
git pull --rebase            # ★먼저. 03:00 크론이 tme 에서 커밋·푸시한다
#   ... 편집 ...
git commit && git push

# tme 에 반영 + 확인
bash scripts/ops/on_tme.sh 'git pull --rebase'
bash scripts/ops/on_tme.sh 'curl -sf "http://127.0.0.1:4324/api/health?deep=1"'
```

**재빌드는 보통 필요 없다.** 지금 도는 건 dev 오버레이라 레포 루트가 컨테이너에
바인드마운트(`..:/app`)돼 있고 `astro dev` 의 HMR 이 `git pull` 을 그대로 집어간다.
의존성(`web/package.json`)이 바뀌었을 때만 재기동한다:

```bash
bash scripts/ops/on_tme.sh 'docker compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml up -d --build web'
```

---

## 3. 서비스 지도 (tme)

| 무엇 | 어디 | 비고 |
|---|---|---|
| 웹앱 (dev 오버레이·HMR) | 컨테이너 `deploy-web-1` · `0.0.0.0:4324` | http://tme.tailf47aa4.ts.net:4324 · `NODE_ENV=development` |
| PostgreSQL | 컨테이너 `deploy-db-1` · `127.0.0.1:5434` | DB/USER `mathstudy` · 16 테이블 · **호스트 인제스트가 psycopg 로 붙는 유일한 경로** |
| 얕은 헬스 | `/api/health` | DB 만 본다 |
| **딥 헬스** | `/api/health?deep=1` | **튜터를 실제 호출**. 호출당 ~$0.00001 |
| dev 서버 (별도) | `server.sh` · `:4323` | 지금 꺼져 있음. watchdog 자동재시작 — **명시적 stop 금지** |
| 시크릿 | `deploy/.env` · `~/.config/math-study/openrouter.key` | 둘 다 커밋 대상 아님 |

> 포렌식 PostgreSQL(`127.0.0.1:5432`)과 **다른 DB** 다. 포트가 갈려 있으니 헷갈리지 말 것.
> `server.sh` 의 `TS_HOST` 기본값(`tme-laptop...`)은 tme 이전 전의 잔재로 낡았다. 실제는 `tme.tailf47aa4.ts.net`.

### 크론 (tme `crontab -l`)

| 시각 | 무엇 |
|---|---|
| 매시 :17 | 튜터 딥 헬스체크 → `/tmp/tutor_health.log` (3회 연속 실패 시 `██` 표시) |
| 03:00 | `widget_spec_loop` — **컨테이너 안에서 git commit → 호스트에서 git push** |
| 04:35 | DB 덤프 → `~/backups/math-study/` + 원격 · 30일 로테이션 |
| 월 05:20 | 백업 **복구 리허설** (빈 DB 복원 검증) |
| 23:40 / 06:00 / 12:00 | 일일 삽화 생성 |

★**03:00 크론이 `main` 에 커밋·푸시한다.** 그래서 push 전에는 반드시 `git pull --rebase` 한다.

---

## 4. 부팅 / 셧다운

`.session-protocol.yml` 에 기계가 읽는 형태로 박혀 있다(session-lifecycle 스킬).
사람이 읽는 판정 기준·사고 이력은 `docs/ops/SHUTDOWN.md`.

**부팅** — ① `docs/TODO.md` + `docs/architecture/app-roadmap.md` + 최신
`docs/handover/{YYYY}/{MM}/{DD}_session.md` 의 「차기 과제」·「잔류 리스크」를 읽는다
② 컨테이너 2종 + 얕은/딥 헬스 확인 ③ `git status` · 래칫 · sympy 헤더 미리보기 ·
**돌고 있는 배치 확인** ④ 브리핑.

**셧다운** — ① 배치·크론이 끝났는지 확인 ② 핸드오버 **append**(덮어쓰기 금지) + TODO·로드맵 갱신
③ 게이트(래칫 · sympy 헤더 · 딥 헬스) ④ 커밋 → `pull --rebase` → push(확인 후)
⑤ 완료/잔류 리스크/차기 과제 구분 보고.

> 돌고 있는 배치 확인은 `pgrep` 결과를 믿지 말고 `/proc/<pid>/cmdline` 을 읽는다.
> `pgrep` 이 **자기 명령줄을 물어** 오판한 적이 있다(2026-08-13).

---

## 5. 절대 규칙 — 전부 실제 사고에서 나왔다

- **dev 서버·컨테이너를 멋대로 멈추지 않는다.** 사장님이 학습 중일 수 있다.
  셧다운은 세션 종료지 전원차단이 아니다.
- **파괴적 작업 전에 백업한다.** 지우거나 덮기 전에 대상 테이블을 `pg_dump`.
  2026-08-13 에 `problem_state` 를 백업 없이 전삭제해 야간 백업으로 겨우 복구했다.
- **파일을 고치는 코드는 쓰기 전에 검사한다.** 정규식 하나로 218KB → 309바이트가 된 적,
  `concepts` 형식 오판으로 YAML 이 깨져 **사이트가 2번 멈춘** 적이 있다.
  핵심 필드가 살아 있는지 확인하고서 쓴다.
- **형식은 하나가 아니다.** 같은 필드가 `concepts: [a, b]` · 블록 리스트 · 키 없음
  세 형태로 존재한다. 한 형태만 가정한 정규식이 위 사고들의 공통 원인이다.
- **얕은 헬스 200 을 믿지 않는다.** 2026-08-12 에 `/api/health` 는 15시간 내내 200 인데
  튜터는 죽어 있었다. 튜터를 봤다고 말하려면 `?deep=1` 을 부른다.
- **sympy 헤더는 브라우저가 1차다.** `pyodide-worker.js` 를 안 고치고 `api/sympy.ts` 만
  고치면 사용자에겐 아무 변화가 없다.
- **시크릿을 커밋하지 않는다.** `deploy/.env`, `openrouterkey.txt` 는 `.gitignore` 에 있다 — 유지한다.

### 맥북 사본 고유 주의

`incoming/processed/` 의 스크린샷 2개는 인덱스에 **NFD(자모 분해)** 로 들어 있어,
macOS(`core.precomposeunicode=true`)에서는 영구히 `??` 로 뜬다. 정상이다.
**절대 `git add -A` 로 쓸어 담지 않는다** — NFC 중복본이 생긴다. 스테이징은 경로를 지정해서 한다.

---

## 6. 문서 지도 — 무엇이 어디의 SSOT 인가

| 파일 | 무엇의 SSOT |
|---|---|
| `agent.md` | 거버넌스 헌법 (Chapter 1~6 + 수학 도메인 D1~D17) |
| `docs/architecture/app-roadmap.md` | **무엇을 어떤 순서로** (날짜 없음 · 게이트 판정) |
| `docs/TODO.md` | 미룬 일 + **판정 근거** (다음 세션이 다시 재지 않게) |
| `docs/ops/plans/{active,pending,backlog,completed}/` | 계획 생애주기 — 폴더가 곧 상태 |
| `docs/handover/{YYYY}/{MM}/{DD}_session.md` | 그 세션의 서사·차기 행동 (**Append-Only**) |
| `docs/log.md` | 한 줄 작업 원장 |
| `docs/ops/SHUTDOWN.md` | 셧다운 판정 기준·사고 이력 |
| `~/.claude/.../memory/` (레포 밖) | 세션 간 교훈 — 레포에 중복 기록하지 않는다 |

> 루트 `HANDOFF.md`(2026-06-06)와 `lifecycle.md`(LWIP 표준 게이트)는 **낡았다**.
> 현재 상태는 `docs/TODO.md` + `docs/architecture/app-roadmap.md` + `git log` 를 본다.
