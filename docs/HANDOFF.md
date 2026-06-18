# 핸드오프 — 2026-06-18 · 개념 도식 생성 파이프라인 + Sonnet QA + 렌더러 정비

> 다음 세션이 바로 이어받도록: 현재 상태 / 한 일 / 검증 / 남은 일 / 함정.
> (이전 세션 UI/UX·오늘의 페이지 핸드오프는 git 히스토리·`docs/TODO.md` 참조.)

## 현재 상태
- **브랜치·커밋**: `origin/main`, 전부 커밋·푸시 완료(미푸시 0). main에서 직접 작업.
- **dev 서버**: `0.0.0.0:4323` 실행 중 (setsid+watchdog 분리 — **끄지 말 것**, `./server.sh status`로만 확인).
- **LLM 크론**: 한도 절약으로 **월요일(2026-06-22 03:30)까지 OFF**, 자동재개 타이머 설정됨.
- **도식 캐시** `web/src/data/concept-figures.json`: 총 ~346개. **도형(geometry) 도메인 완료**(생성+Sonnet QA, 168 수정). **함수(functions) 도메인 7/502 생성 후 일시정지**(한도 고려·사용자 보류).

## 이번 세션 한 일 (전부 커밋·푸시됨)
**개념 도식 파이프라인 (신규)**
- `web/scripts/gen_concept_figures.mjs`: 개념별 "좌표정확+축숨김" Geometry spec 을 **haiku 단계별(STEP A~D, sympy 검증)** 생성 → 캐시. 동시성 풀, 3D 자동제외(`is3D`), 멱등 스킵, `FIGURE_CACHE` 출력경로 오버라이드.
- 개념 페이지(`concepts/[...slug].astro`): 도식을 **제목→요약 다음, 본문 직전**에 배치(inline 스크립트가 하이드레이션 전 relocate).
- `dev/concept-figures.astro`(갤러리)·`dev/figrender.astro`(단일 도식 고정폭 렌더 하네스).
- **Sonnet QA** `web/scripts/qa_concept_figures.mjs`: 도식별 고정폭 실제크기 렌더 스샷 + sympy 로 평가 → 문제 있으면 스펙을 그 자리에서 교정해 캐시 기록. 멱등(`qa.checked`).

**렌더러 수정 (Geometry.tsx — 튜터·문제 figure 에도 공통 적용)**
- 각 호: 외각(반사각) 버그 → **내각(소호)** 만(픽셀좌표 기준 large-arc=0).
- 직각: 호 대신 **정사각형 마커**(두 팔 수직 자동 판정).
- 라벨: 다각형 꼭짓점은 **도형 바깥**(무게중심 반대)·좌표점 밀착, de-overlap MAXSHIFT 축소.
- **`**`(Python 거듭제곱) → `^` 정규화**: mathjs 가 `**` 거부 → 곡선 silent 소실. `_normalizeMathExprStr`에서 결정적 보정(개념·튜터·문제 전부).

**QA 교훈 환류 (haiku 첫패스 품질↑ → 비싼 QA 의존↓)**
- QA 272건 수정사유 분석 → 빈발 top5(showAxes·라벨겹침·range·라벨누락·충실성) + `**` 규칙을 **생성 프롬프트 자가점검** + **튜터 `GRAPHICS_GUIDE`** 양쪽에 박음.

**튜터 기타**
- `api/chat.ts`: 개념 노드에 **연결된 기출 메타데이터를 서버가 프롬프트에 주입**(LLM 은 여전히 `--tools ""` 샌드박스, DB 접근 0).

## 검증
- 헤드리스 렌더 확인: 닮음(A,B,C∼A'B'C' 간격·프라임)·단위원·직각삼각형(직각 정사각형+45°호)·격자점(parametric)·극곡선의 미분(P 큰 r+접선)·동위각엇각(∠ 교정)·곡선의 접촉(t*t 곡선 복원). tsc 0 에러.

## 남은 일 (우선순위)
1. **함수 도메인 도식 재개** (7/502, 일시정지). 개선 프롬프트로 생성 → **스팟체크 QA(~25개)**로 충분(전수 Sonnet QA 불필요). ⚠️**한도 부담 큼**(함수는 도형보다 ~50% 큼). 명령: `node scripts/gen_concept_figures.mjs --domain functions --concurrency 4` (백그라운드, 로그 `/tmp/ingest_logs/concept_figures_fn.log`). 끝나면 무작위 QA: `node scripts/qa_concept_figures.mjs <ids> --concurrency 2`.
2. **3D/공간 76개**: `Geometry3D` 생성 파이프라인 신규 구축 필요(현재 2D 만, `--include-3d` 로 대상은 잡힘).
3. **dev 라우트 재게이팅**: `middleware.ts` PUBLIC_PATHS 의 `/dev/concept-figures`·`/dev/figrender` 는 **TEMP 공개**(헤드리스 검증용) — 도식 작업 끝나면 admin 게이팅으로 되돌릴 것.
4. (선택) equations·algebra·prob-stats 도메인 — 도식친화도 낮아 후순위.

## 함정 (반드시 숙지)
- **캐시 write 경합**: gen 과 QA 둘 다 `concept-figures.json` 통째로 씀 → **동시 실행 금지**. QA 중 단건 생성은 `FIGURE_CACHE=/tmp/x.json` 으로 따로 → 끝나고 머지.
- **헤드리스 폭 과소측정**(240 floor): 실제크기 렌더는 `fixedWidth`(=figrender 하네스). 개념 **페이지**는 튜터 island 때문에 헤드리스가 멈춤 → figrender 나 SSR HTML 구조로 검증.
- **QA timeout**(Sonnet >300s, 복잡 도식): 서브에이전트 반복 재시도 말고 **오케스트레이터가 직접** 렌더 보고 스펙 수정(동위각엇각 사례).
- **zsh**: `$VAR` 미분할 → `${=VAR}` 또는 `bash -c`.
- **로그**: 재시작 시 `>` 덮어쓰기 금지(이전 로그 소실) — 새 파일/`>>`. QA 결과는 캐시 `qa` 필드에 영구 보존되니 로그 잃어도 재구성 가능.
- **서버 stop 금지** — setsid+watchdog. `status`로만. 서버 뜬 채 `astro check`/`npm install` → Vite stale → `server.sh restart`.
- **비용**: Sonnet QA 가 한도 주 소모처. 생성 프롬프트가 QA 교훈 흡수했으니 함수부터는 스팟체크로.
- 관련 메모리: `project_concept_figures`(신규), `project_math_study`, `feedback_shutdown_keep_server`, `project_tutor_katex_robustness`.
