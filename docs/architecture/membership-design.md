# 회원관리 시스템 (멤버십) — 설계 & 구현

> 2026-06-09 야간 자율 구축. 브랜치 `claude/membership-system`. 결정: 이메일+비번 인증
> (지금 동작) + Google OAuth 슬롯, 튜터 백엔드 현행 유지(API 직결은 나중), 로그인 필수 +
> 첫 가입이 기존 single-user 데이터 상속.

## 1. 무엇이 동작하나 (요약)

- **이메일+비밀번호 인증** — 가입·로그인·로그아웃 완전 동작 (scrypt 해싱).
- **로그인 게이팅** — 로그인 안 하면 모든 페이지가 `/login` 으로. API 는 401.
- **세션** — DB 백업(쿠키=랜덤토큰, DB=sha256). HttpOnly·SameSite=Lax. 30일.
- **사용자별 데이터** — 진도(problem_state)·시도(attempts)·개념숙달(concept_mastery)·
  대화이력(chat_history)·학습프로필(user_profile) 전부 user_id 키.
- **첫 가입 데이터 상속** — 첫 실가입 계정이 기존 single-user 의 진도+mastery 를 인수.
- **학습자 모델** — 정량(개념숙달 기반 frontier 학년) + 정성(목표·약점·페이스)을 튜터
  프롬프트에 per-user 주입(학년 하드코딩 0).
- **대화 이력 계정화** — localStorage → DB(기기 넘어 유지, 캐시 손실 취약점 해소).
- **Google OAuth 슬롯** — 코드 완성, 자격증명 꽂으면 동작(현재 graceful 비활성).

## 2. 아키텍처

```
요청 → middleware.ts (세션쿠키→locals.user, 게이팅, CSRF Origin검증)
         ├─ 미인증 + 보호경로 → /login 리다이렉트 (API는 401)
         └─ 인증 → 페이지/엔드포인트 (locals.user.id 로 per-user)
```

- **`lib/auth.ts`** — 비번 해싱(`crypto.scrypt`, 의존성 0), DB세션(createSession/
  getUserBySessionToken/destroySession), 쿠키 헬퍼, CSRF(isSameOrigin), 레이트리밋
  (isThrottled/recordAuthFailure), 더미해시(타이밍 안전).
- **`middleware.ts`** — 전역. 자산/dev모듈 스킵, POST/PUT/PATCH/DELETE Origin 검증,
  세션 해석(fail-safe), 보호경로 게이팅. 공개: `/login`,`/signup`,`/api/auth/*`,`/api/health`.
- **`lib/user-claim.ts`** — 첫 가입 시 legacy(SINGLE_USER_ID) 데이터 인수 + frontmatter
  mastery 시드. 멱등(is_legacy 플래그 FOR UPDATE 잠금).
- **`lib/mastery.ts`** — concept_mastery read/write(per-user).
- **`lib/learner.ts`** — 학습자 모델(정량 도출 + 정성 프로필) → 튜터 프롬프트 문자열.

### ★ 중요: prerender → SSR
정적(prerender=true) 페이지는 **프로덕션에서 미들웨어가 안 돌아** 인증 게이팅이 불가
(개발에선 빈 request). 그래서 14개 페이지를 `prerender=false`(SSR)로 전환했다. 인증
게이팅을 받는 모든 페이지는 SSR 이어야 한다.

## 3. DB 스키마 (migration 0003)

| 테이블 | 용도 |
|---|---|
| `users` | 계정. email(lower 유니크)·password_hash(scrypt)·oauth slot·is_legacy |
| `sessions` | DB세션. token_hash=sha256(쿠키토큰) → DB유출돼도 위조불가 |
| `concept_mastery` | (user_id, concept_id) 개념숙달 — frontmatter 전역값 대체 |
| `user_profile` | 정성 학습자 프로필(목표·약점·페이스) |
| `chat_history` | (user_id, collection, slug) 대화 메시지 |
| `auth_throttle` | 로그인 브루트포스 방어 |

기존 `problem_state`·`problem_attempts` 에 users FK 추가. legacy 플레이스홀더 유저
(SINGLE_USER_ID)로 기존 행 흡수 후 첫 가입이 인수. 적용: `./db/migrate.sh` (멱등).

## 4. 보안 조치

- 비번: `crypto.scrypt`(N=2^14) + per-password salt + `timingSafeEqual`. 포맷에 파라미터
  박아 추후 상향 가능.
- 세션: 쿠키엔 랜덤 32B 토큰, DB엔 sha256(token). HttpOnly·SameSite=Lax. 로그아웃 시 DB 삭제.
- CSRF: SameSite=Lax + state-changing 요청 Origin 동일출처 검증(미들웨어).
- 계정열거 방지: 로그인 실패 메시지 동일 + 유저 없어도 더미해시로 동일 타이밍.
- 레이트리밋: 이메일·IP 각각 8회/15분 → 15분 잠금.
- 권한: 모든 per-user 엔드포인트가 `locals.user.id` 만 사용(요청 바디 user_id 불신).
- SQLi: postgres.js 태그드 템플릿(파라미터화). jsonb 는 `sql.json()`.
- open redirect 방지: returnTo 는 동일출처 상대경로만(클라이언트 검증).
- OAuth: state CSRF, email_verified 강제.

## 5. 남은 것 / 사장님이 할 것

1. **첫 가입** — 깨어나서 `/signup` 으로 본인 계정 생성. 그 즉시 기존 진도·mastery 상속.
   (보안상 제가 계정/비번을 미리 만들지 않았습니다.)
2. **Google OAuth 켜기**(선택) — Google Cloud OAuth 앱 만들어 env 설정:
   `GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET`,
   (선택)`GOOGLE_OAUTH_REDIRECT_URI`. 그러면 로그인 페이지에 Google 버튼 자동 노출.
3. **프로덕션 튜터 백엔드** — 현재 `chat.ts` 는 노트북 `claude` CLI spawn(단일프로세스).
   다중 사용자 서비스엔 Anthropic API 직결 필요(키·과금). 회원관리·아이패드 공통 차단요소.
4. **HTTPS 배포** — 공개 배포 시 `MATH_STUDY_SECURE_COOKIES=true`(Secure 쿠키) 설정 +
   HTTPS. 현재 Tailscale HTTP 라 Secure=false.
5. **이메일 인증/비번재설정**(선택) — 현재 없음. 프로덕션엔 이메일 프로바이더 필요.
6. **학습자 프로필 자동갱신**(follow-up) — 현재 튜터가 프로필을 *읽음*. 튜터가 약점을
   *자동 기록*하려면 ChatPanel 에 profile-update 펜스 파싱 wiring 필요(엔드포인트는 완성).

## 6. 환경변수

| 변수 | 기본 | 용도 |
|---|---|---|
| `MATH_STUDY_DATABASE_URL` | localhost:5434 | Postgres |
| `MATH_STUDY_SECURE_COOKIES` | (false) | HTTPS 시 'true' |
| `GOOGLE_OAUTH_CLIENT_ID/SECRET` | (없음) | Google 로그인 |
| `MATH_STUDY_USER_ID` | (legacy UUID) | (구) single-user — 이제 미사용 |
