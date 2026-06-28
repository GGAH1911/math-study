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

## 2. ★핵심 진실 (2026-06-28 대조실측으로 *재정정*) — claude CLI 는 `--system-prompt` 를 prefix 캐싱한다

★이 문서의 직전 버전은 "CLI 는 우리 프롬프트 캐싱 못 한다(breakpoint 끝에만)"고 단정했으나 **틀렸다.**
그 측정은 DISABLE_GIT 적용 *전*(git churn 활성)이라 prefix 가 매 호출 깨진 걸 "캐싱 불가"로 오판한 것 —
cta-law '동시2=헛다리'와 **같은 git churn 함정에 두 번** 빠진 사례. prefix 만 안정시키면 캐싱은 **작동한다.**

대조실험(clean cwd + DISABLE_GIT, **질문만 변경**):
- 큰 `--system-prompt` 고정 → 2콜째 **cr 이 시스템 크기만큼 증가**: SYS 10k자 → cr=22982, SYS 44k자 → cr=32265
  (내장 base ≈14877 을 초과하는 분 = **우리 시스템 프롬프트가 캐시된 것**).
- `--system-prompt` 한 글자만 바꾸면 → cr 붕괴(12745) + cc 재기록 = **byte-identical prefix 가 캐시 조건**(인과 확정).
- production `tutor_usage`: concepts **max_cr≈29237** = 개념 본문이 실제로 캐시·재사용됨(0이 아니다).

### 캐시 조건 (이걸 다 만족해야 cr)
| 대상 | CLI 로 캐시? | 조건 |
|---|---|---|
| claude 내장 base (도구 정의) | ✅ | 도구 쓰는 호출(--allowedTools/--add-dir). 도구 없으면 base 작음 |
| 우리 `--system-prompt` (규칙·개념본문 등) | ✅ | **byte-identical 안정 prefix** + clean cwd + DISABLE_GIT + 5분 TTL + **2콜째~** |
| `-p` 본문 prefix | ✅ | 〃 (단 질문이 본문 안에 있으면 그 뒤부터는 매 턴 달라져 미스) |

→ 핵심은 "캐싱 되냐"가 아니라 **무엇을 안정 prefix(`--system-prompt`)에 두고, 무엇을 경계 밖(질문·per-user
동적값)에 두느냐.** chat.ts 가 staticPrefix(slug-only) / dynamicSuffix(per-user·질문) 로 쪼개는 이유가 이것.

### C(API 직접)의 역할 — "유일 해법" 아니라 "추가 정밀제어"
CLI 로도 안정 prefix 는 캐시된다. C([[TUTOR_PROMPT_CACHE_C_API|backlog/TUTOR_PROMPT_CACHE_C_API]])는 *추가*
이득(동적부 별도 cache_control breakpoint·다중 경계·BYOK 모델별 제어)일 뿐 — 기본 캐싱의 전제조건이 아니다.

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
| `web/src/pages/api/chat.ts` (튜터) | haiku/sonnet | problem=Read · concept=없음 | ✅ | ✅(0628추가) | **problem max_cr≈20585 / concept max_cr≈29237** (멀티턴, staticPrefix slug-only 고정 후) |
| `web/src/pages/api/regenerate-body.ts` (개념본문 재생성·라이브) | haiku/sonnet | — | ✅ | ✅(0628추가) | |

> ※ 위 표는 **위생 적용 여부**(git churn 차단)다. 실이득(cr)은 ① 안정 prefix(byte-identical) ② 5분 TTL
> 안 2콜째~ 일 때 발생 — 멀티턴 튜터·연사 배치가 이득, 드문 단발 호출(regenerate-body 1회)은 cc만. 형태별 실측=§6-(e).

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

### (e) ★형태별 실측 매트릭스 (2026-06-28, clean cwd + DISABLE_GIT 고정, **질문만 변경**)

| config 형태 | 쓰는 곳 | 1콜 | 2콜(다른 질문) |
|---|---|---|---|
| `--allowedTools Read[,Bash]` (작은 sys) | qa_concept_figures · verify_batch · build_solution_cache · 튜터(problem) | cc≈22939 / cr=0 | cr≈14877 |
| `--system-prompt` 작음 | (테스트) | cc≈16758 / cr=0 | cr≈12755 |
| `--add-dir`만 | run_stage1 · ingest_round · verify_corrected | cr≈14877 | cr≈14877 |
| **`--system-prompt` 큼 10k자** | 개념 튜터 staticPrefix 패턴 | cc≈14240 / cr=12745 | **cr≈22982** |
| **`--system-prompt` 큼 44k자** | 〃 (더 큰 본문) | cc≈23522 | **cr≈32265** |
| `--tools ""` + 작은 sys | (도구·콘텐츠 둘 다 없을 때) | cc 작음 | cr≈0 |

★핵심 해석(직전 버전 "cr 은 sys 길이 무관" 은 **오류, 정정**): **cr 은 `--system-prompt` 크기 따라 증가한다**
(12755 → 22982 → 32265). 즉 우리 콘텐츠(개념 본문·규칙)도 안정 prefix 면 캐시된다. production 개념 튜터
max_cr≈29237 이 그 증거.

### (f) ★end-to-end 실측 (2026-06-28, 실제 /api/chat, staticPrefix slug-only 고정 후)
4325(DEV_NOAUTH) 에서 같은 개념(등비수열) 2턴, 질문만 변경:
| 턴 | cr | cc |
|---|---|---|
| 1 (질문 A) | 0 | 23256 |
| 2 (질문 B, 다름) | **21720** | 1374 |
턴2 cr=21720 ≫ 도구 base(~14877) ≈ 턴1 cc = **staticPrefix(개념 본문+규칙)가 캐시·재사용됨**. staticPrefix 를
slug-only 로 고정(per-user mastery·learnerContext 를 dynamicSuffix 로) 했기에 질문이 바뀌어도 cr 생존.
(측정 시 합성 유저 FK 우회 필요: `tutor_usage.user_id → users(id)`, DEV_NOAUTH 유저 00000…0 이 users 부재면
 best-effort 로깅이 조용히 실패한다.) cr≈0 인 경우는 "캐싱 불가"가 아니라 **(a) 1콜째**(cc 기록) **(b) prefix 가 byte-identical
이 아님**(per-user 동적값 혼입) **(c) TTL 만료** **(d) 캐시할 게 실제로 없음**(작은 sys + `--tools ""`) 중 하나.
→ **연사·멀티턴이 이득 큼**, **드문 단발 호출**(regenerate-body 1회)은 매번 cc만(구조적, 버그 아님).

## 7. 도구 (재사용)
- `web/scripts/lib/claude_p.mjs` — 공용 spawn 래퍼(clean cwd + DISABLE_GIT 둘 다, 0628 완비).
- `scripts/ingest_kice/{ingest_round,run_stage1}.py` `claude_p()` — Python 공용 매퍼(둘 다 완비).
- `web/src/lib/tutor-usage.ts` — `parseUsage`(result usage→정수) + `logTutorUsage`(DB 적재).

---
## 🔗 지식망 연결
- **상위 분류**: [[00_ARCHITECTURE]]
- 코드 진입: [[00_API|web/src/pages/api/]](chat.ts) · [[00_SCRIPTS|scripts/]]
- 계획: [[TUTOR_PROMPT_CACHE_C_API]](C — API 직접 cache_control)
