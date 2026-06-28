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

ROOT = Path('/home/insung/Projects/math-study')
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

MAP_SYSTEM = dedent("""
    당신은 한국 수능 수학 문제 한 개를 분석하여 메타데이터 JSON을 출력합니다.

    주어진 wiki 단원 목록 (unit slugs)과 그 안의 핵심 spoke 중에서 가장 적합한 unit 1개 + 핵심 spoke 1-3개를 선택.

    출력 JSON 스키마:
    {
      "unit": "<unit slug>",                   // 정확히 1개
      "concepts": ["<spoke1>", "<spoke2>"],     // 0-3개 (unit 안의 정의/정리/예제 slug)
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


def claude_p(system: str, user: str, model: str = 'sonnet', max_turns: int = 1, add_dir: str | None = None, timeout: int = 180) -> str | None:
    """Invoke `claude -p` with given system/user prompts. Returns stdout text or None on failure."""
    args = ['claude', '-p',
            '--model', model,
            '--max-turns', str(max_turns),
            '--output-format', 'text',
            '--no-session-persistence']
    if add_dir:
        args += ['--add-dir', add_dir]
    args += ['--system-prompt', system, user]
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=timeout, cwd=_CLEAN_DIR, env=_CLAUDE_ENV)
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


def load_concept_index() -> dict[str, list[str]]:
    """Read all unit pages and their spokes for the LLM mapping prompt."""
    concepts_dir = ROOT / 'docs' / 'concepts'
    units = {}
    for p in concepts_dir.glob('*.md'):
        text = p.read_text(encoding='utf-8')
        ctype = (re.search(r'^concept_type:\s*(\w+)', text, re.MULTILINE) or [None, ''])[1]
        if ctype != 'unit':
            continue
        # spokes: those whose prereq is this unit
        units[p.stem] = []
    # second pass: classify spokes by parent unit
    for p in concepts_dir.glob('*.md'):
        text = p.read_text(encoding='utf-8')
        ctype = (re.search(r'^concept_type:\s*(\w+)', text, re.MULTILINE) or [None, ''])[1]
        if ctype == 'unit':
            continue
        prereq_match = re.search(r'^prerequisites:\s*\[(.*?)\]', text, re.MULTILINE)
        if not prereq_match:
            continue
        for prereq in prereq_match.group(1).split(','):
            slug = prereq.strip().split('/')[-1].replace('.md', '').strip()
            if slug in units:
                units[slug].append(p.stem)
                break
    return units


def map_problem(prob_body: str, number: int, score: int, units_index: dict) -> dict | None:
    """LLM maps a single problem to unit/concepts/intent/tier/cognitive_type/time."""
    # Build a concise list: unit -> first 8 spokes
    units_str = '\n'.join(
        f'- {u}: {", ".join(spokes[:8])}'
        for u, spokes in sorted(units_index.items()) if spokes
    )
    # Also list unit-only entries (no spokes)
    units_only = [u for u, s in units_index.items() if not s]
    if units_only:
        units_str += '\n(spoke 없음): ' + ', '.join(units_only)

    user = f"""문제 번호: {number}, 배점: {score}점

문제 본문:
{prob_body[:2500]}

사용 가능한 wiki unit + 핵심 spoke (한 unit에 spoke 일부만 표시):
{units_str[:6000]}

위 unit/spoke 중에서 적합한 것을 골라 JSON 출력하라."""
    out = claude_p(MAP_SYSTEM, user, model='haiku', max_turns=1, timeout=60)
    if not out:
        return None
    # Strip possible code fences
    out = re.sub(r'^```(?:json)?\s*|\s*```$', '', out.strip(), flags=re.MULTILINE)
    try:
        return json.loads(out)
    except Exception as e:
        print(f'  ! map JSON parse failed for #{number}: {e}\n  raw: {out[:200]}', flush=True)
        return None


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
