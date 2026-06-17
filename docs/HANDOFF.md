# 핸드오프 — 2026-06-17 · UI/UX + 오늘의 페이지 + 튜터 그래픽/렌더 정비

> 다음 세션이 바로 이어받도록: 현재 상태 / 한 일 / 검증 / 남은 일 / 함정.

## 현재 상태
- **브랜치·커밋**: `origin/main` (모든 작업 커밋·푸시 완료, 미푸시 0). main에서 직접 작업.
- **dev 서버**: `0.0.0.0:4323` 실행 중 (setsid+watchdog 분리 — **끄지 말 것**, `./server.sh status`로 확인만).
  http://tme-laptop.tailf47aa4.ts.net:4323 · http://100.124.146.14:4323 . 인증 게이팅(비로그인 302).
- **크론**: 사용자 crontab `40 23 * * *` — `gen_daily_illustration.mjs 0 1 2` 로 '오늘의 개념' 그림 미리 생성.

## 이번 세션 한 일 (전부 커밋·푸시됨)
**UI/UX (모바일/태블릿/데스크탑)**
- 튜터 채팅 스크롤바 → 커스텀 드래그(네이티브 모바일 스크롤바는 못 잡음).
- 컨텍스트 서랍 모바일: **탭 열기 + 위/아래 스와이프 + 그래버형 손잡이**(OS 홈제스처 충돌 해소). 데스크탑·태블릿 우측 손잡이에 세로 그래버.
- 브랜드 통일: 사이드바·모바일헤더·favicon = **빨간 작도 인장**(삼각자 이모지·점박스 favicon 폐지).
- 테마 토글: ✒/✏ → **해/달 인라인 SVG**.
- 튜터 채팅 **FAB**: 개념노드=전 화면 FAB / 문제풀이=md+ 인라인 컬럼·모바일 FAB / 홈(학습 길잡이)=FAB(**태블릿 미표시 버그 수정**). 데스크탑 FAB는 본문 우측 가장자리에 hug. **데스크탑·태블릿은 백드롭 제거** → 채팅 열어둔 채 그래프 패널 동시 조작(모바일은 풀시트 유지).
- 좌측 메뉴 breakpoint `lg→xl`: 태블릿(≤1279)도 ☰ 버튼, 사이드바는 ≥1280만.

**오늘의 페이지(히어로)**
- 매일 새 **개념**(전체 풀 ~2800에서 `daily-concept.mjs` 고정셔플 순회, 수년치 무중복) + **개념 인사이트 한 줄**(blurb).
- 개념별 **그림**: LLM(Sonnet)이 손그림용 stroke 좌표(figure spec)+blurb 생성 → `web/src/data/concept-illustrations.json` 에 개념 id로 캐시. 크론이 내일치 미리 생성. `PaperHero`가 손그림 애니메이션 렌더(곡선=Catmull-Rom 스플라인, **좌표축 제거**). spec 없으면 일반 곡선 폴백.
- 갤러리(관리자): `/dev/daily-figures`.

**튜터 그래픽 프로토콜 / 렌더**
- 도형 단계검증(STEP A의존그래프→B:sympy계산·assert→C:emit→D:비전) 트리거를 `'문제 재현'→'좌표 정확성 필요한 도형 전반(개념 설명 포함)'`로 확장.
- ★ **Haiku 비순응 차단**: 첫 응답에 python+그래픽이 같이 오면 `ChatPanel`이 미검증 그래픽을 strip → sympy 검증 루프가 돌아 STEP C에서 검증 좌표로 재작도(이전엔 `hasGeometry break`로 검증 스킵돼 추정 좌표 노출).
- KaTeX: `\text{}` 안 수학 관계 유니코드(≠ → × ÷ ± ≤ ≥ ⇒ ≈ ∈ …) → `$\ne$` 같은 math 섬(text mode hard-throw 방지). `katex-normalize.mjs`.
- ASCII/박스드로잉 표(코드펜스 ``` 안 포함) → 진짜 HTML 표. `markdown.tryParseTable` + `ChatPanel` 펜스 분기.

## 검증
- `cd web && node scripts/katex-harness.mjs` → **12/12** (≠ 관계기호 회귀 케이스 포함).
- 헤드리스 chromium(CDP) 관측 다수 — 스크롤바 드래그, 서랍 탭/스와이프, FAB breakpoint, 그림 렌더 등.
- 캐시 시드 11종 + 추가분 `/dev/daily-figures`에서 육안 확인.

## 남은 일 / 다음 단계  (상세는 `docs/TODO.md` "완료/잔여 2026-06-17")
- **concept-illustrations.json**: 크론이 매일 갱신 → 워킹트리 주기적 dirty(정상). 주기적 커밋 or gitignore 정책 결정.
- 히어로 figure 일부 약함(예: 조건부명제) → 캐시에서 그 id 삭제 후 `node web/scripts/gen_daily_illustration.mjs <offset>` 재생성.
- `atlas`(개념 지도) 대시보드 채팅은 아직 인라인(홈만 FAB화) → 통일 검토.
- Haiku 단계검증 비순응 모니터(turn-1 strip로 강제 중이나 완벽치 않음).

## 함정 (gotchas)
- **서버 stop 금지** — setsid+watchdog 분리. `status`로만 확인. dev 캐시 footgun: 서버 뜬 채 `astro check`/`npm install` → Vite stale → `server.sh restart`.
- **크론 의존**: `~/.local/bin/claude`(PATH) + `~/.claude/.credentials.json`(세션 env 토큰 없이 동작). 모델 변경=`FIGURE_MODEL` env(기본 sonnet).
- **KaTeX 깨짐 진단**: 추측 말고 `web/`에서 실제 katex로 재현(throw 메시지 확인) → `katex-harness.mjs`로 회귀 0 확인 후 고친다. [[project_tutor_katex_robustness]]
- **히어로 곡선 흔들기 금지**: 진폭·주기·표준편차 흔들면 정규분포 등 왜곡(폐기한 접근). 곡선은 정준 모양 + 스플라인만.
- 관련 메모리: `project_daily_concept_hero`, `project_tutor_katex_robustness`, `feedback_shutdown_keep_server`.
