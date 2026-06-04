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
import concurrent.futures as cf
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
import uuid
from datetime import datetime
from pathlib import Path
from textwrap import dedent

import psycopg
import fitz  # pymupdf

# Optional DeepSeek-OCR client (preferred for vision when healthy)
try:
    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).parent.parent))
    from ocr_client import ocr_page_to_markdown as _ds_ocr_page, is_healthy as _ds_is_healthy
    _DS_OCR_AVAILABLE = True
except Exception:
    _DS_OCR_AVAILABLE = False
    _ds_ocr_page = None
    _ds_is_healthy = lambda: False

VISION_WORKERS = 4   # parallel claude -p calls (per cta-law pattern)
MAP_WORKERS = 4

# ROOT는 MATHSTUDY_ROOT 환경변수로 오버라이드 가능 (git worktree에 적재할 때).
ROOT = Path(os.environ.get('MATHSTUDY_ROOT', '/home/insung/Projects/math-study'))
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
    """Invoke `claude -p`. Returns stdout text or None. Retries on failure.

    Timeout cap: callers pass 30 for haiku mapping (rest of the call should
    finish in 5-15s; if it doesn't, the prompt is malformed and retrying
    with the same body won't help — sleep+retry just stalls the thread).
    For timeout failures we still cool off between retries so we don't
    saturate Anthropic's rate limit in a tight loop."""
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
                time.sleep(5 + attempt * 5)
                continue
            print(f'  ! claude timeout after {timeout}s ({retries+1} attempts)', flush=True)
            return None
    return None


def download(url: str, dst: Path) -> bool:
    if dst.exists() and dst.stat().st_size > 1000:
        return True
    dst.parent.mkdir(parents=True, exist_ok=True)
    # Encode non-ASCII characters in the URL path (e.g. Korean)
    try:
        from urllib.parse import urlsplit, urlunsplit, quote
        parts = urlsplit(url)
        encoded = urlunsplit((parts.scheme, parts.netloc,
                              quote(parts.path, safe='/-._~'),
                              parts.query, parts.fragment))
    except Exception:
        encoded = url
    try:
        req = urllib.request.Request(encoded, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=60) as resp, open(dst, 'wb') as out:
            out.write(resp.read())
        return True
    except Exception as e:
        print(f'  ! download failed: {url}: {e}', flush=True)
        return False


def _record_missing(slug: str, raw_dir: Path, **fields) -> None:
    """Write/merge db/raw/{slug}/missing.json — round-level catalog of pages
    we couldn't OCR, problems whose body came back broken, answers we
    couldn't extract, and Claude mappings that gave up. Consumed by
    scripts/llm_fill_missing.py (Phase 2) to patch the gaps with LLM
    fallbacks. Each call merges into the existing file rather than
    overwriting — sanity loops and self-fix passes both append."""
    path = raw_dir / 'missing.json'
    try:
        existing = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    except Exception:
        existing = {}
    existing.setdefault('slug', slug)
    existing['ts'] = datetime.now().isoformat(timespec='seconds')
    for k, v in fields.items():
        if v is None:
            continue
        if isinstance(v, list):
            cur = existing.get(k, [])
            # de-dupe by JSON-encoded value
            seen = {json.dumps(x, ensure_ascii=False, sort_keys=True) for x in cur}
            for item in v:
                key = json.dumps(item, ensure_ascii=False, sort_keys=True)
                if key not in seen:
                    cur.append(item)
                    seen.add(key)
            existing[k] = cur
        elif isinstance(v, dict):
            cur = existing.get(k, {})
            for kk, vv in v.items():
                if isinstance(vv, list):
                    cur_list = cur.get(kk, [])
                    cur[kk] = sorted(set(cur_list) | set(vv))
                else:
                    cur[kk] = vv
            existing[k] = cur
        else:
            existing[k] = v
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding='utf-8')
    except Exception as e:
        print(f'  ! _record_missing write failed: {e}', flush=True)


def _prepass_clear_stale_pages(work_dir: Path, pdf_path: Path) -> int:
    """Delete page-MD caches whose detected problem numbers OR area header
    don't match the PDF text-layer ground truth. Run BEFORE OCR/mapping so
    stale caches don't drag the detected-problems count down (triggers a
    full re-mapping pass later, wasting Claude calls) or misroute problems
    into the wrong subject bucket (공통 21,22 leaking into 확률과통계 because
    OCR misread the page footer's '선택과목(확률과 통계)' advisory)."""
    if not work_dir.exists() or not pdf_path.exists():
        return 0
    try:
        from ocr_client import _canonical_area_for_page  # type: ignore
    except Exception:
        _canonical_area_for_page = lambda p, n: None  # noqa: E731
    try:
        d = fitz.open(pdf_path)
        canonical_nums: dict[int, set[int]] = {}
        canonical_areas: dict[int, str | None] = {}
        for i, p in enumerate(d):
            t = p.get_text()
            nums: set[int] = set()
            for m in re.finditer(r'(?:^|\n)\s*(\d{1,2})\.\s', t):
                n = int(m.group(1))
                if 1 <= n <= 50:
                    nums.add(n)
            canonical_nums[i + 1] = nums
            canonical_areas[i + 1] = _canonical_area_for_page(pdf_path, i + 1)
        d.close()
    except Exception:
        return 0
    removed = 0
    for md in work_dir.glob('p*.md'):
        try:
            pn = int(md.stem[1:])
        except ValueError:
            continue
        canon = canonical_nums.get(pn, set())
        if not canon:
            continue
        body = md.read_text(encoding='utf-8', errors='replace')
        detected = {int(m.group(1)) for m in re.finditer(r'^##\s*(\d+)\s*번', body, re.MULTILINE)}
        cached_area_m = re.match(r'#\s*영역\s*:\s*(\S+)', body)
        cached_area = cached_area_m.group(1) if cached_area_m else None
        pdf_area = canonical_areas.get(pn)
        ELECTIVES = {'확률과통계', '미적분', '기하'}
        if pdf_area is not None:
            # PDF says elective — cache must match
            area_bad = cached_area != pdf_area
        elif cached_area in ELECTIVES:
            # PDF says 공통 (no `(확통/미적분/기하)` header) but cache
            # labelled it as an elective → OCR misread the page footer
            area_bad = True
        else:
            area_bad = False
        if detected != canon or area_bad:
            md.unlink()
            removed += 1
    return removed


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
    """Parallelized vision conversion via ThreadPoolExecutor (cta-law pattern).
    OAuth claude -p supports concurrent threads within a single process."""
    work_dir.mkdir(parents=True, exist_ok=True)
    results: dict[int, str] = {}

    # Pre-split: cached vs needs-fetch. Drop caches that look like Korean error
    # messages (Claude returns "찾을 수 없습니다" / "권한" when Read fails).
    todo = []
    for png in page_files:
        page_num = int(re.match(r'p(\d+)\.png', png.name).group(1))
        cache = work_dir / f'p{page_num:02d}.md'
        if cache.exists() and cache.stat().st_size > 50:
            body = cache.read_text(encoding='utf-8')
            head = body[:400]
            looks_valid = ('## ' in body) and ('찾을 수 없' not in head) and ('권한' not in head)
            if looks_valid:
                results[page_num] = body
                print(f'  [page {page_num:>2}] cached', flush=True)
                continue
            cache.unlink()
            print(f'  [page {page_num:>2}] cache invalid (error msg) — re-fetching', flush=True)
        todo.append((page_num, png, cache))

    if not todo:
        return results

    # 100% DeepSeek-OCR — no Claude vision, no text-layer fallback.
    # If DeepSeek server is unhealthy, abort immediately.
    if not (_DS_OCR_AVAILABLE and _ds_is_healthy()):
        raise RuntimeError('DeepSeek-OCR server unreachable — aborting (this pipeline is DS-OCR only)')

    pages_dir = Path(add_dir)
    figures_dir = pages_dir.parent / 'figures'
    prob_pdf_path = pages_dir.parent / '문제.pdf'

    # Sequential — DS-OCR (Ollama) serializes anyway.
    # Per-page retry up to 5x with backoff. ocr_client triggers a full
    # ollama serve+runner SSH restart after 2 consecutive fails (~10s
    # recovery), so retries 3+ run on a freshly cold-loaded runner.
    # On final failure: record in missing.json so Phase-2 LLM patcher
    # can fall back to PyMuPDF text-layer or an Opus pass.
    MAX_PAGE_RETRIES = 5
    raw_dir = work_dir.parent
    slug = raw_dir.name
    failed_pages: list[dict] = []
    for item in todo:
        page_num, png, cache = item
        md = None
        for attempt in range(MAX_PAGE_RETRIES):
            t0 = time.time()
            try:
                md = _ds_ocr_page(png, figures_dir=figures_dir, page_num=page_num,
                                  pdf_path=prob_pdf_path if prob_pdf_path.exists() else None)
            except Exception as e:
                print(f'  [page {page_num:>2}] DS-OCR error (try {attempt+1}): {e}', flush=True)
                md = None
            dt = time.time() - t0
            if md and '## ' in md:
                cache.write_text(md, encoding='utf-8')
                results[page_num] = md
                src_label = 'ds-ocr' if attempt == 0 else f'ds-ocr-retry{attempt}'
                print(f'  [page {page_num:>2}] {len(md)} chars ({dt:.1f}s {src_label})', flush=True)
                break
            print(f'  [page {page_num:>2}] try {attempt+1}/{MAX_PAGE_RETRIES} failed ({dt:.1f}s)', flush=True)
            if attempt < MAX_PAGE_RETRIES - 1:
                time.sleep(5 + attempt * 3)
        else:
            print(f'  [page {page_num:>2}] FAILED after {MAX_PAGE_RETRIES} retries — page skipped', flush=True)
            # Catalog the unrecoverable page so Phase-2 can fall back.
            canon: list[int] = []
            try:
                d = fitz.open(prob_pdf_path)
                t = d[page_num - 1].get_text() if page_num - 1 < len(d) else ''
                canon = sorted({int(m.group(1)) for m in re.finditer(r'(?:^|\n)\s*(\d{1,2})\.\s', t)
                                if 1 <= int(m.group(1)) <= 50})
                d.close()
            except Exception:
                pass
            failed_pages.append({'page': page_num, 'reason': 'ocr_unrecoverable',
                                 'attempts': MAX_PAGE_RETRIES, 'canonical_nums': canon})
    if failed_pages:
        _record_missing(slug, raw_dir, missing_pages=failed_pages)
    return results


def _build_textlayer_fallback_md(page_num: int, pages_dir_str: str) -> str | None:
    """Construct a minimal markdown for a single PDF page using PyMuPDF text.
    Used when vision fails — preserves problem numbers so split_problems
    detects them, with garbled-glyph text body as best-effort content."""
    try:
        pages_dir = Path(pages_dir_str)
        # The 문제.pdf is at pages_dir.parent / '문제.pdf'
        pdf_path = pages_dir.parent / '문제.pdf'
        if not pdf_path.exists():
            return None
        d = fitz.open(pdf_path)
        if page_num - 1 >= len(d):
            d.close()
            return None
        page = d[page_num - 1]
        text = page.get_text()
        d.close()
    except Exception:
        return None

    # Detect subject from page text
    area = None
    if '확률과통계' in text or '확률통계' in text:
        area = '확률과통계'
    elif '미적분' in text:
        area = '미적분'
    elif '기하' in text:
        area = '기하'
    elif '수학영역' in text:
        area = '공통'

    # Split text into per-problem chunks by '<num>.' pattern
    parts = re.split(r'(?:^|\n)\s*(\d{1,2})\.\s', text)
    # parts = [preamble, num1, body1, num2, body2, ...]
    md_lines: list[str] = []
    if area:
        md_lines.append(f'# 영역: {area}')
        md_lines.append('')
    has_any = False
    for i in range(1, len(parts), 2):
        try:
            num = int(parts[i])
        except (ValueError, IndexError):
            continue
        if not (1 <= num <= 50):
            continue
        body = parts[i + 1].strip() if i + 1 < len(parts) else ''
        body = body[:2000]  # avoid bleeding into next page if multi-page split
        # 단답형 marker
        if '단답형' in text and num >= 22:
            score_marker = '[4점]'
        else:
            score_marker = '[3점]'
        md_lines.append(f'## {num}번 {score_marker}')
        md_lines.append('')
        md_lines.append(body)
        md_lines.append('')
        md_lines.append('---')
        md_lines.append('')
        has_any = True
    return '\n'.join(md_lines) if has_any else None


def _expected_numbers_per_page(pdf_path: Path) -> dict[int, list[int]]:
    """Use PyMuPDF text layer to recover the canonical problem number for each
    page of a Korean math exam PDF. Korean problem numbers (e.g. "19.", "29.")
    are reliable text even when formulas are in PUA glyphs.
    Returns {page_num: [sorted_unique_numbers]}."""
    out: dict[int, list[int]] = {}
    if not pdf_path.exists():
        return out
    try:
        d = fitz.open(pdf_path)
    except Exception:
        return out
    for i, p in enumerate(d):
        t = p.get_text()
        nums: set[int] = set()
        nums.update(int(n) for n in re.findall(r'(?:^|\n)\s*(\d{1,2})\.\s', t))
        nums.update(int(n) for n in re.findall(r'(?:^|[\s\(])(\d{1,2})번', t))
        out[i + 1] = sorted(n for n in nums if 1 <= n <= 50)
    d.close()
    return out


def realign_page_numbers(page_md: dict[int, str], pdf_path: Path, work_dir: Path) -> dict[int, str]:
    """Deterministic post-process: if a page's vision-extracted ## N번 headers
    don't match the PDF text-layer numbers BUT the counts match, rewrite the
    headers using the canonical numbers (positional alignment). This fixes
    common vision OCR confusion (19→21, 29→28 etc.) without needing re-vision.
    Mismatched counts are left alone so the L3 self-fix retry can handle them."""
    expected_per_page = _expected_numbers_per_page(pdf_path)
    if not expected_per_page:
        return page_md
    fixed = 0
    out: dict[int, str] = {}
    for page_num, body in page_md.items():
        expected = expected_per_page.get(page_num, [])
        detected = [int(m.group(1)) for m in re.finditer(r'^##\s*(\d+)\s*번', body, re.MULTILINE)]
        if expected and detected and len(detected) == len(expected) and detected != expected:
            # Positional rewrite: 1st detected → 1st expected, etc.
            it = iter(expected)
            new_body = re.sub(
                r'(^##\s*)(\d+)(\s*번)',
                lambda m: f'{m.group(1)}{next(it)}{m.group(3)}',
                body,
                flags=re.MULTILINE,
            )
            print(f'  ⇆ p{page_num:02d} realigned: {detected} → {expected}', flush=True)
            out[page_num] = new_body
            # Persist the correction to the page cache so subsequent runs benefit.
            cache = work_dir / f'p{page_num:02d}.md'
            try:
                cache.write_text(new_body, encoding='utf-8')
            except Exception:
                pass
            fixed += 1
        else:
            out[page_num] = body
    if fixed:
        print(f'  ✓ realigned {fixed} page(s) using PDF text-layer ground truth', flush=True)
    return out


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
    for p in concepts_dir.rglob('*.md'):
        text = p.read_text(encoding='utf-8')
        ctype = (re.search(r'^concept_type:\s*(\w+)', text, re.MULTILINE) or [None, ''])[1]
        if ctype == 'unit':
            units[p.stem] = []
    for p in concepts_dir.rglob('*.md'):
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
    base_user = f"""문제 번호: {number}, 배점: {score}점

문제 본문:
{prob_body[:2500]}

사용 가능한 wiki unit + 핵심 spoke:
{units_str[:6000]}

JSON 출력하라."""

    # Haiku occasionally returns malformed JSON (trailing commentary,
    # multiple objects concatenated, list-wrapped). Retry up to 3 times
    # with progressively stricter prompts before giving up — each retry
    # is one Haiku call (~$0.001), much cheaper than leaving unit=? gaps
    # that require manual classification later.
    last_err = None
    for attempt in range(3):
        if attempt == 0:
            user = base_user
        else:
            user = base_user + '\n\n중요: 오직 JSON 객체 하나만 출력하라. 코드펜스/주석/여러 객체 금지.'
        out = claude_p(MAP_SYSTEM, user, model='haiku', max_turns=1, timeout=30, retries=2)
        if not out:
            last_err = 'empty response'
            continue
        out = re.sub(r'^```(?:json)?\s*|\s*```$', '', out.strip(), flags=re.MULTILINE)
        # Try strict parse first
        try:
            parsed = json.loads(out)
        except Exception as e:
            # Salvage: take just the first {...} block
            m = re.search(r'\{.*?\}(?=\s*(?:\{|\Z))', out, re.DOTALL)
            if m:
                try:
                    parsed = json.loads(m.group(0))
                except Exception as e2:
                    last_err = f'parse failed (attempt {attempt+1}): {e}; salvage also failed: {e2}'
                    continue
            else:
                last_err = f'parse failed (attempt {attempt+1}): {e}'
                continue
        if isinstance(parsed, list):
            if parsed and isinstance(parsed[0], dict):
                parsed = parsed[0]
            else:
                last_err = f'returned non-dict list (attempt {attempt+1})'
                continue
        if isinstance(parsed, dict):
            if attempt > 0:
                print(f'  ✓ map recovered for #{number} on retry {attempt}', flush=True)
            break
        last_err = f'non-dict (attempt {attempt+1}): {type(parsed).__name__}'
    else:
        print(f'  ! map gave up for #{number} after 3 attempts: {last_err}', flush=True)
        return None

    # Normalize enum-like fields to satisfy DB CHECK constraints. Haiku
    # sometimes returns multi-value strings like '계산|응용' or values
    # outside the allowed set, which would otherwise crash db_upsert.
    ALLOWED_COG = {'계산', '개념', '응용', '추론', '통합'}
    ALLOWED_TIER = {'early', 'mid', 'killer'}
    def _normalize(val, allowed):
        if not val:
            return None
        if isinstance(val, list):
            val = val[0] if val else None
            if not val:
                return None
        s = str(val).strip()
        if s in allowed:
            return s
        for tok in re.split(r'[|,/、]', s):
            tok = tok.strip()
            if tok in allowed:
                return tok
        return None
    parsed['cognitive_type'] = _normalize(parsed.get('cognitive_type'), ALLOWED_COG)
    parsed['killer_tier'] = _normalize(parsed.get('killer_tier'), ALLOWED_TIER)
    return parsed


def _flatten_answers(data: dict, default_subject: str = '단일') -> dict[str, dict[str, str]]:
    """Normalize various JSON shapes Claude might return:
      {"공통": {"1":"3", ...}, "확률과통계": {...}, ...}  → keep as-is
      {"객관식": {"1":"3"}, "단답형": {"23":"5"}}        → merge under default_subject
      {"1":"3", "2":"5", ...}                           → wrap under default_subject
      {"정답표": {...}, "시험":...}                       → drill into '정답표'
    """
    if not isinstance(data, dict):
        return {}
    if '정답표' in data and isinstance(data['정답표'], dict):
        data = data['정답표']
    out: dict[str, dict[str, str]] = {}
    known_subjects = {'공통', '확률과통계', '미적분', '기하'}
    # Case 1: top-level keys look like subjects → keep nested
    if any(k in known_subjects for k in data.keys()):
        for k, v in data.items():
            if isinstance(v, dict):
                out.setdefault(k, {}).update({str(kk): str(vv) for kk, vv in v.items()})
        return out
    # Case 2: top-level keys are '객관식'/'단답형' → merge under default
    if {'객관식', '단답형'} & set(data.keys()):
        for v in data.values():
            if isinstance(v, dict):
                out.setdefault(default_subject, {}).update({str(kk): str(vv) for kk, vv in v.items()})
        return out
    # Case 3: top-level is {number: answer}
    if all(str(k).isdigit() or (isinstance(k, int)) for k in data.keys()):
        out[default_subject] = {str(k): str(v) for k, v in data.items()}
        return out
    return {}


def _extract_json_blob(text: str) -> str | None:
    """Strip code fences + prose prefix and pull out the first balanced JSON object."""
    text = text.strip()
    text = re.sub(r'^```(?:json)?\s*|\s*```$', '', text, flags=re.MULTILINE)
    # Find the first '{' and walk to the matching '}'
    start = text.find('{')
    if start < 0:
        return None
    depth = 0
    in_str = False
    esc = False
    for i in range(start, len(text)):
        c = text[i]
        if in_str:
            if esc:
                esc = False
            elif c == '\\':
                esc = True
            elif c == '"':
                in_str = False
            continue
        if c == '"':
            in_str = True
        elif c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return text[start:i+1]
    return None


CIRCLE_TO_DIGIT = {'①': '1', '②': '2', '③': '3', '④': '4', '⑤': '5'}


def _ascii_int(tok: str) -> int | None:
    if tok and all('0' <= c <= '9' for c in tok):
        try:
            return int(tok)
        except ValueError:
            return None
    return None


def _parse_kice_column_major(full: str) -> dict[str, dict[str, str]]:
    """Parse the classic KICE 정답표 layout where the answer table is laid out
    as 5 columns × 11 rows (text-extracted as (n, ans, score) triples in
    column-major order across each row):
        col1: 공통 1-11
        col2: 공통 12-22
        col3: 확률과통계 23-30
        col4: 미적분 23-30
        col5: 기하 23-30
    """
    tokens = re.findall(r'[①②③④⑤]|\d+', full)
    out: dict[str, dict[str, str]] = {'공통': {}, '확률과통계': {}, '미적분': {}, '기하': {}}
    elective_count: dict[int, int] = {}
    i = 0
    while i < len(tokens) - 2:
        n = _ascii_int(tokens[i])
        if n is None or not (1 <= n <= 50):
            i += 1
            continue
        ans_tok = tokens[i + 1]
        ans = CIRCLE_TO_DIGIT.get(ans_tok)
        if ans is None:
            a_int = _ascii_int(ans_tok)
            if a_int is not None and 1 <= len(ans_tok) <= 4:
                ans = ans_tok
        if ans is None:
            i += 1
            continue
        score = _ascii_int(tokens[i + 2])
        if score is None or not (1 <= score <= 4):
            i += 1
            continue
        if n <= 22:
            subj = '공통'
        else:
            # 23-30: assign by occurrence: 1st=확률통계, 2nd=미적분, 3rd=기하
            elective_count[n] = elective_count.get(n, 0) + 1
            occ = elective_count[n]
            if occ > 3:
                i += 3
                continue
            subj = ['확률과통계', '미적분', '기하'][occ - 1]
        if str(n) not in out[subj]:
            out[subj][str(n)] = ans
        i += 3
    return {k: v for k, v in out.items() if v}


def extract_single_answers(ans_pdf) -> dict[str, dict[str, str]]:
    """통합형(선택과목 없는 단일 30문항) 정답표 파서 — 예: 2028 수능 예시문항.
    정답표가 3열 그리드여도 PDF 텍스트는 (번호, 정답, 배점) 트리플의 열-major
    나열이라, 1..30 트리플을 순서대로 읽어 전부 '단일' 버킷에 넣는다. 헤더의
    연도(2028) 같은 잡토큰은 번호 범위(1-30) 가드로 스킵해 재동기화한다.
    (기존 _parse_kice_column_major 는 공통+선택 5열 가정이라 단일형에 안 맞음.)"""
    try:
        d = fitz.open(ans_pdf)
        text = '\n'.join(pg.get_text('text') for pg in d)
        d.close()
    except Exception:
        return {}
    tokens = re.findall(r'[①②③④⑤]|\d+', text)
    out: dict[str, str] = {}
    i = 0
    while i < len(tokens) - 2:
        n = _ascii_int(tokens[i])
        if n is None or not (1 <= n <= 30):
            i += 1
            continue
        ans_tok = tokens[i + 1]
        ans = CIRCLE_TO_DIGIT.get(ans_tok)
        if ans is None:
            a_int = _ascii_int(ans_tok)
            if a_int is not None and 1 <= len(ans_tok) <= 4:
                ans = ans_tok
        if ans is None:
            i += 1
            continue
        score = _ascii_int(tokens[i + 2])
        if score is None or not (1 <= score <= 5):
            i += 1
            continue
        if str(n) not in out:
            out[str(n)] = ans
        i += 3
    return {'단일': out} if out else {}


def _parse_answer_sequence(region: str, start_num: int) -> dict[str, str]:
    """Parse {N: ANS} pairs from a token-stream region where problems are
    numbered sequentially starting at `start_num`.

    Numeric answers are accepted only when they don't look like the next
    problem number — this guards against column-layout PDFs where '12' is
    the next problem number, not the answer to '2'. But in the 단답형 zone
    (problem numbers ≥ 23 for math), the answer can legitimately be any
    small integer including expected_next+1, so the guard is dropped there
    — otherwise a real 단답형 answer of 24 for Q23 gets rejected and the
    chain breaks for everything after.

    공통 zone 안에 단답형 (#16-22) 이 섞이는 회차도 있어 객관식/단답형
    경계를 번호로 미리 잘라낼 수는 없다. 대신 _parse_answer_text에서
    `(1번 ~ 22번)` 같은 헤더 범위 텍스트를 사전 제거하므로 "22"가 #1의
    답으로 잘못 잡히던 문제는 거기서 해결된다. 여기서는 next-problem-
    number 가드만 객관식 zone에 남겨두어 column-layout PDF의 12 → '12'
    매치 만 차단한다.
    """
    tokens = re.findall(r'[①②③④⑤]|\d+', region)
    answers: dict[str, str] = {}
    expected_next = start_num
    i = 0
    while i < len(tokens) - 1:
        n = _ascii_int(tokens[i])
        if n is not None and n == expected_next and 1 <= n <= 50:
            ans_tok = tokens[i + 1]
            ans = CIRCLE_TO_DIGIT.get(ans_tok)
            if ans is None:
                a_int = _ascii_int(ans_tok)
                if a_int is not None and len(ans_tok) <= 4:
                    # Drop next-number guard once we're past the 객관식
                    # zone (no false-positive risk for 단답형 N>22).
                    if expected_next >= 23 or a_int != expected_next + 1:
                        ans = ans_tok
            if ans is not None:
                answers[str(expected_next)] = ans
                expected_next += 1
                i += 2
                continue
        i += 1
    return answers


def _extract_answers_from_text(ans_pdf: Path, default_subject: str = '단일',
                               expected_count: int = 30) -> dict[str, dict[str, str]]:
    """Parse 정답 page's text layer. See _parse_answer_text for layout details."""
    if not ans_pdf.exists():
        return {}
    try:
        d = fitz.open(ans_pdf)
        full = '\n'.join(p.get_text() for p in d)
        d.close()
    except Exception:
        return {}
    return _parse_answer_text(full, default_subject, expected_count)


def _parse_answer_text(full: str, default_subject: str = '단일',
                       expected_count: int = 30) -> dict[str, dict[str, str]]:
    """Parse the 정답 text. Handles two layouts:

    SIMPLE (모의고사 고1/고2, 검정고시): single sequence 1, 2, ..., N
      → returned under {default_subject}.

    MULTI-SUBJECT (고3 모평/수능): 공통 1-22 + each elective 23-30. Subjects
    are detected via headers like `[공통]`, `[확률과통계]`, `[미적분]`, `[기하]`
    or `■ 공통`, `■ [선택: 확률과통계]` somewhere in the answer pages.

    Input can come from PDF text-layer OR DS-OCR output for image-only PDFs
    (e.g. 2025_수능 where the answer table was Distiller-outlined and has no
    extractable text)."""

    # Strip HTML tags + entities — DS-OCR markdown mode returns the answer
    # table as `<table><tr><td rowspan="2">...` and HTML attribute numbers
    # (rowspan="2", colspan="10") leak into the token stream as if they were
    # answer cells. Replace tags with spaces so cell contents survive but
    # attributes don't. Also normalize "공통과목" / "공통 과목" prefixes.
    full = re.sub(r'<[^>]+>', ' ', full)
    full = re.sub(r'&[a-z]+;', ' ', full)

    # EBSi 통합본-style 정답 PDFs include section headers that contain
    # literal problem-number ranges:
    #   "공통 (1번 ~ 22번)" / "선택과목: 확률과 통계 (23번 ~ 30번)"
    # The trailing digits would otherwise be parsed as the first answer
    # of that section (e.g. "23번 ~ 30번" → #23's answer = "30"). Wipe
    # any "N번 ~ M번" range token before tokenizing.
    full = re.sub(r'\d+\s*번\s*[~∼〜-]\s*\d+\s*번', ' ', full)

    # Decode PUA glyphs — EBSi 모의고사/학력평가 정답 PDFs embed 단답형
    # answers using Private Use Area code points (.. for 1..0)
    # because the custom font's glyph map has no Unicode entry. KICE official
    # PDFs are unaffected (their numbers render as plain ASCII). Decoding
    # turns "Q29: " into "Q29: 45" so the token stream parses.
    full = full.translate({0xe034 + i: ord(str(i + 1)) for i in range(9)} | {0xe03d: ord('0')})

    # Elective subject markers. Some PDFs use '[확률과통계]' inline, others
    # split as '확률과 통계\n[\n]\n23...' (bracket chars on separate lines).
    # Match the subject name alone followed within ~10 chars by '23' to locate it.
    # Elective subject markers. Each entry matches several layouts:
    #   [확률과통계]                          — KICE official
    #   확률과 통계 ... 23                    — bracket-on-newline EBSi
    #   선택: 확률                            — abbreviated EBSi
    #   선택과목: 확률과 통계 (23번 ~ 30번)   — EBSi 통합본 form (the one
    #                                            students get via taildrop)
    ELECTIVES = [
        ('확률과통계', re.compile(
            r'\[\s*확\s*률\s*과?\s*통\s*계\s*\]'
            r'|확\s*률\s*과?\s*통\s*계(?=[\s\[\]]*23)'
            r'|선\s*택\s*(?:과\s*목)?\s*[:：]?\s*확률')),
        ('미적분',   re.compile(
            r'\[\s*미\s*적\s*분\s*\]'
            r'|미\s*적\s*분(?=[\s\[\]]*23)'
            r'|선\s*택\s*(?:과\s*목)?\s*[:：]?\s*미적분')),
        ('기하',     re.compile(
            r'\[\s*기\s*하\s*\]'
            r'|기\s*하(?=[\s\[\]]*23)'
            r'|선\s*택\s*(?:과\s*목)?\s*[:：]?\s*기하')),
    ]
    elective_positions: list[tuple[int, str]] = []
    for subj, pat in ELECTIVES:
        for m in pat.finditer(full):
            elective_positions.append((m.start(), subj))
    elective_positions.sort()

    # 정답표 시작 anchor: FIRST occurrence of "정 답" / "정답" / "수학 정답".
    # The original max(...) call was buggy — 학평 정답+해설 PDFs contain
    # multiple subject tables (수학 → 영어 → 사회 ...) so max returns the
    # last subject's table position, missing the math table at the top.
    cands = [p for p in (full.find('정 답'), full.find('정답'), full.find('수학 정답')) if p >= 0]
    table_start = min(cands) if cands else 0
    # Prefer the first "1 [①②③④⑤]" pair anywhere it appears earliest —
    # the real answer table always opens with that pattern, while the
    # "정답" keyword may live further down the page (e.g. in the heading
    # of the 해설 section) and pull table_start past the table itself.
    # Whichever anchor comes first wins.
    first_pair = re.search(r'\b1\s*[\n\s]*[①②③④⑤]', full)
    if first_pair and (table_start == 0 or first_pair.start() < table_start):
        table_start = first_pair.start()
    # 정답표 종료 anchor: the bare "정답" matched the document title
    # "정답 및 해설" earlier, and "해설" inside that title was getting
    # matched as the end anchor too — chopping region down to 5 chars. Use
    # more specific markers that only appear at the actual 해설 section
    # start: "해 설" (spaced subheader) or "[출제의도]" (per-problem
    # commentary header). Search past table_start to skip the title.
    end_cands = []
    for marker in ('해 설', '[출제의도]', '[ 출제의도]'):
        idx = full.find(marker, table_start + 1)
        if idx > table_start:
            end_cands.append(idx)
    # Fallback: bare "해설" but only after a generous buffer past table_start
    fallback = full.find('해설', table_start + 100)
    if fallback > table_start:
        end_cands.append(fallback)
    end_idx = min(end_cands) if end_cands else len(full)

    out: dict[str, dict[str, str]] = {}

    # KICE column-major layout: header lists "공통 / 선택 / 확률과 통계 / 미적분 / 기하"
    # at top, then data in 5-column rows of (번호, 정답, 배점) tuples.
    # Detect by:
    #   (1) all four subject names within first 300 chars (header area), AND
    #   (2) KICE-specific column-header phrase "문항 번호" repeated (5 times
    #       for the 5 columns). EBSi 학평 정답 PDFs happen to mention all
    #       three elective names in the first page's "정답 및 해설" header
    #       but use a simple sequence layout, so the bare keyword check
    #       generates false positives — the "문항 번호" repetition is what
    #       actually distinguishes the KICE table.
    header_region = full[:300]
    has_all_subjects = (('확률과 통계' in header_region or '확률과통계' in header_region)
                        and '미적분' in header_region and '기하' in header_region)
    # "문항\n번호" or "문항 번호" appears at top of each of the 5 columns
    # in KICE 정답표 (text-layer extract may split or join the two words).
    has_kice_table = len(re.findall(r'문항\s*\n?\s*번호', full)) >= 4
    if has_all_subjects and has_kice_table and not elective_positions:
        col_major = _parse_kice_column_major(full)
        # Require ≥80% coverage so half-matches don't lock out the simpler
        # sequence parser below (which can pick up the missing 공통).
        if col_major and sum(len(v) for v in col_major.values()) >= expected_count * 0.8:
            return col_major

    if elective_positions:
        # Multi-subject layout (수능/모평/고3 모의고사):
        #   공통 region:   start → first elective marker
        #   each elective: marker → next marker (or EOF)
        # The "정답" anchor (table_start) is unreliable for 학평/모의고사
        # 정답+해설 PDFs because the doc title "정답 및 해설" appears partway
        # through the file — that location is after the actual 1-22 answer
        # table on page 1. Just scan from the start of the document up to
        # the first elective; the parser only picks numeric→answer pairs so
        # heading text doesn't interfere.
        first_elective_pos = min(p for p, _ in elective_positions)
        common_region = full[:first_elective_pos]
        common_ans = _parse_answer_sequence(common_region, 1)
        # 공통 max = 22 in KICE / 학평 / 고3 모의고사. Drop anything beyond
        # so the parser's natural number-sequence continuation doesn't leak
        # 23-24 (which belong to electives) into the 공통 bucket.
        common_ans = {k: v for k, v in common_ans.items() if int(k) <= 22}
        if common_ans:
            out['공통'] = common_ans

        # For each elective, region = from this marker to next subject marker
        # (don't truncate at 해설 — elective tables typically come after 해설 of 공통)
        seen_subj: set[str] = set()
        for idx, (pos, subj) in enumerate(elective_positions):
            if subj in seen_subj:
                continue  # only first occurrence
            seen_subj.add(subj)
            next_pos = len(full)
            for p2, s2 in elective_positions[idx + 1:]:
                if s2 != subj:
                    next_pos = p2
                    break
            region = full[pos:next_pos]
            sub_ans = _parse_answer_sequence(region, 23)
            if sub_ans:
                out[subj] = sub_ans

        if out:
            return out

    # Single-sequence layout (모의고사/검정고시): parse from '정답' to '해설'
    region = full[max(table_start, 0):end_idx]
    answers = _parse_answer_sequence(region, 1)
    if answers:
        out[default_subject] = answers
    return out


def _ocr_answer_pdf_pages(ans_pdf: Path, work_dir: Path) -> list[str]:
    """Render answer PDF pages to PNG (cached under work_dir/ans_pages) and
    OCR each via DeepSeek-OCR. Returns one OCR text per page (empty list on
    failure). Used as fallback when the PDF has no text layer — e.g.
    2025_수능 정답표 was exported with Distiller font-outline so PyMuPDF
    sees only vector drawings.

    Pages are returned separately so the caller can pick the best page —
    KICE 수능 정답.pdf has 홀수형 on p1 and 짝수형 on p2, which have
    different 객관식 answers (only the order of choices differs). Our
    문제.pdf is 홀수형, so we want p1's answers."""
    if not _DS_OCR_AVAILABLE or not _ds_is_healthy():
        print('    DS-OCR fallback: server not available', flush=True)
        return []
    ans_pages_dir = work_dir / 'ans_pages'
    ans_pages_dir.mkdir(exist_ok=True)
    try:
        doc = fitz.open(ans_pdf)
        for i, page in enumerate(doc):
            p = ans_pages_dir / f'ans_p{i+1:02d}.png'
            if not p.exists():
                page.get_pixmap(dpi=200).save(p)
        doc.close()
    except Exception as e:
        print(f'    DS-OCR fallback: render failed: {e}', flush=True)
        return []

    pages = sorted(ans_pages_dir.glob('ans_p*.png'))
    from ocr_client import ocr_page_raw
    out: list[str] = []
    for png in pages:
        cache = work_dir / f'{png.stem}_ocr.txt'
        if cache.exists() and cache.stat().st_size > 10:
            out.append(cache.read_text(encoding='utf-8'))
            print(f'    DS-OCR fallback: {png.name} cached', flush=True)
            continue
        print(f'    DS-OCR fallback: OCR {png.name}...', flush=True)
        try:
            r = ocr_page_raw(png, include_crops=False)
        except Exception as e:
            print(f'      ! OCR error: {e}', flush=True)
            out.append('')
            continue
        if r and r.get('text'):
            text = r['text']
            cache.write_text(text, encoding='utf-8')
            out.append(text)
            print(f'      ✓ {len(text)} chars', flush=True)
        else:
            out.append('')
    return out


def extract_answers(ans_pdf: Path, work_dir: Path, default_subject: str = '단일',
                    expected_count: int = 30) -> dict[str, dict[str, str]]:
    """Try PDF text-layer first (cheap, captures 객관식 reliably). If the PDF
    has no extractable text (e.g. 2025_수능 정답표 is font-outlined vector
    drawings only), fall back to DS-OCR on rendered pages and pipe the OCR
    text into the same multi-subject parser.

    Trade-off note for text-layer success path: 단답형 rendered as PUA glyphs
    may be missed, accepted as a trade-off — most 객관식 + many 단답형 are
    captured via the column-major parser."""
    if not ans_pdf.exists():
        return {}
    result = _extract_answers_from_text(ans_pdf, default_subject, expected_count)
    total = sum(len(v) for v in result.values())
    if total >= expected_count * 0.8:
        return result

    # Fallback: PDF text-layer was empty or unreliable — try DS-OCR.
    print(f'    text-layer extracted {total}/{expected_count} answers — DS-OCR fallback', flush=True)
    page_texts = _ocr_answer_pdf_pages(ans_pdf, work_dir)
    if not page_texts:
        return result  # whatever text-layer gave us

    # Two different strategies based on exam type:
    #
    # A) KICE 수능 정답.pdf has p1=홀수형, p2=짝수형 — both list the same
    #    questions but with DIFFERENT 객관식 choice order (so different
    #    answers). 문제.pdf is always 홀수형, so we MUST take only p1.
    #    Detect by default_subject == '공통' (수능/모평/고3 모의고사 use
    #    공통/확률통계/미적분/기하).
    #
    # B) Single-subject exam (모의고사 고1/고2, 학력평가, 검정고시) — answer
    #    table can span multiple pages because the PDF also contains 해설.
    #    Concatenate text from all pages so a 20-30 question table that's
    #    split across pages still parses fully.
    is_multi_subject = (default_subject == '공통')
    if is_multi_subject:
        p1_text = page_texts[0]
        if not p1_text:
            print('    DS-OCR fallback: p1 empty — skipping (must not use 짝수형)', flush=True)
            return result
        parsed = _parse_answer_text(p1_text, default_subject, expected_count)
        parsed_total = sum(len(v) for v in parsed.values())
        print(f'    DS-OCR fallback p1 (홀수형): parsed {parsed_total} answers', flush=True)
        return parsed if parsed_total > total else result

    # Single-subject: try concatenated text first (covers multi-page tables),
    # then per-page best as backup.
    joined = '\n'.join(t for t in page_texts if t)
    parsed = _parse_answer_text(joined, default_subject, expected_count)
    parsed_total = sum(len(v) for v in parsed.values())
    print(f'    DS-OCR fallback (joined, 단일): parsed {parsed_total} answers', flush=True)
    best, best_total = parsed, parsed_total
    for i, text in enumerate(page_texts):
        if not text:
            continue
        ppar = _parse_answer_text(text, default_subject, expected_count)
        ptot = sum(len(v) for v in ppar.values())
        if ptot > best_total:
            best, best_total = ppar, ptot
            print(f'    DS-OCR fallback p{i+1}: parsed {ptot} (new best)', flush=True)
    return best if best_total > total else result


def classify_subject(number: int, fallback: str = '공통', exam_type: str = '수능') -> str:
    """Fallback heuristic for problems without explicit area headers.
    검정고시는 25 단일 문제 — 공통/선택 구분 없음 → '단일' 고정."""
    if exam_type == '검정고시':
        return '단일'
    if number <= 22:
        return '공통'
    return fallback


def slugify_round(year: int, exam_type: str, session: str | None = None, grade: str | None = None) -> str:
    """Folder/slug name under db/raw/. Examples:
      수능       → 2024_수능
      모의평가    → 2024_9월모평 / 2024_6월모평
      모의고사    → 2024_고3_3월모의고사
      학력평가    → 2024_고3_3월학평
      검정고시    → 2024_중졸_1회 / 2024_고졸_2회
    """
    if exam_type == '수능':
        if session and '예시' in session: return f'{year}_예시'
        return f'{year}_수능'
    if exam_type == '모의평가':
        if session and '9월' in session: return f'{year}_9월모평'
        if session and '6월' in session: return f'{year}_6월모평'
        return f'{year}_{exam_type}'
    if exam_type == '모의고사':
        g = grade or '고3'
        return f'{year}_{g}_{session or "?"}모의고사'
    if exam_type == '학력평가':
        g = grade or '고3'
        return f'{year}_{g}_{session or "?"}학평'
    if exam_type == '검정고시':
        g = grade or '중졸'
        return f'{year}_{g}_{session or "1회"}'
    return f'{year}_{exam_type}'


def write_markdown(prob: dict, mapping: dict, answer: str | None, round_slug: str,
                   year: int, exam_type: str, session: str,
                   grade: str | None = None, agency: str = '평가원') -> Path:
    subject = prob.get('subject') or classify_subject(prob['number'], exam_type=exam_type)
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

    grade_yaml = f'\n          grade: {grade}' if grade else ''
    fm = dedent(f'''\
        ---
        sources: [pdf:db/raw/{round_slug}/문제.pdf, mirror:horaeng.com]
        created: {TODAY}
        updated: {TODAY}
        source:
          agency: {agency}
          exam_type: {exam_type}
          year: {year}
          session: {session}{grade_yaml}
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
    concept_links = '\n'.join(f'- [{c.replace("_"," ")}](../concepts/{c}.md)' for c in ([unit] + concepts) if c)
    body = (
        f'\n# [{year} {exam_type} {subject} {prob["number"]}번] {prob["score"]}점\n\n'
        f'> 출처: 평가원 {year}{"년" if exam_type == "모의고사" else "학년도"} {exam_type} {session} 수학영역 · 단원: {unit or "(매핑 필요)"}\n'
        f'> Tier: {killer or "?"} · cognitive: {cog or "?"} · 예상 시간 {et}초\n'
        f'> **{intent or "(intent missing)"}**\n\n'
        f'## 문제\n\n{prob["body"]}\n\n'
        f'## 풀이 (학습 시 채워짐)\n\n'
        f'본 페이지의 상세 풀이는 학습 시 직접 작성하거나, 페이지 하단 채팅창에서 LLM 튜터의 도움으로 채우세요.\n\n'
        f'## 매핑된 개념\n{concept_links}\n'
    )

    out.write_text(fm + body, encoding='utf-8')
    return out


def db_upsert(problems_with_meta: list[dict], year: int, exam_type: str, session: str, pdf_rel_path: str,
              grade: str | None = None, agency: str = '평가원') -> None:
    with psycopg.connect(DB) as conn, conn.cursor() as cur:
        cur.execute(
            """INSERT INTO exams (agency, exam_type, year, session, grade, source_pdf)
               VALUES (%s, %s, %s, %s, %s, %s)
               ON CONFLICT (agency, exam_type, year, session, grade) DO UPDATE SET ingested_at = NOW()
               RETURNING id""",
            (agency, exam_type, year, session, grade, pdf_rel_path),
        )
        exam_id = cur.fetchone()[0]
        round_slug = slugify_round(year, exam_type, session, grade)
        for item in problems_with_meta:
            prob = item['prob']
            mapping = item['mapping'] or {}
            ans = item['answer']
            subject = prob.get('subject') or classify_subject(prob['number'], exam_type=exam_type)
            slug = f'{round_slug}_{subject}_{prob["number"]:02d}'
            # v2 (PNG-First) passes image_path/image_paths via prob dict;
            # v1 (OCR) leaves them empty so old behavior keeps working.
            image_paths = prob.get('image_paths') or []
            has_image = bool(image_paths)
            cur.execute(
                """INSERT INTO problems
                     (exam_id, subject, number, score, format, text_markdown, has_image, image_paths,
                      answer, unit_slug, exam_intent, killer_tier, cognitive_type, expected_time_sec,
                      frontmatter_path)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                   ON CONFLICT (exam_id, subject, number) DO UPDATE SET
                     score = EXCLUDED.score, format = EXCLUDED.format,
                     text_markdown = EXCLUDED.text_markdown,
                     has_image = EXCLUDED.has_image, image_paths = EXCLUDED.image_paths,
                     answer = EXCLUDED.answer,
                     unit_slug = EXCLUDED.unit_slug, exam_intent = EXCLUDED.exam_intent,
                     killer_tier = EXCLUDED.killer_tier, cognitive_type = EXCLUDED.cognitive_type,
                     expected_time_sec = EXCLUDED.expected_time_sec
                   RETURNING id""",
                (exam_id, subject, prob['number'], prob['score'], prob['format'],
                 prob.get('searchable_text') or prob.get('body') or '',
                 has_image, image_paths, ans, mapping.get('unit') or None,
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


def ingest_round(year: int, exam_type: str, session: str, pdf_url: str | None = None, ans_url: str | None = None,
                 grade: str | None = None, agency: str = '평가원') -> dict:
    round_slug = slugify_round(year, exam_type, session, grade)
    raw = ROOT / 'db' / 'raw' / round_slug
    label = f'{exam_type}, {session}' + (f', {grade}' if grade else '')
    t_round_start = time.time()
    print(f'\n══════ {round_slug} ({label}) ══════', flush=True)

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
    work.mkdir(parents=True, exist_ok=True)
    # Pre-pass: delete page-MD caches whose detected problem numbers don't
    # match the PDF text-layer canonical numbers BEFORE OCR/mapping. Without
    # this, a stale cache from a buggy earlier OCR run leaks into the
    # detected-problems list — we under-count, run mapping (paid Claude
    # call) on the partial set, THEN clear_suspect_pages triggers self-fix
    # and we re-map all problems from scratch. Doing the check up-front
    # avoids the wasted mapping pass.
    _prepass_cleared = _prepass_clear_stale_pages(work, prob_pdf)
    if _prepass_cleared:
        print(f'  [prepass] cleared {_prepass_cleared} stale page caches', flush=True)
    page_md = convert_pages(page_files, work, str(pages_dir))
    page_md = realign_page_numbers(page_md, prob_pdf, work)

    combined = '\n\n---\n\n'.join(page_md[i] for i in sorted(page_md.keys()))
    problems = split_problems(combined)
    print(f'  ✓ {len(problems)} problems detected', flush=True)
    if not problems:
        return {'round': round_slug, 'ok': False, 'reason': 'no problems detected'}

    # 고3 모의고사/학력평가 정답표는 수능 형식 (공통 1-22 + 선택 23-30 ×3).
    # default_subject='단일'로 처리하면 단순 sequence 파서가 23번에서
    # 첫 선택과목 정답을 잡고 거기서 종료되어 24-30이 누락됨.
    if exam_type in ('모의고사', '학력평가') and grade == '고3':
        default_ans_subj = '공통'
    elif exam_type in ('모의고사', '학력평가', '검정고시'):
        default_ans_subj = '단일'
    else:
        default_ans_subj = '공통'
    expected_problem_count = len(problems)
    answers = extract_answers(ans_pdf, work, default_subject=default_ans_subj,
                              expected_count=expected_problem_count) if ans_pdf.exists() else {}
    print(f'  ✓ answers: {sum(len(v) for v in answers.values())} entries', flush=True)

    # Pre-map sanity (up to 3 passes): catch both classes of OCR failure
    # BEFORE mapping enters Claude haiku territory:
    #   (a) "missing" — answer table has Q23 but split_problems didn't find it
    #   (b) "garbled body" — `## 28번` detected but body is OCR garbage like
    #       '중 / 만족 / (7) / (8) ...' — almost no Korean text, no LaTeX,
    #       just stray tokens. Naive length-only checks (>200c) also flagged
    #       LEGITIMATE short problems like "두 함수 f(x)=x^2의 미분을 구하시오.
    #       [3점]" (~50 Korean chars + LaTeX) → infinite redo loop. So the
    #       garbled-body signal is: Korean char count below a small floor
    #       AND LaTeX dollar count low. Real short problems always have
    #       enough of one or the other.
    def _looks_garbled(body: str) -> bool:
        korean_chars = sum(1 for c in body if '가' <= c <= '힣')
        latex_dollars = body.count('$')
        # Heuristic: legitimate problems have ≥15 Korean chars OR ≥4 $ (2 math expressions)
        return korean_chars < 15 and latex_dollars < 4

    prev_redo: set[int] = set()
    for sanity_attempt in range(3):
        ans_nums: set[int] = set()
        for sub_map in answers.values():
            for k in sub_map.keys():
                try:
                    ans_nums.add(int(k))
                except ValueError:
                    pass
        detected_nums = {p['number'] for p in problems}
        missing = ans_nums - detected_nums
        garbled = {p['number'] for p in problems if _looks_garbled(p['body'])}
        needs_redo = missing | garbled
        if not needs_redo:
            break
        try:
            d = fitz.open(prob_pdf)
            pages_to_redo: set[int] = set()
            for i, p in enumerate(d):
                t = p.get_text()
                canon = {int(m.group(1)) for m in re.finditer(r'(?:^|\n)\s*(\d{1,2})\.\s', t)
                         if 1 <= int(m.group(1)) <= 50}
                if canon & needs_redo:
                    pages_to_redo.add(i + 1)
            d.close()
        except Exception:
            pages_to_redo = set()
        if not pages_to_redo:
            break
        # Early break: if this iteration would re-OCR the exact same pages
        # as the previous pass, the OCR result isn't going to change —
        # bail out and let the missing.json + Phase-2 patcher handle it.
        if pages_to_redo == prev_redo:
            print(f'  [sanity pass {sanity_attempt+1}/3] same pages as prev — OCR plateaued, stopping early', flush=True)
            break
        prev_redo = pages_to_redo
        print(f'  [sanity pass {sanity_attempt+1}/3] missing={sorted(missing)} garbled={sorted(garbled)} → redo pages {sorted(pages_to_redo)}', flush=True)
        for pn in pages_to_redo:
            (work / f'p{pn:02d}.md').unlink(missing_ok=True)
        page_md = convert_pages(page_files, work, str(pages_dir))
        page_md = realign_page_numbers(page_md, prob_pdf, work)
        combined = '\n\n---\n\n'.join(page_md[i] for i in sorted(page_md.keys()))
        problems = split_problems(combined)
        print(f'  ✓ {len(problems)} problems detected (after redo)', flush=True)

    # After loop (with or without break): tally remaining gaps + drop garbled.
    still_missing = sorted(ans_nums - {p['number'] for p in problems})
    still_garbled = sorted({p['number'] for p in problems if _looks_garbled(p['body'])})
    if still_missing or still_garbled:
        print(f'  [sanity] residual after redo: missing={still_missing} garbled={still_garbled}', flush=True)
        _record_missing(round_slug, raw,
                        missing_numbers=still_missing,
                        garbled_body_numbers=still_garbled,
                        reason_sanity='ocr_persistent_garble')
        # Drop garbled bodies so they don't poison the mapping step
        before = len(problems)
        problems = [p for p in problems if not _looks_garbled(p['body'])]
        if before != len(problems):
            print(f'  → mapping will skip {before - len(problems)} garbled-body problems', flush=True)

    units_index = load_concept_index()

    DOCS_PROBLEMS.mkdir(parents=True, exist_ok=True)
    sorted_probs = sorted(problems, key=lambda p: (p['subject'], p['number']))
    total_probs = len(sorted_probs)
    print(f'  → mapping {total_probs} problems via claude haiku ({MAP_WORKERS} parallel)', flush=True)
    t_map_start = time.time()

    # Per-round mapping cache: work/map_cache/{subject}_{number:02d}.json
    # Holds {body_sha, mapping}. body_sha invalidates when the OCR/realign
    # changes the problem text (self-fix replaces a stale page → new body
    # → cache miss → re-map). Without this, every self-fix pass re-maps
    # ALL problems with Claude haiku — burning $0.05 + 2 min per round.
    import hashlib
    map_cache_dir = work / 'map_cache'
    map_cache_dir.mkdir(parents=True, exist_ok=True)
    _cache_hits = 0
    _cache_lock = __import__('threading').Lock()

    ALLOWED_COG = {'계산', '개념', '응용', '추론', '통합'}
    ALLOWED_TIER = {'early', 'mid', 'killer'}
    def _normalize_mapping(m: dict) -> dict:
        """Sanitize enum-like fields from old cache entries that pre-date
        the map_problem-side normalization. Keeps cache hits cheap by
        avoiding cache invalidation churn."""
        def pick(val, allowed):
            if not val: return None
            if isinstance(val, list): val = val[0] if val else None
            if not val: return None
            s = str(val).strip()
            if s in allowed: return s
            for tok in re.split(r'[|,/、]', s):
                tok = tok.strip()
                if tok in allowed: return tok
            return None
        m['cognitive_type'] = pick(m.get('cognitive_type'), ALLOWED_COG)
        m['killer_tier'] = pick(m.get('killer_tier'), ALLOWED_TIER)
        return m

    def map_one(prob):
        nonlocal _cache_hits
        body_sha = hashlib.sha1(prob['body'].encode('utf-8')).hexdigest()[:12]
        cache_file = map_cache_dir / f'{prob["subject"]}_{prob["number"]:02d}.json'
        if cache_file.exists():
            try:
                data = json.loads(cache_file.read_text(encoding='utf-8'))
                if data.get('body_sha') == body_sha and isinstance(data.get('mapping'), dict):
                    with _cache_lock:
                        _cache_hits += 1
                    return prob, _normalize_mapping(data['mapping'])
            except Exception:
                pass
        m = map_problem(prob['body'], prob['number'], prob['score'], units_index)
        if isinstance(m, dict):
            try:
                cache_file.write_text(json.dumps({'body_sha': body_sha, 'mapping': m},
                                                 ensure_ascii=False, indent=2),
                                       encoding='utf-8')
            except Exception:
                pass
        return prob, m

    written_map: dict[tuple, dict] = {}
    map_failures: list[dict] = []
    done = 0
    with cf.ThreadPoolExecutor(max_workers=MAP_WORKERS) as ex:
        for prob, mapping in ex.map(map_one, sorted_probs):
            written_map[(prob['subject'], prob['number'])] = {'prob': prob, 'mapping': mapping}
            done += 1
            unit = (mapping or {}).get('unit', '?') if isinstance(mapping, dict) else '?'
            mark = '✓' if mapping else '✗'
            print(f'    [map {done:>2}/{total_probs}] {mark} #{prob["number"]:>2} {prob["subject"]:>8}  unit={unit}', flush=True)
            if not isinstance(mapping, dict):
                map_failures.append({'subject': prob['subject'], 'number': prob['number'],
                                     'reason': 'haiku_failed_or_timeout'})
    if map_failures:
        _record_missing(round_slug, raw, mapping_failures=map_failures)
    print(f'  → mapping done ({time.time() - t_map_start:.1f}s, cache hits {_cache_hits}/{total_probs}, fails {len(map_failures)})', flush=True)

    written = []
    for prob in sorted_probs:
        entry = written_map[(prob['subject'], prob['number'])]
        mapping = entry['mapping']
        subj = prob['subject']
        ans = (answers.get(subj, {}) or {}).get(str(prob['number']))
        # Fallback: non-수능 exams store answers under '단일' regardless of
        # whether vision labeled problems as '공통'. Try the only-key dict too.
        if ans is None and len(answers) == 1:
            only_key = next(iter(answers))
            if only_key != subj:
                ans = answers[only_key].get(str(prob['number']))
        # Preserve prior answer: if extraction missed it but existing markdown
        # had it (from a previous vision run), keep that value instead of
        # overwriting with empty.
        if ans is None:
            slug_check = f'{round_slug}_{subj}_{prob["number"]:02d}'
            existing_md = DOCS_PROBLEMS / f'{slug_check}.md'
            if existing_md.exists():
                try:
                    body = existing_md.read_text(encoding='utf-8')
                    m = re.search(r'^answer:\s*"([^"]*)"', body, re.MULTILINE)
                    if m and m.group(1):
                        ans = m.group(1)
                except Exception:
                    pass
        write_markdown(prob, mapping, ans, round_slug, year, exam_type, session, grade=grade, agency=agency)
        written.append({'prob': prob, 'mapping': mapping, 'answer': ans})
        print(f'  [{prob["number"]:>2}] {subj:>8}  ans={ans!s:>4}  unit={mapping.get("unit","?") if mapping else "?"}', flush=True)

    # Catalog answer gaps so the Phase-2 LLM patcher can fill them.
    missing_ans = [{'subject': w['prob']['subject'], 'number': w['prob']['number']}
                   for w in written if w['answer'] is None]
    if missing_ans:
        _record_missing(round_slug, raw, missing_answers=missing_ans)
    # Round-level summary in missing.json (overwrites prior counts, no list dedup churn)
    _record_missing(round_slug, raw,
                    expected_problems=expected_problem_count,
                    written_problems=len(written))

    try:
        db_upsert(written, year, exam_type, session, f'db/raw/{round_slug}/문제.pdf', grade=grade, agency=agency)
    except Exception as e:
        # DB upsert failed — markdown files were written but DB is stale.
        # Bubble up so auto_complete_rounds marks this round as failed
        # instead of silently moving on with an empty problems table.
        msg = str(e)[:300]
        print(f'  ✗ DB upsert failed: {msg}', flush=True)
        raise
    elapsed = time.time() - t_round_start
    print(f'  ✓ DB upsert {len(written)} problems  (round took {elapsed:.0f}s = {elapsed/60:.1f}m)', flush=True)
    return {'round': round_slug, 'ok': True, 'count': len(written)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--year', type=int)
    ap.add_argument('--exam-type', default='수능')
    ap.add_argument('--session', default='11월 본수능')
    ap.add_argument('--pdf-url')
    ap.add_argument('--ans-url')
    ap.add_argument('--grade')
    ap.add_argument('--agency', default='평가원')
    ap.add_argument('--manifest', help='JSON file with array of round configs')
    args = ap.parse_args()

    rounds = []
    if args.manifest:
        rounds = json.loads(Path(args.manifest).read_text(encoding='utf-8'))
    elif args.year:
        rounds = [{
            'year': args.year, 'exam_type': args.exam_type, 'session': args.session,
            'pdf_url': args.pdf_url, 'ans_url': args.ans_url,
            'grade': args.grade, 'agency': args.agency,
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
                grade=r.get('grade'),
                agency=r.get('agency', '평가원'),
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
