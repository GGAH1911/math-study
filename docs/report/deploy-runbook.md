# 배포 런북 — Railway (Render 대안 포함)

math-study 웹앱(`web/`, Astro + `@astrojs/node` standalone)을 관리형 PaaS 에 배포하는
턴키 절차다. 실제 프로비저닝은 사장님이 하고, 이 문서는 그대로 따라할 수 있게 한 줄씩
정리한 가이드다.

전제 산출물(이미 레포에 있음):
- `web/Dockerfile` — node 22 멀티스테이지 빌드 + 런타임에 python3/sympy 설치.
- `/.dockerignore` (레포 루트) — Docker 가 실제로 읽는 무시 목록.
- `web/.env.example` — 필요한 환경변수 전체.
- `web/src/pages/api/health.ts` — `GET /api/health` 헬스체크(DB ping).
- `.github/workflows/ci.yml` — push/PR 시 `astro check` + `astro build` 게이트.

> ★핵심 주의 1 — **빌드 컨텍스트는 레포 루트**여야 한다. `web/package.json` 의
> prebuild 와 `astro.config.mjs` 가 `../docs`(개념/문제 마크다운, 자산)를 읽기 때문.
> 그래서 Dockerfile 경로만 `web/Dockerfile` 로 지정하고 컨텍스트는 루트로 둔다.
> Railway/Render 의 Dockerfile 배포는 기본적으로 레포 루트를 컨텍스트로 잡으므로
> Root Directory 를 `web` 로 바꾸지 말 것(바꾸면 docs 가 사라져 빌드 실패).
>
> ★핵심 주의 2 — **재인제스트 금지 함정과 무관하게** 이 배포는 읽기 빌드만 한다.
> DB 스키마는 마이그레이션(4단계)으로 따로 적용한다.

---

## 1) GitHub 연결

1. Railway 대시보드 → **New Project** → **Deploy from GitHub repo** 선택.
2. `math-study` 레포와 `main` 브랜치를 연결한다.
3. 서비스가 생성되면 **Settings → Build**:
   - **Builder**: `Dockerfile` 선택.
   - **Dockerfile Path**: `web/Dockerfile` 입력.
   - **Root Directory**: 비워둔다(= 레포 루트). ★`web` 로 설정하지 말 것.
4. **Settings → Deploy**:
   - **Start Command**: 비워둔다(Dockerfile 의 `CMD` 사용).
   - **Health Check Path**: `/api/health` 입력. **Health Check Timeout**: 30s 정도.

---

## 2) 관리형 Postgres 추가 → DATABASE_URL

1. 같은 프로젝트에서 **New → Database → Add PostgreSQL**.
2. 생성되면 Postgres 서비스의 **Variables** 탭에서 `DATABASE_URL`(또는 개별
   `PGHOST/PGUSER/...`)을 확인한다. Railway 는 내부 참조 변수
   `${{ Postgres.DATABASE_URL }}` 를 제공한다.
3. 이 값을 **웹 서비스**의 env 로 매핑한다(3단계에서).
   - Railway 관리형 PG 는 SSL 이 필요할 수 있다 → 접속 문자열 끝에
     `?sslmode=require` 를 붙인다.

---

## 3) 환경변수 설정 (`web/.env.example` 참조)

웹 서비스 → **Variables** 에 아래를 넣는다(값은 예시).

| 변수 | 값 | 비고 |
|---|---|---|
| `MATH_STUDY_DATABASE_URL` | `${{ Postgres.DATABASE_URL }}?sslmode=require` | ★없으면 프로덕션 기동 실패(의도된 가드) |
| `MATH_STUDY_SECURE_COOKIES` | `true` | HTTPS 전용 쿠키 |
| `NODE_ENV` | `production` | 프로덕션 가드/최적화 |
| `HOST` | `0.0.0.0` | 컨테이너 외부 노출 |
| `PORT` | (비워둠/플랫폼 주입) | Railway 가 동적 주입 → standalone 이 읽음. 하드코딩 금지 |

- `web/.env.example` 의 "향후" 섹션(LLM 키·결제·OAuth)은 지금 채울 필요 없다.
- ★`PORT` 는 Railway 가 주입하는 값을 그대로 쓰게 두는 게 안전하다. Dockerfile 은
  미주입 시 8080 으로 폴백한다.

---

## 4) 마이그레이션 실행

DB 스키마(`db/migrations/0001_init.sql` … `0003_membership.sql`)는 앱 기동과 별개로
한 번 적용해야 한다. 멱등(IF NOT EXISTS)이라 재실행해도 안전하다.

방법 A — 로컬에서 원격 DB 로 (가장 간단):
1. Railway Postgres 의 **public** 접속 문자열을 복사(대시보드 → Connect).
2. 로컬에서 `psql` 보유 상태로:
   ```sh
   MATH_STUDY_DATABASE_URL='postgresql://...@...railway.app:5432/railway?sslmode=require' \
     ./db/migrate.sh
   ```
   `migrate.sh` 가 `db/migrations/*.sql` 을 순서대로 `psql` 로 적용한다.

방법 B — Railway CLI 로:
1. `railway login` → `railway link`(해당 프로젝트 선택).
2. `railway connect Postgres` 로 psql 셸을 열고 각 `.sql` 을 `\i` 로 실행,
   또는 `railway run ./db/migrate.sh`(이 경우 `DATABASE_URL` 이 주입되지만
   `migrate.sh` 는 `MATH_STUDY_DATABASE_URL` 을 보므로
   `railway run sh -c 'MATH_STUDY_DATABASE_URL=$DATABASE_URL ./db/migrate.sh'`).

> 마이그레이션은 새 컬럼/테이블 추가 시마다 다시 돌린다. 콘텐츠(문제/개념)는
> 마크다운 + 빌드 산출물이라 DB 마이그레이션과 무관하다.

---

## 5) 커스텀 도메인 + 자동 TLS

1. 웹 서비스 → **Settings → Networking → Custom Domain** → 도메인 입력
   (예: `mathstudy.example.com`).
2. Railway 가 제시하는 `CNAME` 레코드를 도메인 DNS 에 추가한다.
3. DNS 전파 후 Railway 가 Let's Encrypt 인증서를 **자동 발급/갱신**한다(수동 작업 없음).
4. 임시로는 Railway 가 주는 `*.up.railway.app` 서브도메인으로도 즉시 HTTPS 접속 가능.

> 커스텀 도메인 적용 후 `MATH_STUDY_SECURE_COOKIES=true` 와 HTTPS 가 맞물려야
> 로그인 쿠키가 정상 동작한다(이미 3단계에서 설정).

---

## 6) /api/health 확인

배포 완료 후:
```sh
curl -s https://<도메인>/api/health | jq .
```
기대 응답(정상):
```json
{ "status": "ok", "db": "ok", "uptime": 12, "ts": "2026-..." }
```
- `status: "ok"`, HTTP 200 → 앱 + DB 정상.
- HTTP 503, `db: "down"` → DB 접속 실패. `MATH_STUDY_DATABASE_URL`/sslmode/마이그레이션을
  점검한다. `db_error` 필드에 원인 메시지가 담긴다.
- `/api/health` 는 미인증 공개 라우트(middleware PUBLIC_PATHS)라 로그인 없이 호출된다.
- Railway Health Check Path 를 `/api/health` 로 잡아두면 배포 시 자동 검증된다.

---

## 7) Render 대안 메모

Render 도 동일 Dockerfile 로 배포 가능(거의 동등):

1. **New → Web Service** → GitHub 레포 연결.
2. **Runtime**: `Docker`. **Dockerfile Path**: `web/Dockerfile`.
   **Docker Build Context Directory**: `.`(레포 루트 — ★중요, `web` 아님).
3. **New → PostgreSQL** 로 관리형 DB 생성 → **Internal Database URL** 복사.
4. 웹 서비스 **Environment** 에 3단계 표와 동일하게 입력
   (`MATH_STUDY_DATABASE_URL` = Render 의 Internal Database URL, 끝에 `?sslmode=require`).
   - Render 도 `PORT` 를 주입한다 → 하드코딩하지 말 것.
5. **Health Check Path**: `/api/health`.
6. 마이그레이션은 4단계 방법 A(로컬 psql + External Database URL) 그대로.
7. 커스텀 도메인 + 자동 TLS 도 Render 가 동일하게 Let's Encrypt 로 처리한다.

차이점:
- Render 무료 플랜은 유휴 시 슬립(cold start) — 헬스체크 프로브가 깨워도 첫 응답 지연.
- Railway 는 사용량 과금, Render 는 인스턴스 플랜 과금. 트래픽 패턴에 맞춰 선택.

---

## 부록 — 로컬에서 프로덕션 이미지 검증(선택)

배포 전 Dockerfile 이 도는지 로컬에서 확인:
```sh
# 컨텍스트는 레포 루트, Dockerfile 만 web/ 지정.
docker build -f web/Dockerfile -t math-study .

# 로컬 PG 가 있다면 그 URL 로(없으면 503 으로 떠도 컨테이너 기동 자체는 확인됨).
docker run --rm -p 8080:8080 \
  -e NODE_ENV=production \
  -e MATH_STUDY_DATABASE_URL='postgresql://user:pass@host:5432/db?sslmode=require' \
  -e MATH_STUDY_SECURE_COOKIES=true \
  math-study

curl -s http://127.0.0.1:8080/api/health | jq .
```
sympy 동작까지 보려면 컨테이너 안에서 `/app/.venv/bin/python -c "import sympy; print(sympy.__version__)"`.
