#!/usr/bin/env python3
"""
Stage 1 ingest: 2025 수능 수학 → markdown + Postgres.

Pipeline:
  1. Each PDF page (PNG, already rendered) → markdown via Claude vision
  2. Concatenate all pages, split by '## N번 [X점]' header → 46 problems
  3. Answer key page (separate PDF) → number → answer dict
  4. For each problem, claude -p maps to {unit, concepts[], intent, killer_tier, cognitive_type, expected_time_sec}
  5. Write docs/problems/2025_수능_<subject>_<num>.md (frontmatter + body)
  6. Upsert into Postgres (exams, problems, problem_concepts)

Idempotent: existing files are skipped unless --force.
"""
from __future__ import annotations
import json
import os
import re
import subprocess
import sys
import time
import uuid
from pathlib import Path
from textwrap import dedent

import psycopg

# ★2026-08-13: 여기 `/home/insung/Projects/math-study` 가 박혀 있었다. 레포는 진작
#   `/home/insung/math-study` 로 옮겨졌고 그 경로는 **존재하지 않는다.** 그래서
#   load_concept_index() 가 빈 dict 를 돌려줬고(파일이 0개니까), LLM 은 "아래 목록에서
#   고르라" 는 지시와 함께 **빈 목록**을 받아 개념 이름을 지어냈다. 예외는 안 났다 —
#   존재하지 않는 디렉터리의 glob 은 조용히 빈 결과다.
#   → 파일 위치에서 유도하고, 필요하면 MATHSTUDY_ROOT 로 덮어쓴다.
ROOT = Path(os.environ.get('MATHSTUDY_ROOT') or Path(__file__).resolve().parents[2])
if not (ROOT / 'docs' / 'concepts').is_dir():
    raise SystemExit(f'[FATAL] 개념 트리를 찾을 수 없다: {ROOT}/docs/concepts — MATHSTUDY_ROOT 를 확인하라')
RAW = ROOT / 'db' / 'raw' / '2025_수능'
PAGES = RAW / 'pages'
DOCS_PROBLEMS = ROOT / 'docs' / 'problems'
WORK = RAW / 'work'  # intermediate per-page markdown
WORK.mkdir(parents=True, exist_ok=True)

# ★프롬프트 캐싱 위생: clean cwd(벨트) + DISABLE_GIT(멜빵). 레포 cwd 면 git status 가 매 호출
#   system prompt 를 바꿔 claude 내장 base 캐시까지 깬다. 파일접근은 --add-dir(절대경로)로.
_CLEAN_DIR = os.environ.get('CLAUDE_P_CWD', '/tmp/claude_p_clean')
os.makedirs(_CLEAN_DIR, exist_ok=True)
_CLAUDE_ENV = {**os.environ, 'CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS': '1'}

DB = 'postgresql://mathstudy:mathstudy@127.0.0.1:5434/mathstudy'
TODAY = '2026-05-17'

VISION_SYSTEM = dedent("""
    당신은 한국 수능 수학 PDF 페이지를 한국어 markdown + KaTeX로 변환하는 변환기입니다.

    출력 규칙:
    1. 각 문제는 `## N번 [X점]` 헤더로 시작 (N=문제번호, X=배점 2/3/4).
    2. 문제 본문 다음에 객관식 보기 (1) (2) (3) (4) (5)는 한 줄에 ① ② 같은 원숫자 대신 `(1) ... (2) ... (3) ... (4) ... (5) ...` 형식.
    3. 단답형 문제 (22-30번 등)는 보기 줄 없음.
    4. 수식은 KaTeX: inline `$...$`, display `$$...$$`, 케이스는 `\\begin{cases}...\\end{cases}`.
    5. 그림이 있는 문제는 문제 본문 끝에 `<!-- 그림: 좌표평면에 ... 같은 한 줄 설명 -->` 주석으로.
    6. 페이지 번호·홀수형/짝수형 라벨·저작권 문구·"5지선다형" 등 메타는 제외.
    7. 문제 사이는 `---` 구분선.
    출력은 변환된 markdown만, 다른 설명 일절 없음.
""").strip()

ANSWER_SYSTEM = dedent("""
    당신은 한국 수능 수학 정답표 PDF 페이지를 읽어 문제번호→정답을 JSON으로 출력합니다.

    출력 형식:
    {
      "공통": {"1": "3", "2": "5", ..., "22": "8"},
      "확률과통계": {"23": "...", ..., "30": "..."},
      "미적분": {"23": "...", ..., "30": "..."},
      "기하": {"23": "...", ..., "30": "..."}
    }

    객관식 정답은 "1"~"5", 단답형은 수치 그대로. 출력은 JSON만.
""").strip()

UNIT_SYSTEM = dedent("""
    한국 수능 수학 문제를 읽고, 주어진 단원 경로 목록에서 **가장 적합한 하나**를 고른다.
    출력은 경로 문자열 하나뿐. 설명·따옴표·코드펜스 일절 금지.
""").strip()

MAP_SYSTEM = dedent("""
    당신은 한국 수능 수학 문제 한 개를 분석하여 메타데이터 JSON을 출력합니다.

    단원은 이미 정해져 있다. 주어진 **개념 경로 목록에서만** 1-3개를 고른다.
    목록에 없는 개념을 지어내지 마라 — 지어낸 것은 버려진다.

    출력 JSON 스키마:
    {
      "concepts": ["<경로1>", "<경로2>"],       // 1-3개, 반드시 목록에 있는 경로 그대로
      "exam_intent": "<한 줄 요약>",
      "killer_tier": "early|mid|high|killer",
      "cognitive_type": "계산|개념|응용|추론|통합",
      "expected_time_sec": <정수>
    }

    killer_tier 가이드:
    - early: 1-15번대, 2-3점, 단순 계산
    - mid: 15-20번대, 3-4점, 표준 응용
    - high: 20-22번대, 4점, 까다로운 추론
    - killer: 21·22·28·29·30번대, 정답률 30% 미만 예상

    출력은 JSON만, 설명 일절 없음.
""").strip()


def claude_p(system: str, user: str, model: str = 'sonnet', max_turns: int = 1,
             add_dir: str | None = None, timeout: int = 180, retries: int = 2,
             no_tools: bool = False) -> str | None:
    """Invoke `claude -p` with given system/user prompts. Returns stdout text or None on failure.

    ★연속 호출에서 간헐적으로 rc=1(빈 stderr)이 난다. 배치에서 이걸 한 번의 실패로 처리하면
      멀쩡한 모델이 '0점' 으로 집계된다(실제로 A/B 첫 측정이 그랬다). 짧게 재시도한다.
    """
    for attempt in range(max(1, retries)):
        out = _claude_p_once(system, user, model, max_turns, add_dir, timeout, no_tools)
        if out:
            return out
        time.sleep(1.5 * (attempt + 1))
    return None


def _claude_p_once(system: str, user: str, model: str, max_turns: int,
                   add_dir: str | None, timeout: int, no_tools: bool = False) -> str | None:
    args = ['claude', '-p',
            '--model', model,
            '--max-turns', str(max_turns),
            '--output-format', 'text',
            '--no-session-persistence']
    # ★도구 쓸 일이 없는 분류·매핑 호출은 도구를 **꺼야** 한다. 안 끄면 모델이 파일을
    #   열어보려다 --max-turns 1 을 그 턴에 다 써 `Error: Reached max turns (1)` 로 죽는다.
    #   haiku 가 sonnet 보다 도구를 잘 집어서, A/B 첫 측정에서 haiku 만 0점이 나왔다 —
    #   능력 차이로 오독할 뻔했다. 측정은 기준부터 의심하라.
    if no_tools:
        args += ['--tools', '']
    if add_dir:
        args += ['--add-dir', add_dir]
    args += ['--system-prompt', system, user]
    try:
        # ★stdin 을 닫아 준다. 안 닫으면 `claude -p` 가 파이프 입력을 3초 기다렸다가
        #   경고를 내고 실패한다(rc=1). 배치에서 조용히 전부 실패하는 원인이 된다.
        r = subprocess.run(args, capture_output=True, text=True, timeout=timeout,
                           cwd=_CLEAN_DIR, env=_CLAUDE_ENV, stdin=subprocess.DEVNULL)
        if r.returncode != 0:
            print(f'  ! claude failed (rc={r.returncode}): stderr={r.stderr[:300]!r}', file=sys.stderr, flush=True)
            return None
        return r.stdout.strip()
    except subprocess.TimeoutExpired:
        print(f'  ! claude timeout after {timeout}s', file=sys.stderr, flush=True)
        return None


def convert_pages(page_files: list[Path]) -> dict[int, str]:
    """For each PDF page (PNG), run claude vision → markdown. Cache to WORK/."""
    results = {}
    for png in page_files:
        page_num = int(re.match(r'p(\d+)\.png', png.name).group(1))
        cache = WORK / f'p{page_num:02d}.md'
        if cache.exists() and cache.stat().st_size > 50:
            results[page_num] = cache.read_text(encoding='utf-8')
            print(f'  [page {page_num}] cached', flush=True)
            continue
        t0 = time.time()
        md = claude_p(
            VISION_SYSTEM,
            f'{png.name} 이미지를 Read 툴로 열어 페이지의 모든 문제를 markdown+KaTeX로 변환하라. 설명 없이 markdown만 출력.',
            model='sonnet',
            max_turns=5,
            add_dir=str(PAGES),
            timeout=240,
        )
        if md:
            cache.write_text(md, encoding='utf-8')
            results[page_num] = md
            print(f'  [page {page_num}] {len(md)} chars  ({time.time()-t0:.1f}s)', flush=True)
        else:
            print(f'  [page {page_num}] FAILED', flush=True)
    return results


def split_problems(all_md: str) -> list[dict]:
    """Split combined markdown into individual problems by '## N번 [X점]' headers."""
    pattern = re.compile(r'##\s*(\d+)\s*번\s*\[(\d+)점\]\s*\n', re.MULTILINE)
    problems = []
    matches = list(pattern.finditer(all_md))
    for i, m in enumerate(matches):
        number = int(m.group(1))
        score = int(m.group(2))
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(all_md)
        body = all_md[start:end].strip()
        # strip trailing horizontal rules
        body = re.sub(r'\n---\s*$', '', body).strip()
        # determine format heuristically: contains (1)...(5)? → choice
        fmt = 'choice' if re.search(r'\(1\).*\(2\).*\(3\).*\(4\).*\(5\)', body, re.DOTALL) else 'numeric'
        problems.append({'number': number, 'score': score, 'body': body, 'format': fmt})
    return problems


from ingest_round import (  # noqa: E402  구현은 한 곳에만 — 두 벌이면 반드시 갈라진다
    load_concept_index, scope_for, unit_menu, spoke_menu, validate_mapping,
)


def map_problem(prob_body: str, number: int, score: int, units_index: dict,
                subject: str | None = None, grade: str | None = None,
                model: str = 'haiku') -> dict | None:
    """문제 1개 → unit/concepts/intent/tier/cognitive. **2단계 + 게이트.**

    ★예전에는 한 번에 물었고, 후보 목록이 비어 있어도 그대로 진행했다. 그래서 LLM 이
      개념 이름을 지어냈고 아무도 실패로 세지 않았다. 이제 ①후보가 비면 즉시 None,
      ②단원 → 스포크로 나눠 묻고, ③둘 다 후보 안에서 나왔는지 검증한다.
    """
    index = units_index or {}
    if not index:
        print(f'  ! #{number}: 개념 후보가 0개 — 매핑 중단(스코프/경로 확인)', flush=True)
        return None

    body = prob_body[:2500]
    ctx = f'문제 번호: {number}, 배점: {score}점' + (f', 영역: {subject}' if subject else '')

    # ── 1단계: 단원 ──────────────────────────────────────────────────────────
    u_user = f"""{ctx}

문제 본문:
{body}

아래 **단원 경로 중 정확히 하나**를 고르라(경로 그대로, 다른 텍스트 금지).
경로의 가운데 조각은 학년이다 — 이 문제의 학년에 맞는 것을 골라야 한다.
{unit_menu(index)}"""
    unit = (claude_p(UNIT_SYSTEM, u_user, model=model, max_turns=1, timeout=60, no_tools=True) or '').strip()
    unit = re.sub(r'^```\w*|```$', '', unit).strip().strip('"\'` ')
    if unit not in index:
        # 경로 일부만 답한 경우 구제(예: 마지막 조각만).
        cand = [u for u in index if u.endswith('/' + unit) or u == unit]
        unit = cand[0] if len(cand) == 1 else ''
    if not unit:
        print(f'  ! #{number}: 단원 선택 실패', flush=True)
        return None

    # ── 2단계: 스포크 + 나머지 메타 ──────────────────────────────────────────
    s_user = f"""{ctx}
선택된 단원: {unit}

문제 본문:
{body}

아래 **개념 경로 중 1-3개**를 고르고 나머지 필드를 채워 JSON 만 출력하라.
{spoke_menu(index, unit)}"""
    out = claude_p(MAP_SYSTEM, s_user, model=model, max_turns=1, timeout=60, no_tools=True)
    if not out:
        return None
    out = re.sub(r'^```(?:json)?\s*|\s*```$', '', out.strip(), flags=re.MULTILINE)
    try:
        meta = json.loads(out)
    except Exception as e:
        print(f'  ! map JSON parse failed for #{number}: {e}\n  raw: {out[:200]}', flush=True)
        return None

    meta['unit'] = unit
    meta['concepts'] = [c for c in (meta.get('concepts') or []) if isinstance(c, str)]
    ok, why = validate_mapping(unit, meta['concepts'], index)
    if not ok:
        # 후보 밖 스포크는 버린다 — 지어낸 개념이 프론트매터로 새어 나가는 걸 여기서 끊는다.
        allowed = set(index[unit])
        dropped = [c for c in meta['concepts'] if c not in allowed]
        meta['concepts'] = [c for c in meta['concepts'] if c in allowed]
        print(f'  ~ #{number}: 후보 밖 개념 {len(dropped)}개 버림 ({why})', flush=True)
    return meta


def extract_answers(pages: list[Path]) -> dict[str, dict[str, str]]:
    """Render answer-key PDF pages → vision → JSON of {subject: {number: answer}}."""
    answers_pdf = RAW / '정답.pdf'
    if not answers_pdf.exists():
        return {}
    # Render the answer pdf as well
    import fitz
    ans_pages_dir = RAW / 'ans_pages'
    ans_pages_dir.mkdir(exist_ok=True)
    doc = fitz.open(answers_pdf)
    for i, page in enumerate(doc):
        out_path = ans_pages_dir / f'ans_p{i+1:02d}.png'
        if not out_path.exists():
            page.get_pixmap(dpi=200).save(out_path)
    doc.close()

    combined = {}
    for png in sorted(ans_pages_dir.glob('ans_p*.png')):
        cache = WORK / f'{png.stem}.json'
        if cache.exists() and cache.stat().st_size > 5:
            data = json.loads(cache.read_text(encoding='utf-8'))
        else:
            raw = claude_p(
                ANSWER_SYSTEM,
                f'{png.name} 이미지를 Read 툴로 열고 정답표를 JSON으로 출력하라.',
                model='sonnet',
                max_turns=5,
                add_dir=str(ans_pages_dir),
                timeout=180,
            )
            if not raw:
                continue
            raw = re.sub(r'^```(?:json)?\s*|\s*```$', '', raw.strip(), flags=re.MULTILINE)
            try:
                data = json.loads(raw)
            except Exception as e:
                print(f'  ! answer JSON parse failed for {png.name}: {e}', flush=True)
                continue
            cache.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        for subj, mapping in data.items():
            combined.setdefault(subj, {}).update(mapping)
    return combined


def classify_subject(number: int) -> str:
    """수능 수학 영역 구조: 1-22번은 공통, 23-30번은 선택. PDF 하나에 공통+선택 1개가 들어 있음.
    이 PDF가 어떤 선택을 담는지는 PDF 메타 또는 파일명에서. 일단 23-30은 'unknown_selective'.
    실제로는 PDF가 미적분/확통/기하 중 어느 것인지 표지에 적혀 있음.
    호랭이닷컴의 문제.pdf는 통합본일 가능성이 높음 — 22번까지 공통, 그 뒤 미적분 8 + 확통 8 + 기하 8 = 46.
    """
    if number <= 22:
        return '공통'
    elif number <= 30:
        return '미적분'  # 첫 선택과목 — 통합본 순서 가정
    elif number <= 38:
        return '확률과통계'
    else:
        return '기하'


def write_markdown(prob: dict, mapping: dict, answer: str | None, exam_year: int = 2025) -> Path:
    """Generate the docs/problems/<slug>.md frontmatter + body."""
    subject = classify_subject(prob['number'])
    # Within selective subject, renumber to local 23-30 (kept) — keep global number for now
    slug = f'{exam_year}_수능_{subject}_{prob["number"]:02d}'
    out = DOCS_PROBLEMS / f'{slug}.md'

    pid = str(uuid.uuid4())
    concepts = mapping.get('concepts', []) if mapping else []
    unit = mapping.get('unit', '') if mapping else ''
    intent = mapping.get('exam_intent', '') if mapping else ''
    killer = mapping.get('killer_tier', '') if mapping else ''
    cog = mapping.get('cognitive_type', '') if mapping else ''
    et = mapping.get('expected_time_sec', 0) if mapping else 0

    # Build concepts list including the unit + spokes (all under docs/concepts/)
    concept_paths = [f'docs/concepts/{unit}.md'] if unit else []
    for c in concepts:
        cp = f'docs/concepts/{c}.md'
        if cp not in concept_paths:
            concept_paths.append(cp)
    concepts_yaml = ', '.join(concept_paths)

    fm = dedent(f'''\
        ---
        sources: [pdf:db/raw/2025_수능/문제.pdf, kice:공식정답표]
        created: {TODAY}
        updated: {TODAY}
        source:
          agency: 평가원
          exam_type: 수능
          year: {exam_year}
          session: 11월 본수능
          subject: {subject}
          number: {prob['number']}
          score: {prob['score']}
        problem_id: {pid}
        format: {prob['format']}
        has_image: false
        image_paths: []
        answer: "{answer or ''}"
        official_pass_rate: null
        official_solution_url: null
        unit: {unit}
        concepts: [{concepts_yaml}]
        exam_intent: "{intent}"
        killer_tier: {killer}
        cognitive_type: {cog}
        expected_time_sec: {et}
        status: unsolved
        review_state: new
        next_review: {TODAY}
        ---
        ''')

    body = dedent(f'''\

        # [{exam_year} 수능 {subject} {prob["number"]}번] {prob["score"]}점

        > 출처: 한국교육과정평가원 {exam_year}학년도 수능 수학영역 · 단원: {unit or '(매핑 필요)'}
        > Tier: {killer or '?'} · cognitive: {cog or '?'} · 예상 시간 {et}초
        > **{intent or "(intent missing)"}**

        ## 문제

        {prob['body']}

        ## 풀이 (학습 시 채워짐)

        본 페이지의 상세 풀이는 학습 시 직접 작성하거나, 페이지 하단 채팅창에서 LLM 튜터의 도움으로 채우세요.

        ## 매핑된 개념
        ''') + '\n'.join(f'- [{c.replace("_"," ")}](../concepts/{c}.md)' for c in ([unit] + concepts) if c) + '\n'

    out.write_text(fm + body, encoding='utf-8')
    return out


def db_upsert(problems_with_meta: list[dict]) -> None:
    """Insert/upsert exam + problems + concept mappings into Postgres."""
    with psycopg.connect(DB) as conn, conn.cursor() as cur:
        # Per subject, one exam row (or one exam with subject as column? plan says one row per subject is fine)
        # We use one exam row for the whole 수능 회차, subject is on problems.
        cur.execute(
            """INSERT INTO exams (agency, exam_type, year, session, source_pdf)
               VALUES (%s, %s, %s, %s, %s)
               ON CONFLICT (agency, exam_type, year, session) DO UPDATE SET ingested_at = NOW()
               RETURNING id""",
            ('평가원', '수능', 2025, '11월 본수능', 'db/raw/2025_수능/문제.pdf'),
        )
        exam_id = cur.fetchone()[0]

        for item in problems_with_meta:
            prob = item['prob']
            mapping = item['mapping'] or {}
            ans = item['answer']
            subject = classify_subject(prob['number'])
            slug = f'2025_수능_{subject}_{prob["number"]:02d}'
            cur.execute(
                """INSERT INTO problems
                     (exam_id, subject, number, score, format, text_markdown, has_image, image_paths,
                      answer, unit_slug, exam_intent, killer_tier, cognitive_type, expected_time_sec,
                      frontmatter_path)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                   ON CONFLICT (exam_id, subject, number) DO UPDATE SET
                     score = EXCLUDED.score, format = EXCLUDED.format,
                     text_markdown = EXCLUDED.text_markdown, answer = EXCLUDED.answer,
                     unit_slug = EXCLUDED.unit_slug, exam_intent = EXCLUDED.exam_intent,
                     killer_tier = EXCLUDED.killer_tier, cognitive_type = EXCLUDED.cognitive_type,
                     expected_time_sec = EXCLUDED.expected_time_sec
                   RETURNING id""",
                (exam_id, subject, prob['number'], prob['score'], prob['format'], prob['body'],
                 False, [], ans, mapping.get('unit') or None,
                 mapping.get('exam_intent'), mapping.get('killer_tier'),
                 mapping.get('cognitive_type'), mapping.get('expected_time_sec'),
                 f'docs/problems/{slug}.md'),
            )
            pid = cur.fetchone()[0]

            # concept mappings
            cur.execute('DELETE FROM problem_concepts WHERE problem_id = %s', (pid,))
            unit = mapping.get('unit')
            if unit:
                cur.execute(
                    """INSERT INTO problem_concepts (problem_id, concept_slug, weight, is_primary)
                       VALUES (%s, %s, 1.0, TRUE)
                       ON CONFLICT DO NOTHING""",
                    (pid, unit),
                )
            for spoke in mapping.get('concepts', []) or []:
                cur.execute(
                    """INSERT INTO problem_concepts (problem_id, concept_slug, weight, is_primary)
                       VALUES (%s, %s, 0.8, FALSE)
                       ON CONFLICT DO NOTHING""",
                    (pid, spoke),
                )
        conn.commit()


def main():
    print('=== Stage 1: 2025 수능 수학 ingest ===', flush=True)

    # Step 1: convert all pages
    print('\n[1] Converting PDF pages with Claude vision...', flush=True)
    page_files = sorted(PAGES.glob('p*.png'))
    page_md = convert_pages(page_files)

    # Step 2: combine and split
    print('\n[2] Splitting into problems...', flush=True)
    combined = '\n\n---\n\n'.join(page_md[i] for i in sorted(page_md.keys()))
    problems = split_problems(combined)
    print(f'  → {len(problems)} problems detected', flush=True)
    nums = sorted(p['number'] for p in problems)
    print(f'  numbers: {nums[:10]} ... {nums[-5:]}' if len(nums) > 15 else f'  numbers: {nums}', flush=True)

    # Step 3: answers
    print('\n[3] Extracting answer key...', flush=True)
    answers = extract_answers([RAW / '정답.pdf'])
    print(f'  → {sum(len(v) for v in answers.values())} answers across {len(answers)} subjects', flush=True)

    # Step 4: load concept index
    print('\n[4] Loading concept index...', flush=True)
    units_index = load_concept_index()
    print(f'  → {len(units_index)} units, {sum(len(v) for v in units_index.values())} spokes', flush=True)

    # Step 5: per-problem mapping + write + collect
    print('\n[5] Mapping + writing markdown...', flush=True)
    DOCS_PROBLEMS.mkdir(parents=True, exist_ok=True)
    written = []
    for prob in sorted(problems, key=lambda p: p['number']):
        subj = classify_subject(prob['number'])
        ans = (answers.get(subj, {}) or answers.get('공통' if prob['number'] <= 22 else subj, {})).get(str(prob['number']))
        mapping = map_problem(prob['body'], prob['number'], prob['score'], units_index)
        out = write_markdown(prob, mapping, ans)
        written.append({'prob': prob, 'mapping': mapping, 'answer': ans})
        print(f'  [{prob["number"]:>2}] {subj:>8}  ans={ans!s:>4}  unit={mapping.get("unit","?") if mapping else "?"}', flush=True)

    # Step 6: DB upsert
    print('\n[6] Upserting to Postgres...', flush=True)
    db_upsert(written)

    # Done
    n = len(written)
    print(f'\n=== DONE: {n} problems ingested → docs/problems/ + DB ===', flush=True)


if __name__ == '__main__':
    main()
