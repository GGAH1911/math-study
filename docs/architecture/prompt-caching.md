---
sources: []
created: 2026-06-28
updated: 2026-06-28
---

# 프롬프트 캐싱 — 어디에 필요하고, 어떻게 검증하나

> 분류: Architecture / LLM. 2026-06-28 측정으로 정정된 권위 문서. 짧은 운영 메모는
> `docs/CLAUDE_P_CACHING.md`, 크론 실측은 [[cron-runs|docs/ops/status/cron-runs.md]].

## 1. 왜 캐싱이 중요한가 (우리 맥락)

- **구독(Claude Code/`claude -p`)에서 캐싱은 "돈"이 아니라 5시간 rate-limit 한도를 아낀다** — 토큰당
  과금이 아니라 한도 소진을 늦춘다. 대량 배치(인제스트·솔버·위젯)에서 한도 절약이 곧 처리량.
- **API 직접(BYOK·프로덕션)에서는 진짜 비용 절감** — cache_read 토큰은 입력 단가의 1/10.

## 2. ★핵심 진실 — claude CLI 는 *우리* 프롬프트를 prefix 캐싱 못 한다

측정으로 밝혀진 것(이전 "cache_read≈43k/콜이 우리 시스템 프롬프트" 주장은 오해였음):

- claude CLI(`-p`)는 `cache_control` breakpoint 를 프롬프트 **맨 끝에만 자동으로** 찍는다.
  → **프롬프트 전체가 byte-identical 일 때만** cache_read 히트. 질문이 한 글자라도 다르면, 멀티턴으로
  앞부분을 공유해도 **미스**(cc 매번 생성, cr=0).
- 그럼 인제스트·배치에서 잡히던 cache_read 는 무엇? → **claude 내장 base**(claude 자체 시스템 프롬프트
  + 도구 정의)가 캐시된 것. **우리 콘텐츠가 아니다.** 실측: 도구 활성 시 "사과"·"바나나"(완전 다른
  질문) 2회도 cr 동일(≈14877) = 질문 무관한 내장 base 토큰.

### 따라서 우리가 통제 가능한 것 / 불가능한 것
| 대상 | CLI 로 캐시? | 비고 |
|---|---|---|
| claude 내장 base (도구 정의 등) | ✅ (자동) | **도구 쓰는 호출**(--allowedTools / --add-dir)에서 cr 로 잡힘 |
| 우리 시스템 프롬프트 (규칙·문제텍스트·개념) | ❌ | breakpoint 가 끝에만 → prefix 부분캐시 불가 |
| 우리 프롬프트 (전체 동일 반복) | ✅ | 비현실적(질문이 매번 다름) |

→ **우리 거대 프롬프트의 진짜 캐싱 = Anthropic API 직접 + 명시적 cache_control breakpoint** 뿐.
  계획: [[TUTOR_PROMPT_CACHE_C_API|backlog/TUTOR_PROMPT_CACHE_C_API]].

## 3. CLI 에서 캐시를 *깨는* 것들 (피해야 할 것)

1. **git churn** (가장 흔함): Claude Code 가 system prompt 에 git status/branch/commits 를 박는다.
   레포 cwd 에서 spawn 하면 미커밋 변경이 매 호출 prefix 를 바꿔 **내장 base 캐시까지 깨진다**.
   → 우리 레포는 미커밋 수백 개라 특히 심각.
2. 모델/effort 전환, MCP 로딩, /compact, fast mode 토글.
3. 5분(또는 1h) TTL 초과.

## 4. 처방 — 벨트+멜빵 (CLI 호출의 표준)

내장 base 캐시라도 생존시키려면 **둘 다** 줘야 한다(실측: git 켜짐=cr 콜마다 변동 17506→25092,
DISABLE_GIT=23478 고정):

```js
spawn('claude', args, {
  cwd: CLEAN_DIR,                                   // ① 벨트: 빈 /tmp/claude_p_clean (git 없음 + CLAUDE.md auto-discovery 차단)
  env: { ...env, CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS: '1' },  // ② 멜빵: git 블록 자체 제거(cwd 무관)
});
// 파일 접근은 cwd 가 아니라 --add-dir <절대경로> 로 (레포를 가리켜도 안전).
```

- **①만으로는 부족** — clean cwd 라도 git 블록이 새어 cache_creation 만 잡히고 cr=0 인 경우 있음.
- 서버(`/api/chat`)는 env 화이트리스트(`safeChildEnv`)를 쓰므로 **거기에 DISABLE_GIT 를 명시 추가**해야
  한다(2026-06-28 튜터에 빠져 있던 게 이 함정 — ALLOW 리스트에 없어 멜빵이 통째 누락됐었음).

## 5. 캐싱이 필요한 부분 (적용 현황 — 2026-06-28 전수 실사 후 정정·완비)

★2026-06-28: 전수 조사로 누락 다수 발견 후 **전부 보강 완료**(clean cwd + DISABLE_GIT 둘 다).
plan: [[PROMPT_CACHE_HYGIENE_2026-06-28|completed/2026_06/PROMPT_CACHE_HYGIENE]].

| 호출 지점 | 모델 | 도구 | clean cwd | DISABLE_GIT | 비고 |
|---|---|---|---|---|---|
| `scripts/build_solution_cache.py` (솔버) | haiku→sonnet→opus | Read | ✅ | ✅ | 내장 base(도구 큼) |
| `scripts/ingest_kice/ingest_round.py` `claude_p()` (매핑·**공용**) | haiku | — | ✅(0628추가) | ✅ | text_meta·vision_meta·crop_with_llm·llm_solve_geomgo 가 import |
| `scripts/ingest_kice/run_stage1.py` `claude_p()` (매핑·**공용**) | sonnet/haiku | — | ✅(0628추가) | ✅(0628추가) | concept_remap(map_problem) 가 import |
| `scripts/fill_spoke_bodies.py` (개념본문) | haiku | — | ✅(0628추가) | ✅(0628추가) | |
| `scripts/regenerate_searchable.py` (재OCR) | sonnet | Read | ✅(0628추가) | ✅(0628추가) | 타일 vision |
| `web/scripts/widget_generate.mjs` · `widget_survey.mjs` (위젯) | opus | — | ✅ | ✅ | cr 측정(`cr=`) |
| `web/scripts/verify_batch.mjs` · `corrector.mjs` · `redraw_*.mjs` · `gen_concept_figures.mjs` | sonnet | Read | ✅ | ✅ | 도구 base |
| `web/scripts/qa_concept_figures.mjs` (도식 QA) | sonnet | Read,Bash | ✅(0628추가) | ✅(0628추가) | CLAUDE_SPAWN 공용화 |
| `web/scripts/verify_corrected.mjs` (교정검증) | sonnet | — | ✅(0628추가) | ✅(0628추가) | |
| `web/scripts/lib/claude_p.mjs` (공용 래퍼) | * | * | ✅ | ✅(0628추가) | corrector import(자체 spawn 씀=저영향이나 footgun 제거) |
| `web/scripts/gen_daily_illustration.mjs` (그림) | haiku | — | ✅ | ✅ | 작음(도구 없음) |
| `web/src/pages/api/chat.ts` (튜터) | haiku/sonnet | problem=Read · concept=없음 | ✅ | ✅(0628추가) | **problem cr≈20585 / concept≈0** |
| `web/src/pages/api/regenerate-body.ts` (개념본문 재생성·라이브) | haiku/sonnet | — | ✅ | ✅(0628추가) | |

### ★구조 교훈 (공용함수 = 단일 수정점)
Python 인제스트는 **공용 `claude_p()` 2개**(`run_stage1.py`, `ingest_round.py`)에 하위 5개가 의존 →
공용함수만 고치면 전파된다. 새 호출은 **반드시 이 공용함수(또는 .mjs `lib/claude_p.mjs`)를 경유**할 것.

### 남은 N/A (1회성 PoC·진단 — 캐싱 무관)
`scripts/{poc_*,tile_*_test,pilot_*,contamination_probe,ab_path_leak,measure_*,backfill_*,refine_opus,recover_text_defects,audit_searchable_ocr,extract_all_answers}.py` 등.

## 6. 검증 방법론 (★조용히 깨지므로 반드시 실측)

캐싱은 "조용히 깨지는 게 가장 나쁘다" — 됐다고 **가정 금지**, `usage.cache_read_input_tokens` 를 본다.

### (a) 단발 실측 — stream-json 의 result 이벤트
```bash
cd /tmp/claude_p_clean
CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS=1 claude -p "<프롬프트>" --model haiku \
  --output-format stream-json --verbose --tools "" 2>/dev/null \
| python3 -c "import sys,json
for l in sys.stdin:
  try:o=json.loads(l)
  except:continue
  if o.get('type')=='result':
    u=o.get('usage',{});print('cr=%s cc=%s in=%s'%(u.get('cache_read_input_tokens'),u.get('cache_creation_input_tokens'),u.get('input_tokens')))"
```

### (b) 캐시 *생존* 판정 — 같은 조건 2회
- **1회차 cc>0, 2회차 cr>0** = 캐시 생존(히트). 2회차도 cc 만이면 **prefix 가 매번 다른 것**(깨짐).
- ★주의: 완전 동일 프롬프트로 테스트하면 우리 콘텐츠가 캐시되는 것처럼 *오인*한다. **질문을 바꿔서**
  테스트해야 "내장 base 만 캐시되고 우리 콘텐츠는 안 된다"는 진실이 드러난다.

### (c) git churn 격리 — 켜고/끄고 비교
- DISABLE_GIT 없이 vs 있이 같은 호출 2회씩. 없으면 cr 콜마다 변동, 있으면 고정 → churn 이 범인 확정.

### (d) 운영 추적 — DB / 로그
- **튜터**: `tutor_usage` 테이블(계정별 input/output/cache_read/cache_creation, [[00_LIB|lib/tutor-usage.ts]]).
  `SELECT collection, avg(cache_read_tokens) FROM tutor_usage GROUP BY collection;`
- **크론(위젯)**: `widget_daily.log` 의 `cache_read=K` + `cron-runs.md` 다이제스트(cr avg/max).

## 7. 도구 (재사용)
- `web/scripts/lib/claude_p.mjs` — 공용 spawn 래퍼(clean cwd + DISABLE_GIT 둘 다, 0628 완비).
- `scripts/ingest_kice/{ingest_round,run_stage1}.py` `claude_p()` — Python 공용 매퍼(둘 다 완비).
- `web/src/lib/tutor-usage.ts` — `parseUsage`(result usage→정수) + `logTutorUsage`(DB 적재).

---
## 🔗 지식망 연결
- **상위 분류**: [[00_ARCHITECTURE]]
- 코드 진입: [[00_API|web/src/pages/api/]](chat.ts) · [[00_SCRIPTS|scripts/]]
- 계획: [[TUTOR_PROMPT_CACHE_C_API]](C — API 직접 cache_control)
