#!/usr/bin/env python3
"""
Generalized KICE round ingester. Usage:

  python ingest_round.py \
      --year 2024 --exam-type 수능 --session "11월 본수능" \
      --pdf-url "https://horaeng.com/.../문제.pdf" \
      --ans-url "https://horaeng.com/.../정답.pdf"

Or from a manifest:
  python ingest_round.py --manifest rounds.json

Refactored from run_stage1.py for batch processing many rounds serially.
"""
from __future__ import annotations
import argparse
import json
import re
import subprocess
import sys
import time
import urllib.request
import uuid
from pathlib import Path
from textwrap import dedent

import psycopg
import fitz  # pymupdf

ROOT = Path('/home/insung/Projects/math-study')
DOCS_PROBLEMS = ROOT / 'docs' / 'problems'
DB = 'postgresql://mathstudy:mathstudy@127.0.0.1:5434/mathstudy'
TODAY = '2026-05-17'

VISION_SYSTEM = dedent("""
    당신은 한국 수능 수학 PDF 페이지를 한국어 markdown + KaTeX로 변환하는 변환기입니다.

    출력 규칙:
    1. 페이지 상단에 영역이 명시되어 있으면 그 영역(공통/확률과통계/미적분/기하)을 본문 첫 줄에 `# 영역: <영역명>` 헤더로 출력. 페이지 중간에 새 영역이 시작되면 그 부분에서도 출력. 영역 헤더는 다음 문제 전까지 유효.
    2. 각 문제는 `## N번 [X점]` 헤더로 시작 (N=문제번호, X=배점 2/3/4).
    3. 문제 본문 다음에 객관식 보기는 `(1) ... (2) ... (3) ... (4) ... (5) ...` 형식.
    4. 단답형 문제 (수능에서 22번까지는 객관식, 단답형은 보기 없음)는 보기 줄 없음.
    5. 수식은 KaTeX: inline `$...$`, display `$$...$$`, 케이스는 `\\begin{cases}...\\end{cases}`.
    6. 그림이 있는 문제는 `<!-- 그림: 한 줄 설명 -->` 주석으로.
    7. 페이지 번호·홀수형 라벨·저작권 문구·"5지선다형" 등 메타는 제외.
    8. 문제 사이는 `---` 구분선.

    영역명 매핑 단서:
    - "수학 영역" 단독 또는 "공통 과목"이라 표시되면 → 공통
    - "확률과 통계", "확률과통계" → 확률과통계
    - "미적분" → 미적분
    - "기하" → 기하

    출력은 변환된 markdown만, 다른 설명 일절 없음.
""").strip()

ANSWER_SYSTEM = dedent("""
    당신은 한국 수능 수학 정답표 PDF 페이지를 읽어 문제번호→정답을 JSON으로 출력합니다.

    출력 형식 예:
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

    주어진 wiki 단원 목록과 spoke 중에서 적합한 unit 1개 + 핵심 spoke 1-3개 선택.

    출력 JSON 스키마:
    {
      "unit": "<unit slug>",
      "concepts": ["<spoke1>", "<spoke2>"],
      "exam_intent": "<한 줄 요약>",
      "killer_tier": "early|mid|high|killer",
      "cognitive_type": "계산|개념|응용|추론|통합",
      "expected_time_sec": <정수>
    }

    killer_tier 가이드:
    - early: 1-15번대, 2-3점, 단순 계산
    - mid: 15-20번대, 3-4점, 표준 응용
    - high: 20-22번대, 4점, 까다로운 추론
    - killer: 21·22·28·29·30번대

    출력은 JSON만.
""").strip()


def claude_p(system: str, user: str, model: str = 'sonnet', max_turns: int = 1, add_dir: str | None = None, timeout: int = 180, retries: int = 2) -> str | None:
    """Invoke `claude -p`. Returns stdout text or None. Retries on failure."""
    args = ['claude', '-p',
            '--model', model,
            '--max-turns', str(max_turns),
            '--output-format', 'text',
            '--no-session-persistence']
    if add_dir:
        args += ['--add-dir', add_dir]
    args += ['--system-prompt', system, user]

    for attempt in range(retries + 1):
        try:
            r = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
            if r.returncode == 0 and r.stdout.strip():
                return r.stdout.strip()
            if attempt < retries:
                time.sleep(3 + attempt * 5)
                continue
            print(f'  ! claude failed (rc={r.returncode}, stderr={r.stderr[:200]!r}, stdout={r.stdout[:100]!r})', flush=True)
            return None
        except subprocess.TimeoutExpired:
            if attempt < retries:
                continue
            print(f'  ! claude timeout after {timeout}s', flush=True)
            return None
    return None


def download(url: str, dst: Path) -> bool:
    if dst.exists() and dst.stat().st_size > 1000:
        return True
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=60) as resp, open(dst, 'wb') as out:
            out.write(resp.read())
        return True
    except Exception as e:
        print(f'  ! download failed: {url}: {e}', flush=True)
        return False


def render_pdf_pages(pdf: Path, out_dir: Path, dpi: int = 200) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    existing = sorted(out_dir.glob('p*.png'))
    if existing:
        return existing
    doc = fitz.open(pdf)
    paths = []
    for i, page in enumerate(doc):
        out_path = out_dir / f'p{i+1:02d}.png'
        page.get_pixmap(dpi=dpi).save(out_path)
        paths.append(out_path)
    doc.close()
    return paths


def convert_pages(page_files: list[Path], work_dir: Path, add_dir: str) -> dict[int, str]:
    work_dir.mkdir(parents=True, exist_ok=True)
    results = {}
    for png in page_files:
        page_num = int(re.match(r'p(\d+)\.png', png.name).group(1))
        cache = work_dir / f'p{page_num:02d}.md'
        if cache.exists() and cache.stat().st_size > 50:
            results[page_num] = cache.read_text(encoding='utf-8')
            print(f'  [page {page_num:>2}] cached', flush=True)
            continue
        t0 = time.time()
        md = claude_p(
            VISION_SYSTEM,
            f'{png.name} 이미지를 Read 툴로 열어 페이지의 모든 문제를 markdown+KaTeX로 변환하라. 설명 없이 markdown만.',
            model='sonnet',
            max_turns=5,
            add_dir=add_dir,
            timeout=240,
            retries=2,
        )
        if md:
            cache.write_text(md, encoding='utf-8')
            results[page_num] = md
            print(f'  [page {page_num:>2}] {len(md)} chars ({time.time()-t0:.1f}s)', flush=True)
        else:
            print(f'  [page {page_num:>2}] FAILED', flush=True)
    return results


def split_problems(all_md: str) -> list[dict]:
    """Split by '## N번 [X점]' headers, tracking current section header
    '# 영역: <name>' (공통/확률과통계/미적분/기하). Dedup key is (subject, number).
    Default subject is '공통' until a '# 영역:' header switches it."""
    # Pattern to find either an area marker or a problem header.
    pattern = re.compile(
        r'^(?:#\s*영역\s*:\s*([^\n]+)|##\s*(\d+)\s*번\s*\[(\d+)점\])\s*$',
        re.MULTILINE,
    )
    problems = []
    matches = list(pattern.finditer(all_md))
    current_subject = '공통'
    for i, m in enumerate(matches):
        # Area marker?
        if m.group(1):
            area = m.group(1).strip()
            if '확률' in area:
                current_subject = '확률과통계'
            elif '미적' in area:
                current_subject = '미적분'
            elif '기하' in area:
                current_subject = '기하'
            else:
                current_subject = '공통'
            continue
        # Problem header
        number = int(m.group(2))
        score = int(m.group(3))
        start = m.end()
        # Find end: the next match (any kind), or end-of-text
        end = matches[i + 1].start() if i + 1 < len(matches) else len(all_md)
        body = all_md[start:end].strip()
        body = re.sub(r'\n---\s*$', '', body).strip()
        fmt = 'choice' if re.search(r'\(1\).*\(2\).*\(3\).*\(4\).*\(5\)', body, re.DOTALL) else 'numeric'
        key = (current_subject, number)
        existed = next((p for p in problems if (p['subject'], p['number']) == key), None)
        if existed:
            if len(body) > len(existed['body']):
                existed['body'] = body
                existed['score'] = score
                existed['format'] = fmt
        else:
            problems.append({
                'subject': current_subject,
                'number': number,
                'score': score,
                'body': body,
                'format': fmt,
            })
    return problems


def load_concept_index() -> dict[str, list[str]]:
    concepts_dir = ROOT / 'docs' / 'concepts'
    units = {}
    for p in concepts_dir.glob('*.md'):
        text = p.read_text(encoding='utf-8')
        ctype = (re.search(r'^concept_type:\s*(\w+)', text, re.MULTILINE) or [None, ''])[1]
        if ctype == 'unit':
            units[p.stem] = []
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
    units_str = '\n'.join(
        f'- {u}: {", ".join(spokes[:8])}'
        for u, spokes in sorted(units_index.items()) if spokes
    )
    units_only = [u for u, s in units_index.items() if not s]
    if units_only:
        units_str += '\n(spoke 없음): ' + ', '.join(units_only)
    user = f"""문제 번호: {number}, 배점: {score}점

문제 본문:
{prob_body[:2500]}

사용 가능한 wiki unit + 핵심 spoke:
{units_str[:6000]}

JSON 출력하라."""
    out = claude_p(MAP_SYSTEM, user, model='haiku', max_turns=1, timeout=60, retries=2)
    if not out:
        return None
    out = re.sub(r'^```(?:json)?\s*|\s*```$', '', out.strip(), flags=re.MULTILINE)
    try:
        return json.loads(out)
    except Exception as e:
        print(f'  ! map JSON parse failed for #{number}: {e}\n  raw: {out[:200]}', flush=True)
        return None


def extract_answers(ans_pdf: Path, work_dir: Path) -> dict[str, dict[str, str]]:
    if not ans_pdf.exists():
        return {}
    ans_pages_dir = work_dir / 'ans_pages'
    ans_pages_dir.mkdir(exist_ok=True)
    doc = fitz.open(ans_pdf)
    for i, page in enumerate(doc):
        p = ans_pages_dir / f'ans_p{i+1:02d}.png'
        if not p.exists():
            page.get_pixmap(dpi=200).save(p)
    doc.close()
    combined = {}
    for png in sorted(ans_pages_dir.glob('ans_p*.png')):
        cache = work_dir / f'{png.stem}.json'
        if cache.exists() and cache.stat().st_size > 5:
            data = json.loads(cache.read_text(encoding='utf-8'))
        else:
            raw = claude_p(
                ANSWER_SYSTEM,
                f'{png.name} 이미지를 Read 툴로 열고 정답표를 JSON으로 출력.',
                model='sonnet',
                max_turns=5,
                add_dir=str(ans_pages_dir),
                timeout=180,
                retries=2,
            )
            if not raw:
                continue
            raw = re.sub(r'^```(?:json)?\s*|\s*```$', '', raw.strip(), flags=re.MULTILINE)
            try:
                data = json.loads(raw)
            except Exception:
                continue
            cache.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        for subj, mapping in data.items():
            combined.setdefault(subj, {}).update(mapping)
    return combined


def classify_subject(number: int, fallback: str = '공통') -> str:
    """Fallback heuristic for problems without explicit area headers."""
    if number <= 22:
        return '공통'
    return fallback


def slugify_round(year: int, exam_type: str, session: str) -> str:
    # e.g., 2024_수능, 2024_9월모평
    if exam_type == '수능':
        return f'{year}_수능'
    if '9월' in session:
        return f'{year}_9월모평'
    if '6월' in session:
        return f'{year}_6월모평'
    return f'{year}_{exam_type}'


def write_markdown(prob: dict, mapping: dict, answer: str | None, round_slug: str,
                   year: int, exam_type: str, session: str) -> Path:
    subject = prob.get('subject') or classify_subject(prob['number'])
    slug = f'{round_slug}_{subject}_{prob["number"]:02d}'
    out = DOCS_PROBLEMS / f'{slug}.md'

    pid = str(uuid.uuid4())
    concepts = mapping.get('concepts', []) if mapping else []
    unit = mapping.get('unit', '') if mapping else ''
    intent = (mapping.get('exam_intent', '') if mapping else '').replace('"', "'")
    killer = mapping.get('killer_tier', '') if mapping else ''
    cog = mapping.get('cognitive_type', '') if mapping else ''
    et = mapping.get('expected_time_sec', 0) if mapping else 0

    concept_paths = [f'docs/concepts/{unit}.md'] if unit else []
    for c in concepts:
        cp = f'docs/concepts/{c}.md'
        if cp not in concept_paths:
            concept_paths.append(cp)
    concepts_yaml = ', '.join(concept_paths)

    fm = dedent(f'''\
        ---
        sources: [pdf:db/raw/{round_slug}/문제.pdf, mirror:horaeng.com]
        created: {TODAY}
        updated: {TODAY}
        source:
          agency: 평가원
          exam_type: {exam_type}
          year: {year}
          session: {session}
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

        # [{year} {exam_type} {subject} {prob["number"]}번] {prob["score"]}점

        > 출처: 평가원 {year}학년도 {exam_type} {session} 수학영역 · 단원: {unit or '(매핑 필요)'}
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


def db_upsert(problems_with_meta: list[dict], year: int, exam_type: str, session: str, pdf_rel_path: str) -> None:
    with psycopg.connect(DB) as conn, conn.cursor() as cur:
        cur.execute(
            """INSERT INTO exams (agency, exam_type, year, session, source_pdf)
               VALUES (%s, %s, %s, %s, %s)
               ON CONFLICT (agency, exam_type, year, session) DO UPDATE SET ingested_at = NOW()
               RETURNING id""",
            ('평가원', exam_type, year, session, pdf_rel_path),
        )
        exam_id = cur.fetchone()[0]
        round_slug = slugify_round(year, exam_type, session)
        for item in problems_with_meta:
            prob = item['prob']
            mapping = item['mapping'] or {}
            ans = item['answer']
            subject = prob.get('subject') or classify_subject(prob['number'])
            slug = f'{round_slug}_{subject}_{prob["number"]:02d}'
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
            cur.execute('DELETE FROM problem_concepts WHERE problem_id = %s', (pid,))
            unit = mapping.get('unit')
            if unit:
                cur.execute(
                    """INSERT INTO problem_concepts (problem_id, concept_slug, weight, is_primary)
                       VALUES (%s, %s, 1.0, TRUE) ON CONFLICT DO NOTHING""",
                    (pid, unit),
                )
            for spoke in mapping.get('concepts', []) or []:
                cur.execute(
                    """INSERT INTO problem_concepts (problem_id, concept_slug, weight, is_primary)
                       VALUES (%s, %s, 0.8, FALSE) ON CONFLICT DO NOTHING""",
                    (pid, spoke),
                )
        conn.commit()


def ingest_round(year: int, exam_type: str, session: str, pdf_url: str | None = None, ans_url: str | None = None) -> dict:
    round_slug = slugify_round(year, exam_type, session)
    raw = ROOT / 'db' / 'raw' / round_slug
    print(f'\n══════ {round_slug} ({exam_type}, {session}) ══════', flush=True)

    prob_pdf = raw / '문제.pdf'
    ans_pdf = raw / '정답.pdf'
    if pdf_url and not prob_pdf.exists():
        if not download(pdf_url, prob_pdf):
            return {'round': round_slug, 'ok': False, 'reason': 'pdf download failed'}
        print(f'  ✓ downloaded {prob_pdf.name} ({prob_pdf.stat().st_size//1024}KB)', flush=True)
    if ans_url and not ans_pdf.exists():
        download(ans_url, ans_pdf)
        if ans_pdf.exists():
            print(f'  ✓ downloaded {ans_pdf.name} ({ans_pdf.stat().st_size//1024}KB)', flush=True)

    pages_dir = raw / 'pages'
    page_files = render_pdf_pages(prob_pdf, pages_dir)
    print(f'  ✓ {len(page_files)} pages rendered', flush=True)

    work = raw / 'work'
    page_md = convert_pages(page_files, work, str(pages_dir))

    combined = '\n\n---\n\n'.join(page_md[i] for i in sorted(page_md.keys()))
    problems = split_problems(combined)
    print(f'  ✓ {len(problems)} problems detected', flush=True)
    if not problems:
        return {'round': round_slug, 'ok': False, 'reason': 'no problems detected'}

    answers = extract_answers(ans_pdf, work) if ans_pdf.exists() else {}
    print(f'  ✓ answers: {sum(len(v) for v in answers.values())} entries', flush=True)

    units_index = load_concept_index()

    written = []
    DOCS_PROBLEMS.mkdir(parents=True, exist_ok=True)
    for prob in sorted(problems, key=lambda p: (p['subject'], p['number'])):
        subj = prob['subject']
        ans = (answers.get(subj, {}) or {}).get(str(prob['number']))
        mapping = map_problem(prob['body'], prob['number'], prob['score'], units_index)
        write_markdown(prob, mapping, ans, round_slug, year, exam_type, session)
        written.append({'prob': prob, 'mapping': mapping, 'answer': ans})
        print(f'  [{prob["number"]:>2}] {subj:>8}  ans={ans!s:>4}  unit={mapping.get("unit","?") if mapping else "?"}', flush=True)

    db_upsert(written, year, exam_type, session, f'db/raw/{round_slug}/문제.pdf')
    print(f'  ✓ DB upsert {len(written)} problems', flush=True)
    return {'round': round_slug, 'ok': True, 'count': len(written)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--year', type=int)
    ap.add_argument('--exam-type', default='수능')
    ap.add_argument('--session', default='11월 본수능')
    ap.add_argument('--pdf-url')
    ap.add_argument('--ans-url')
    ap.add_argument('--manifest', help='JSON file with array of round configs')
    args = ap.parse_args()

    rounds = []
    if args.manifest:
        rounds = json.loads(Path(args.manifest).read_text(encoding='utf-8'))
    elif args.year:
        rounds = [{
            'year': args.year, 'exam_type': args.exam_type, 'session': args.session,
            'pdf_url': args.pdf_url, 'ans_url': args.ans_url,
        }]
    else:
        ap.error('--year/--exam-type/--session or --manifest required')

    summary = []
    for r in rounds:
        try:
            result = ingest_round(
                year=r['year'],
                exam_type=r['exam_type'],
                session=r['session'],
                pdf_url=r.get('pdf_url'),
                ans_url=r.get('ans_url'),
            )
            summary.append(result)
        except Exception as e:
            summary.append({'round': r.get('exam_type'), 'ok': False, 'reason': str(e)})
            print(f'  !! round error: {e}', flush=True)

    print('\n═══════ Summary ═══════')
    for s in summary:
        status = '✓' if s.get('ok') else '✗'
        print(f'  {status} {s.get("round"):<24}  {s}', flush=True)


if __name__ == '__main__':
    main()
