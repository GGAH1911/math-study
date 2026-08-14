---
name: math-study-ingest
description: >-
  math-study 에 새 기출 회차를 인제스트한다. 인제스트는 **한 번의 명령이 아니라 여러 단계의
  사슬**이고, 중간 단계가 조용히 빠지면 며칠 뒤 사람이 눈으로 보고서야 발견된다. 이 스킬은
  사전점검(의존성·인증·경로) → 인제스트 → 후속단계(교정·도형·박스·개념·풀이캐시) →
  **완결성 게이트**로 그 누락을 기계가 잡게 한다. 사용자가 "회차 인제스트", "기출 넣어줘",
  "새 시험지 적재", "taildrop 에 넣어놨어", "인제스트 확인해줘" 류로 말하면 — 명시하지
  않아도 — 이 스킬을 사용하라. 이미 적재된 회차의 상태 점검에도 쓴다.
---

# math-study 기출 인제스트

## 왜 이 스킬이 있나

2026-08-14, `2026_고3_7월모의고사` 가 **인제스트는 됐는데 교정 단계를 통째로 못 탄 채**
며칠을 지냈다. 사장님이 문제 목록을 눈으로 보다 발견했다.

겉으로 드러난 증상은 셋이었다 — ① 지수 전사가 깨짐(`5^{-}\frac{1}{2}×2\frac{3}{5^{4}}`)
② 도형 크롭 없음 ③ 보기 박스 없음. **원인은 하나**였고(교정 파이프라인 미실행), 그마저도
사람의 실수가 아니라 **툴체인이 실행 불가 상태**였다(레포 경로 하드코딩 + `claude -p` 인증 누락).

아무도 못 본 이유는 단순하다 — **"다 됐는지" 를 확인하는 것이 없었다.** 정상 회차는
`corrector_done` 이 100% 다. 한 줄만 비교했어도 잡혔다.

## 원칙

1. **각 단계는 끝났다고 믿지 말고 확인한다.** 특히 조용히 실패하는 것들:
   - `claude -p` 는 인증이 없으면 `Not logged in` 한 줄만 뱉고 **exit 0** 이다 → 호출부엔
     "파싱실패"로 보이고 → 자가치유 실패 → **문항 격리**. 인증 문제가 데이터 문제로 위장된다.
   - 파이썬 의존성 누락은 `건너뜀` 한 줄로 지나간다(`rosetta_extend 건너뜀: No module named pikepdf`).
2. **마지막에 반드시 완결성 게이트를 돌린다.** 통과 못 하면 인제스트는 안 끝난 것이다.
3. **오래 걸리는 단계는 백그라운드로**(`setsid ... &`). 세션이 끊겨도 완주한다.
4. **파괴적 작업 전 백업.** 재실행이 기존 md 를 덮는다.

## 0단계 — 사전점검 (건너뛰지 마라)

```bash
bash scripts/ops/on_tme.sh '
  echo "--- 파이썬 의존성 ---";
  for m in fitz pikepdf fontTools PIL sympy scipy psycopg; do
    ~/.venvs/ms-ingest/bin/python -c "import $m" 2>/dev/null && echo "  OK $m" || echo "  ✗ $m 없음";
  done
  echo "--- 외부 CLI ---"; for c in claude pdftotext node docker; do which $c >/dev/null && echo "  OK $c" || echo "  ✗ $c"; done
  echo "--- 인증 ---"; grep -q "^MS_CLAUDE_OAUTH_TOKEN=." deploy/.env && echo "  OK 토큰 있음" || echo "  ✗ 토큰 없음"
'
```

- `pikepdf` 없으면 → 새 회차에 **처음 보는 한컴 글리프가 있을 때** 로제타 자동확장이 죽는다
  (기존 글리프만 쓰는 회차면 영향 없다. `requirements.txt` 에 선언이 없는 것이 근본 문제 —
  `docs/TODO.md` 참조).
- 토큰 없으면 → **여기서 멈춰라.** 진행하면 교정이 전 문항을 격리한다.

## 1단계 — 인제스트

taildrop 에 파일이 있으면 자동 분류 디스패처를 쓴다. **기본 dry-run 이다.**

```bash
bash scripts/ops/on_tme.sh '~/.venvs/ms-ingest/bin/python scripts/ingest_kice/ingest_auto.py'          # 분류만 확인
bash scripts/ops/on_tme.sh '~/.venvs/ms-ingest/bin/python scripts/ingest_kice/ingest_auto.py --run'    # 실행
```

`ingest_auto` 는 후속 단계까지 체이닝한다. **다만 체이닝이 중간에 끊길 수 있으므로**
(실측: `체이닝 0/2` 에서 멈춘 로그가 있다) 2단계를 반드시 따로 확인한다.

교육청 고3 과목별 배포(`기하_문제.pdf` 등 과목별 PDF)는 `v2_haesol` 백엔드로 잡히고
`merge_subject_pdfs` 가 통합 `문제.pdf` 를 만든다 — 통합본이 생겼는지 확인하라.

## 2단계 — 후속 단계 (누락되는 자리)

인제스트가 끊겼다면 회차를 지정해 직접 돌린다. 순서가 중요하다.

```bash
R=2026_고3_7월모의고사
bash scripts/ops/on_tme.sh "MATHSTUDY_ROOT=/home/insung/math-study \
  CORRECT_BACKEND=sonnet RECORRECT_BACKEND=sonnet PAR_C=3 PAR_V=3 PAR_G=2 \
  node web/scripts/correct_verify_pipeline.mjs $R"        # ①교정+도형크롭+검증 (오래 걸림 → 백그라운드)
bash scripts/ops/on_tme.sh "MATHSTUDY_ROOT=/home/insung/math-study \
  ~/.venvs/ms-ingest/bin/python web/scripts/box_backfill.py $R"    # ②박스 마커 (결정론·LLM0·1초)
```

- **`extract_figures.py` 는 `corrector.mjs` 안 ① 단계**다. 교정을 안 돌리면 도형 크롭도 없다.
  둘이 한 몸이라는 걸 모르면 "도형만 다시 뽑자"고 헤매게 된다.
- 백엔드: `gemma`(로컬 맥북·토큰0) / `sonnet`(구독) / `agy`(Gemini) / `or`(OpenRouter).
  **agy 는 현재 사용 불가.** gemma 는 맥북 mlx 서버가 떠 있어야 한다. 소량이면 `sonnet` 이 간단하다.
- 크롭 결과물은 `web/private/problem-images/` 에 간다(`public` 아님 — 인증 게이팅 때문에
  정적 서빙 밖으로 뺐다. `web/src/lib/media-root.ts` 참조).

## 3단계 — 완결성 게이트 ★

```bash
bash scripts/ops/on_tme.sh '~/.venvs/ms-ingest/bin/python scripts/ops/verify_ingest_complete.py 2026/고3_7월모의고사'
```

**차단**(고치기 전엔 끝난 게 아니다): 교정 미실행 · 격리 · 난이도 공백 · 전사 비었음 ·
선언된 도형 파일 없음.
**경고**: 도형 라벨 본문 누출 · 고아 `{{FIG}}` 마커 · 배점 불일치.

> 회차는 `연도/회차`(`2026/고3_7월모의고사`) 로 지정하라 — 회차명은 해마다 중복이다.

정상 회차와 대조해 보는 것도 좋다(`corrector_done` 은 100% 가 정상):

```bash
bash scripts/ops/on_tme.sh '~/.venvs/ms-ingest/bin/python scripts/ops/verify_ingest_complete.py --all --quiet'
```

## 4단계 — 커밋

산출물은 `docs/problems/<연도>/<회차>/` 와 `web/private/problem-images/` 두 곳이다.
크론(`03:00 widget_spec_loop`)이 경로 미지정 `git commit` 을 하므로 **스테이징만 남기지 마라** —
남의 변경까지 딸려 간다.

## 증상 → 원인 (실측 이력)

| 증상 | 실제 원인 |
|---|---|
| 문항이 대량 `격리` | `claude -p` 인증 누락. 토큰부터 봐라 — 데이터 문제 아니다 |
| 교정이 아예 안 돌아감 | `web/scripts/*` 의 레포 경로. 이전 후 `ENOENT` 로 즉사했다 |
| 도형 크롭 0 | 교정 미실행(크롭은 corrector 안에 있다) |
| 지수·분수 구조 깨짐 | `hancom_decode` 구조 파서 버그. 교정기가 이미지로 덮는다 |
| `rosetta_extend 건너뜀` | `pikepdf` 미설치. **새 글리프가 없으면 무해** — 성급히 원인으로 몰지 마라 |
| 난이도 공백 | 프롬프트는 `high` 를 시키는데 검증기가 몰랐다(`tiers.py` 로 통합해 해결) |

## 하지 말 것

- **재전사로 전사 오류를 고치려 하지 마라.** 디코더는 결정론이라 같은 출력이 나온다.
  전사 오류는 **교정기(vision)** 가 이미지를 보고 고치는 것이 유일한 경로다.
- **`--no-correct` 로 넘기지 마라.** 그게 오늘의 사고를 만든 지름길이다.
- 게이트가 빨간데 "나중에 고치지" 하고 넘기지 마라 — 빨간 게이트는 곧 아무도 안 보는 게이트가 된다.
