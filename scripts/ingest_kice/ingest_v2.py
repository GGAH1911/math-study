#!/usr/bin/env python3
"""PNG-First per-round ingest pipeline (replaces OCR-based ingest_round.py).

Flow:
    1. Render PDF pages to PNG (200 DPI)              — reuse render_pdf_pages
    2. Identify problem bboxes via PDF text-layer     — bbox.extract_problem_bboxes
    3. Crop one PNG per problem                       — bbox.crop_problem_image
    4. Sonnet 4.6 vision → metadata JSON (cached)     — vision_meta.extract_metadata
    5. Extract answers from 정답.pdf (text + DS-OCR)   — reuse extract_answers
    6. Write per-problem markdown shell + DB upsert   — write_markdown_v2 + db_upsert

No OCR for problem body. Body is the PNG (visual ground truth). Markdown
holds the searchable_text shadow for LLM/tutor consumption.
"""
from __future__ import annotations
import concurrent.futures as cf
import json
import re
import sys
import time
import uuid
from datetime import datetime, date
from pathlib import Path
from textwrap import dedent

_HERE = Path(__file__).parent
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_HERE.parent))

from bbox import extract_problem_bboxes, crop_problem_image, _collect_text_lines, _column_of  # noqa: E402
from crop_with_llm import crop_by_gap, crop_problem  # noqa: E402  (v3.1: pure-PIL, no LLM)
from text_meta import extract_metadata  # noqa: E402  (PDF text + Haiku, NOT vision)
from ingest_round import (  # noqa: E402
    render_pdf_pages, extract_answers, extract_single_answers, db_upsert, slugify_round,
    load_concept_index, classify_subject, download,
    ROOT, DOCS_PROBLEMS, TODAY,
)
from answer_textlayer import (parse_answer_table, parse_single_answer_table,  # noqa: E402
                              has_text_layer)  # 정답표 텍스트레이어 우선
import fitz  # noqa: E402
from PIL import Image  # noqa: E402


META_WORKERS = 4   # Haiku text-only is fast (~3-5s); 4 parallel is safe
CROP_WORKERS = 4   # pure-PIL crop_by_gap is CPU-bound and fast (~50ms/problem)
WEB_PUBLIC_IMAGES = ROOT / 'web' / 'public' / 'problem-images'


def _validate_crop(image_path: Path, pdf_path: Path, page_num: int,
                   anchor_y_pt: float, next_anchor_y_pt: float | None,
                   col_idx: int, dpi: int = 200) -> tuple[bool, str]:
    """Sanity-check a cropped problem PNG against the PDF text-layer.

    Pass criteria:
      - right edge: image_width_pt covers the rightmost text line's x1 in
        the column's range [anchor_y, next_anchor_y]
      - bottom edge: image_height_pt covers the last text line's y1 - anchor_y

    Returns (ok, reason). Reason is non-empty when validation fails so the
    caller can log + record in missing.json. We allow ~12pt slack for PIL
    trim and rendering rounding.
    """
    SLACK_PT = 12.0
    try:
        im = Image.open(image_path)
    except Exception as e:
        return False, f'open failed: {e}'
    pt_per_px = 72.0 / dpi
    img_w_pt = im.width * pt_per_px
    img_h_pt = im.height * pt_per_px

    try:
        d = fitz.open(pdf_path)
        lines = _collect_text_lines(d[page_num - 1])
        d.close()
    except Exception as e:
        return True, ''  # PDF read failed — skip validation

    # Lines inside this column AND vertically in this problem's range.
    end_y = next_anchor_y_pt if next_anchor_y_pt is not None else 1e9
    relevant = []
    for (lx0, ly0, lx1, ly1) in lines:
        cx = (lx0 + lx1) / 2.0
        if _column_of(cx) != col_idx:
            continue
        if ly0 < anchor_y_pt - 2 or ly0 >= end_y - 2:
            continue
        relevant.append((lx0, ly0, lx1, ly1))
    if not relevant:
        return True, ''  # figure-only or table — can't validate

    min_x_pt = min(b[0] for b in relevant)
    max_x_pt = max(b[2] for b in relevant)
    max_y_pt = max(b[3] for b in relevant)
    needed_h_pt = max_y_pt - anchor_y_pt
    # Width check accounts for PIL left-trim: the image width equals the
    # ink span, which should be max_x - min_x. Comparing raw PDF max_x
    # against trimmed image width was a false positive every time the
    # ink started at x>0 (always, on Korean exam pages).
    needed_w_pt = max_x_pt - min_x_pt
    if needed_w_pt > img_w_pt + SLACK_PT:
        return False, f'right_clip: ink width={needed_w_pt:.0f}pt > img={img_w_pt:.0f}pt'
    if needed_h_pt > img_h_pt + SLACK_PT:
        return False, f'bottom_clip: need={needed_h_pt:.0f}pt > img={img_h_pt:.0f}pt'
    return True, ''


def _ensure_web_symlink(image_path: Path) -> None:
    """Create a symlink in web/public/problem-images/ pointing at the
    canonical image under db/raw/. astro dev/build serves this URL as
    /problem-images/<basename>. Idempotent."""
    WEB_PUBLIC_IMAGES.mkdir(parents=True, exist_ok=True)
    link = WEB_PUBLIC_IMAGES / image_path.name
    if link.is_symlink() or link.exists():
        return
    try:
        # 상대경로 심링크 — worktree 절대경로가 박히면 main 머지 시 깨진다.
        import os
        link.symlink_to(os.path.relpath(image_path.resolve(), WEB_PUBLIC_IMAGES.resolve()))
    except Exception as e:
        # Fallback to copy on filesystems without symlink support
        import shutil
        try:
            shutil.copy2(image_path, link)
        except Exception as e2:
            print(f'  ! could not link {image_path.name}: {e}; copy also failed: {e2}', flush=True)


_CONCEPT_NORM_INDEX: dict | None = None
_CONCEPT_PATH_INDEX: dict | None = None


def _norm_concept(s: str) -> str:
    """언더스코어·공백 제거 + NFC. LLM이 '삼각함수의미분'으로 뽑아도 '삼각함수의_미분'에 매칭."""
    import unicodedata
    return re.sub(r'[_\s]', '', unicodedata.normalize('NFC', s or ''))


def _concept_norm_index() -> dict:
    """{정규화슬러그: 실제 basename} — 기존 개념 트리 전체(rglob 1회 캐시)."""
    global _CONCEPT_NORM_INDEX
    if _CONCEPT_NORM_INDEX is None:
        idx = {}
        for p in (ROOT / 'docs' / 'concepts').rglob('*.md'):
            idx.setdefault(_norm_concept(p.stem), p.stem)
        _CONCEPT_NORM_INDEX = idx
    return _CONCEPT_NORM_INDEX


def _concept_path_index() -> dict:
    """{정규화 상대경로: 실제 상대경로} — 확장자 없는 docs/concepts 기준 경로."""
    global _CONCEPT_PATH_INDEX
    if _CONCEPT_PATH_INDEX is None:
        base = ROOT / 'docs' / 'concepts'
        _CONCEPT_PATH_INDEX = {}
        for p in base.rglob('*.md'):
            rel = p.relative_to(base).as_posix()[:-3]
            _CONCEPT_PATH_INDEX[_norm_concept(rel)] = rel
    return _CONCEPT_PATH_INDEX


def _canonical_concept(slug: str, scope: list | None = None) -> str:
    """LLM 이 준 값을 실제 개념 **상대경로**로 정규화한다.

    ★2026-08-13 이전에는 **파일명(잎)만** 보고 매칭했다. `제곱근` 이 중3에도 수1 트리에도
      있을 수 있는데 이름만으로는 못 가른다 — rglob 순서상 **먼저 걸린 파일이 이겼다.**
      그래서 수능 지수 문제가 중3 제곱근으로 갔다.
      이제 ①경로면 경로로 맞추고 ②이름뿐이면 **스코프 안에서** 찾는다.
      스코프 안에 없으면 원본을 그대로 돌려준다(=진짜 신규로 취급).
    """
    if not slug:
        return slug
    n = _norm_concept(slug)
    hit = _concept_path_index().get(n)
    if hit:
        return hit
    # 이름만 온 경우 — 스코프(학년 디렉터리)로 좁혀서 고른다.
    leaf = slug.rsplit('/', 1)[-1]
    nleaf = _norm_concept(leaf)
    cands = [rel for k, rel in _concept_path_index().items() if rel.rsplit('/', 1)[-1] == leaf or k.endswith('/' + nleaf)]
    if scope:
        scoped = [c for c in cands if any(f'/{g}/' in f'/{c}' for g in scope)]
        # ★스코프 밖 후보는 **쓰지 않는다.** 예전엔 여기서 학년이 어긋난 개념을 그대로
        #   집어서 "수능 문제 → 중3 제곱근" 이 나왔다. 못 찾으면 원본을 남겨 게이트가 잡게 한다.
        if not scoped:
            return slug
        cands = scoped
    if len(cands) == 1:
        return cands[0]
    # 여러 개면 고르지 않는다 — 아무거나 집어서 학년을 틀리느니 원본을 남겨 눈에 띄게 한다.
    return _concept_norm_index().get(n, slug)


def _ensure_concept_exists(slug: str, parent_unit: str | None,
                            concept_type: str = 'definition') -> bool:
    """Create a placeholder docs/concepts/{slug}.md if it doesn't exist.
    Returns True if newly created. Schema matches existing concepts so
    astro content collection + the LWIP graph builder accept it without
    extra config. Body is intentionally minimal — students or the LLM
    tutor fill it in later."""
    if not slug:
        return False
    concepts_root = ROOT / 'docs' / 'concepts'
    path = concepts_root / f'{slug}.md'
    # ★★파일이 있으면 **무조건** 손대지 않는다. 이 함수는 이름이 '보장' 이지만 하는 일은
    #   write 다 — 존재 판정이 한 번만 어긋나면 그 즉시 실제 노트가 stub 으로 사라진다.
    #   2026-08-13 에 그 일이 실제로 났다(개념 186개가 4-7줄 템플릿으로 덮였다).
    #   판정 로직이 또 틀려도 **데이터는 살아남아야 한다** — 그래서 판정보다 앞에 둔다.
    if path.exists():
        return False
    # 개념트리는 중첩(docs/concepts/<도메인>/<학년>/<단원>.md). 정규화 매칭으로
    # 표기차(언더스코어 등)까지 흡수 — flat 중복 stub 양산 방지(과거 490종 사고).
    # ★경로 인덱스를 **먼저** 본다. _canonical_concept 가 전체 경로를 돌려주게 바뀌었는데
    #   잎 이름 인덱스만 보면 'a/b/유리지수' 를 "없는 개념" 으로 판정한다 — 그게 위 사고의 원인.
    if _norm_concept(slug) in _concept_path_index() or _norm_concept(slug) in _concept_norm_index():
        return False
    prereq_line = f'prerequisites: [docs/concepts/{parent_unit}.md]' if parent_unit else 'prerequisites: []'
    fm = (
        '---\n'
        'sources: []\n'
        f'created: {TODAY}\n'
        f'updated: {TODAY}\n'
        f'concept_type: {concept_type}\n'
        f'{prereq_line}\n'
        'enables: []\n'
        'mastery: unknown\n'
        '---\n\n'
        f'# {slug.replace("_", " ")}\n\n'
        '(개념 정의는 학습 시 채워집니다.)\n\n'
        '## 정의\n\n'
        '## 예시\n\n'
        '## 관련 개념\n'
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(fm, encoding='utf-8')
    _concept_norm_index().setdefault(_norm_concept(slug), slug)   # 같은 런 내 재생성 방지
    return True


def write_markdown_v2(prob: dict, meta: dict | None, answer: str | None,
                      image_url: str, image_fs: str, round_slug: str,
                      year: int, exam_type: str, session: str,
                      grade: str | None = None, agency: str = '평가원') -> Path:
    """v2: body = `<img>` only; searchable_text + metadata in frontmatter.

    Backward-compatible with the astro content collection schema — extends
    rather than replaces (adds problem_image, searchable_text, has_figure)."""
    subject = prob['subject']
    slug = f'{round_slug}_{subject}_{prob["number"]:02d}'
    # nested: docs/problems/<year>/<round_dir>/<slug>.md — 회차별 그룹핑(content collection **/*.md).
    # round_dir = round_slug 에서 연도 prefix 제거 (예: 2027_6월모평 → 6월모평, 2024_고3_3월모의고사 → 고3_3월모의고사)
    round_dir = round_slug.split('_', 1)[1] if '_' in round_slug else round_slug
    out = DOCS_PROBLEMS / str(year) / round_dir / f'{slug}.md'
    out.parent.mkdir(parents=True, exist_ok=True)

    meta = meta or {}
    pid = str(uuid.uuid4())
    unit = meta.get('unit') or ''
    concepts = meta.get('concepts') or []
    # YAML double-quoted scalar treats \X as an escape — LaTeX like $\sqrt{n}$
    # crashes the parser. Escape backslashes (and embedded double-quotes).
    intent = (meta.get('exam_intent') or '').replace('\\', '\\\\').replace('"', '\\"')
    killer = meta.get('killer_tier') or ''
    cog = meta.get('cognitive_type') or ''
    # prob['format']은 어댑터가 시험 구조상 결정한 권위 있는 값이므로 우선.
    # (v2 본체는 meta.get('format')을 prob에 넣으므로 v2 경로 동작은 동일.)
    fmt = prob.get('format') or meta.get('format') or 'numeric'
    has_fig = bool(meta.get('has_figure'))
    # YAML block scalar (|) preserves raw content — no escape needed.
    searchable = meta.get('searchable_text') or ''

    concept_paths = [f'docs/concepts/{unit}.md'] if unit else []
    for c in concepts:
        cp = f'docs/concepts/{c}.md'
        if cp not in concept_paths:
            concept_paths.append(cp)
    concepts_yaml = ', '.join(concept_paths)

    # Build frontmatter without dedent — dedent mis-aligns dynamic indented
    # blocks (e.g. grade_yaml inserts 2-space-indented line, dedent then
    # strips 2 spaces from EVERY line). Just write the YAML in column 0.
    grade_line = f'  grade: {grade}\n' if grade else ''
    searchable_block = '\n'.join('  ' + ln for ln in searchable.split('\n'))
    fm_lines = [
        '---',
        f'sources: [pdf:db/raw/{round_slug}/문제.pdf]',
        f'created: {TODAY}',
        f'updated: {TODAY}',
        'source:',
        f'  agency: {agency}',
        f'  exam_type: {exam_type}',
        f'  year: {year}',
        f'  session: {session}',
    ]
    if grade:
        fm_lines.append(f'  grade: {grade}')
    fm_lines.extend([
        f'  subject: {subject}',
        f'  number: {prob["number"]}',
        f'  score: {prob["score"]}',
        f'problem_id: {pid}',
        f'problem_image: {image_url}',
        f'has_figure: {str(has_fig).lower()}',
        f'format: {fmt}',
        'has_image: true',
        f'image_paths: [{image_fs}]',
        f'answer: "{answer or ""}"',
        'official_pass_rate: null',
        'official_solution_url: null',
        f'unit: {unit}',
        f'concepts: [{concepts_yaml}]',
        f'exam_intent: "{intent}"',
        f'killer_tier: {killer}',
        f'cognitive_type: {cog}',
        'status: unsolved',
        'review_state: new',
        f'next_review: {TODAY}',
        'searchable_text: |',
        searchable_block,
        '---',
        '',
    ])
    fm = '\n'.join(fm_lines)

    def _slugify(s: str) -> str:
        return s.strip().replace(' ', '_')
    concept_links = '\n'.join(
        f'- [{_slugify(c).replace("_", " ")}](../concepts/{_slugify(c)}.md)'
        for c in ([unit] + concepts) if c
    )
    body = (
        f'\n# [{year} {exam_type} {subject} {prob["number"]}번] {prob["score"]}점\n\n'
        f'> 출처: {agency} {year}{"년" if exam_type == "모의고사" else "학년도"} {exam_type} {session or ""} 수학영역 · 단원: {unit or "(매핑 필요)"}\n'
        f'> Tier: {killer or "?"} · cognitive: {cog or "?"}\n'
        f'> **{intent or "(intent missing)"}**\n\n'
        f'## 문제\n\n'
        f'<img src="{image_url}" alt="{year} {exam_type} {subject} {prob["number"]}번 문제" class="problem-image" />\n\n'
        f'## 풀이 (학습 시 채워짐)\n\n'
        f'본 페이지의 상세 풀이는 학습 시 직접 작성하거나, 페이지 하단 채팅창에서 LLM 튜터의 도움으로 채우세요.\n\n'
        f'## 매핑된 개념\n{concept_links}\n'
    )
    DOCS_PROBLEMS.mkdir(parents=True, exist_ok=True)
    out.write_text(fm + body, encoding='utf-8')
    return out


def _guess_score(number: int, exam_type: str, grade: str | None) -> int:
    """Heuristic when meta doesn't report score explicitly. Vision can
    extract '[X점]' but if missing this gives a reasonable default."""
    if exam_type in ('모의고사', '학력평가') and grade in ('고1', '고2'):
        if number <= 15:
            return 2 if number <= 4 else 3
        if number <= 22:
            return 4
        return 4
    # 수능/모평/고3
    if number <= 8:
        return 2 if number <= 2 else 3
    if number <= 22:
        return 4 if number >= 12 else 3
    if number <= 28:
        return 3
    return 4


def ingest_round_v2(year: int, exam_type: str, session: str,
                    pdf_url: str | None = None, ans_url: str | None = None,
                    grade: str | None = None, agency: str = '평가원',
                    single: bool = False) -> dict:
    round_slug = slugify_round(year, exam_type, session, grade)
    raw = ROOT / 'db' / 'raw' / round_slug
    label = f'{exam_type}, {session}' + (f', {grade}' if grade else '')
    t_start = time.time()
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

    # Step 1: render pages
    pages_dir = raw / 'pages'
    page_files = render_pdf_pages(prob_pdf, pages_dir)
    print(f'  ✓ {len(page_files)} pages rendered', flush=True)

    # Step 1.5: 로제타 자동 확장 — 신규 PUA 글리프(사전에 없는 것)가 있으면 비전으로 식별해 등록
    try:
        import rosetta_extend
        _added = rosetta_extend.extend(prob_pdf, log=lambda m: print('  ' + m, flush=True))
        if _added:
            print(f'  ✓ 로제타 사전 확장 {len(_added)}종', flush=True)
    except Exception as _e:
        print(f'  · rosetta_extend 건너뜀: {str(_e)[:80]}', flush=True)

    # Step 2: identify problem bboxes
    entries = extract_problem_bboxes(prob_pdf, exam_type=exam_type, grade=grade)
    if not entries:
        return {'round': round_slug, 'ok': False, 'reason': 'no problem bboxes detected'}
    print(f'  ✓ {len(entries)} problems located via PDF text-layer', flush=True)

    # 단일과목 회차 — 통합형(--single, 예: 2028 예시) + 교육청 고1/고2 학평 +
    # 검정고시. bbox는 영역 헤더가 없으면 전 문항을 '공통'으로 찍으나 '단일'이 맞다.
    # (모의고사/학력평가 고3은 공통+선택이라 제외.)
    is_single_subject = single or (
        exam_type in ('모의고사', '학력평가', '검정고시') and grade != '고3')
    if is_single_subject:
        for e in entries:
            e['subject'] = '단일'
        _tag = '통합형(--single)' if single else f'{exam_type} {grade or ""}'.strip()
        print(f'  · 전 문항 subject=단일 ({_tag})', flush=True)

    # Step 3: crop each problem PNG
    images_dir = raw / 'images'
    images_dir.mkdir(exist_ok=True)
    crop_cache = raw / 'crop_cache'
    page_png_by_num = {int(p.stem[1:]): p for p in page_files}

    # Pre-compute next-anchor lookup for validation.
    # entries are already sorted by (subject, number, page); rebuild by
    # (page, column) order so each anchor knows its next-same-column.
    same_col_anchors: dict[tuple[int, int], list[tuple[int, float]]] = {}
    for e in entries:
        key = (e['page_num'], _column_of((e['bbox_pdf'][0] + e['bbox_pdf'][2]) / 2.0))
        same_col_anchors.setdefault(key, []).append((e['number'], e['bbox_pdf'][1]))
    for key in same_col_anchors:
        same_col_anchors[key].sort(key=lambda t: t[1])

    def _next_anchor_y(page_num: int, col_idx: int, anchor_y: float) -> float | None:
        anchors = same_col_anchors.get((page_num, col_idx), [])
        for _, y in anchors:
            if y > anchor_y + 1:
                return y
        return None

    failed_crops: list[dict] = []
    crop_validations: list[dict] = []

    def _process_crop(e):
        page_png = page_png_by_num.get(e['page_num'])
        if not page_png:
            return e, 'no_page', None
        img_name = f'{round_slug}_{e["subject"]}_{e["number"]:02d}.png'
        img_path = images_dir / img_name
        e['image_path'] = img_path
        e['image_fs'] = f'db/raw/{round_slug}/images/{img_name}'
        e['image_url'] = f'/problem-images/{img_name}'
        try:
            # 1. candidate = column rect × [anchor, next anchor]
            img = Image.open(page_png)
            candidate = img.crop(e['bbox_px'])
            tmp = images_dir / f'.cand_{e["subject"]}_{e["number"]:02d}.png'
            candidate.save(tmp)
            try:
                # v3.2: gap-based 경계 + 위로 18px(위첨자 클립 방지). 페이지+bbox 직접 사용.
                ok = crop_problem(img, e['bbox_px'], img_path, exam_type=exam_type)
                if not ok:
                    # Degenerate (mostly blank candidate) — keep raw so
                    # something is at least visible.
                    candidate.save(img_path)
            finally:
                try: tmp.unlink()
                except Exception: pass
            _ensure_web_symlink(img_path)
            return e, 'ok', None
        except Exception as ex:
            return e, 'error', str(ex)[:200]

    cropped_entries: list[dict] = []
    t_crop = time.time()
    total = len(entries)
    with cf.ThreadPoolExecutor(max_workers=CROP_WORKERS) as ex:
        for entry, status, reason in ex.map(_process_crop, entries):
            if status == 'no_page':
                print(f'  ✗ crop skip #{entry["number"]:>2} {entry["subject"]:>8}  page not rendered', flush=True)
                failed_crops.append({'subject': entry['subject'], 'number': entry['number'],
                                     'reason': 'page_not_rendered'})
                continue
            if status == 'error':
                print(f'  ✗ crop fail #{entry["number"]:>2} {entry["subject"]:>8}: {reason}', flush=True)
                failed_crops.append({'subject': entry['subject'], 'number': entry['number'],
                                     'reason': f'crop_error: {reason}'})
                continue
            cropped_entries.append(entry)

    entries = cropped_entries
    if failed_crops:
        _missing_path = raw / 'missing.json'
        try:
            existing = json.loads(_missing_path.read_text(encoding='utf-8')) if _missing_path.exists() else {}
        except Exception:
            existing = {}
        existing['failed_crops'] = failed_crops
        existing['ts'] = datetime.now().isoformat(timespec='seconds')
        try:
            _missing_path.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding='utf-8')
        except Exception:
            pass
    summary_suffix = f'  ({len(failed_crops)} failed → missing.json)' if failed_crops else ''
    print(f'  ✓ {len(entries)} problem PNGs cropped ({time.time()-t_crop:.0f}s){summary_suffix}', flush=True)

    # Step 4: PDF-text + Haiku metadata (parallel, cached). The PNG is
    # already the user-facing body; this step just classifies.
    # ★스코프는 문제마다 다르므로(과목·학년·연도) 여기서 통째로 만들지 않는다.
    #   extract_metadata 가 각 문제의 과목/학년/연도로 직접 좁힌다.
    units = load_concept_index()
    meta_cache = raw / 'meta_cache'

    def _meta_one(entry):
        t0 = time.time()
        cache_key = f'{entry["subject"]}_{entry["number"]:02d}'
        m = extract_metadata(
            pdf_path=prob_pdf,
            page_num=entry['page_num'],
            bbox_pdf=entry['bbox_pdf'],
            number=entry['number'],
            subject=entry['subject'],
            units_index=units,
            cache_dir=meta_cache,
            cache_key=cache_key,
            timeout=60,
            # ★개념 매핑은 **이미지**를 근거로 한다. PDF 텍스트레이어는 지수를 근호로
            #   뭉개서(4^(2/3) → 4√3/2) 수능 문제를 중3 문제로 보이게 만든다.
            image_path=Path(entry['image_fs']) if entry.get('image_fs') else None,
            grade=grade,
            year=year,
        )
        return entry, m, time.time() - t0

    t_meta = time.time()
    done = 0
    total = len(entries)
    meta_failures: list[dict] = []
    with cf.ThreadPoolExecutor(max_workers=META_WORKERS) as ex:
        for entry, meta, dt in ex.map(_meta_one, entries):
            entry['meta'] = meta
            done += 1
            unit = (meta or {}).get('unit', '?') if isinstance(meta, dict) else '?'
            mark = '✓' if (isinstance(meta, dict) and meta.get('unit')) else '✗'
            print(f'    [meta {done:>2}/{total}] {mark} #{entry["number"]:>2} {entry["subject"]:>8} '
                  f'unit={unit} ({dt:.0f}s)', flush=True)
            if not (isinstance(meta, dict) and meta.get('unit')):
                meta_failures.append({'subject': entry['subject'], 'number': entry['number'],
                                      'reason': 'haiku_meta_fail'})
    if meta_failures:
        _missing_path = raw / 'missing.json'
        try:
            existing = json.loads(_missing_path.read_text(encoding='utf-8')) if _missing_path.exists() else {}
        except Exception:
            existing = {}
        existing['meta_failures'] = meta_failures
        existing['ts'] = datetime.now().isoformat(timespec='seconds')
        try:
            _missing_path.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding='utf-8')
        except Exception:
            pass
    print(f'  → metadata done ({time.time()-t_meta:.0f}s, fails {len(meta_failures)})', flush=True)

    # Step 5: extract answers (reuse existing pipeline — works reliably)
    if single:
        default_ans_subj = '단일'
    elif exam_type in ('모의고사', '학력평가') and grade == '고3':
        default_ans_subj = '공통'
    elif exam_type in ('모의고사', '학력평가', '검정고시'):
        default_ans_subj = '단일'
    else:
        default_ans_subj = '공통'
    work = raw / 'work'
    work.mkdir(exist_ok=True)
    if not ans_pdf.exists():
        answers = {}
    elif single:
        # 통합형 단일 30문항 — 3열 정답표 전용 파서로 전부 '단일' 버킷에.
        answers = extract_single_answers(ans_pdf)
    else:
        answers = None
        # 공통+선택(평가원 수능/모평·교육청 고3) 정답표는 텍스트레이어 좌표파싱이
        # 비전보다 정확하다 — 비전은 다중컬럼에서 선택 3과목에 같은 답을 복사하는
        # 오류가 잦다(2027_6월모평 실측: vision 10/46 → textlayer 46/46).
        if default_ans_subj == '공통' and ans_pdf.exists() and has_text_layer(ans_pdf):
            try:
                flat = parse_answer_table(ans_pdf)  # {(subject, number): answer}
                if flat and any(s != '공통' for s, _n in flat):  # 선택과목까지 잡혔는지
                    answers = {}
                    for (s, n), a in flat.items():
                        answers.setdefault(s, {})[str(n)] = a
                    print(f'  ✓ answers: textlayer 좌표파싱 ({len(flat)} entries)', flush=True)
            except Exception as e:
                print(f'  ⚠ textlayer 파싱 실패: {e} → vision 폴백', flush=True)
                answers = None
        elif default_ans_subj == '단일' and ans_pdf.exists() and has_text_layer(ans_pdf):
            # 단일과목(교육청 고1/고2 학평 등): 단답형이 HyhwpEQ 수식폰트 PUA 글리프라
            # 비전이 자주 틀린다 → 좌표/PUA 디코딩이 정확(고1·고2 2026-6월 60/60 실측).
            try:
                flat = parse_single_answer_table(ans_pdf)  # {'단일': {num: ans}}
                got = flat.get('단일', {})
                if len(got) >= max(20, int(0.7 * len(entries))):
                    answers = flat
                    print(f'  ✓ answers: textlayer PUA 디코딩 ({len(got)} entries)', flush=True)
                else:
                    print(f'  ⚠ 단일 textlayer 부족({len(got)}) → vision 폴백', flush=True)
            except Exception as e:
                print(f'  ⚠ 단일 textlayer 실패: {e} → vision 폴백', flush=True)
                answers = None
        if answers is None:
            answers = extract_answers(ans_pdf, work, default_subject=default_ans_subj,
                                      expected_count=len(entries))
    print(f'  ✓ answers: {sum(len(v) for v in answers.values())} entries', flush=True)

    # Step 6: write markdown + DB upsert
    written = []
    for entry in entries:
        subj = entry['subject']
        num = entry['number']
        ans = (answers.get(subj, {}) or {}).get(str(num))
        # Fallback for non-수능 single-subject answer tables stored under '단일'
        if ans is None and len(answers) == 1:
            only_key = next(iter(answers))
            if only_key != subj:
                ans = answers[only_key].get(str(num))
        meta = entry.get('meta') or {}
        score = _guess_score(num, exam_type, grade)
        prob_for_write = {
            'subject': subj,
            'number': num,
            'score': score,
            'format': meta.get('format', 'numeric'),
            'body': '',  # body is the PNG image, not text
            'image_paths': [entry['image_fs']],
            'searchable_text': meta.get('searchable_text', ''),
        }
        # Auto-create missing concept placeholders so the markdown links
        # don't dangle. Haiku occasionally invents spoke names not in our
        # concept tree; create a stub linked under the parent unit and
        # let later study/tutor sessions fill in the body.
        # LLM 슬러그를 기존 정규 개념으로 정규화 매칭 → md 가 정규 slug 를 참조(중복 stub 방지).
        unit_slug = meta.get('unit') if isinstance(meta, dict) else None
        if unit_slug:
            unit_slug = _canonical_concept(unit_slug)
            meta['unit'] = unit_slug
            _ensure_concept_exists(unit_slug, parent_unit=None, concept_type='unit')
        if isinstance(meta, dict) and meta.get('concepts'):
            meta['concepts'] = [_canonical_concept(s) for s in meta['concepts']]
            for spoke in meta['concepts']:
                _ensure_concept_exists(spoke, parent_unit=unit_slug, concept_type='definition')
        write_markdown_v2(prob_for_write, meta, ans,
                          entry['image_url'], entry['image_fs'],
                          round_slug, year, exam_type, session, grade=grade, agency=agency)
        written.append({'prob': prob_for_write, 'mapping': meta, 'answer': ans})
        print(f'  [{num:>2}] {subj:>8}  ans={ans!s:>4}  unit={meta.get("unit","?")}', flush=True)

    try:
        db_upsert(written, year, exam_type, session,
                  f'db/raw/{round_slug}/문제.pdf', grade=grade, agency=agency)
    except Exception as e:
        print(f'  ✗ DB upsert failed: {str(e)[:300]}', flush=True)
        raise

    elapsed = time.time() - t_start
    print(f'  ✓ DB upsert {len(written)} problems  (round took {elapsed:.0f}s = {elapsed/60:.1f}m)', flush=True)
    return {'round': round_slug, 'ok': True, 'count': len(written)}


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--year', type=int, required=True)
    ap.add_argument('--exam-type', required=True)
    ap.add_argument('--session', default=None)
    ap.add_argument('--grade', default=None)
    ap.add_argument('--agency', default='평가원')
    ap.add_argument('--single', action='store_true',
                    help='통합형(선택과목 없는 30문항) → 전 문항 subject=단일')
    ap.add_argument('--with-cache', action='store_true',
                    help='인제스트 후 풀이 캐시(blind-solve 검증)까지 자동 체이닝')
    ap.add_argument('--no-sync', action='store_true',
                    help='후처리 동기화(post_ingest_sync) 생략 — orchestrate가 일괄 처리할 때')
    args = ap.parse_args()
    result = ingest_round_v2(args.year, args.exam_type, args.session,
                              grade=args.grade, agency=args.agency, single=args.single)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # ── 자동 체이닝 ──────────────────────────────────────────────────────
    # 인제스트 성공 시: (옵션)풀이 캐시 먼저(md에 solution 추가) → 후처리 동기화(개념 역인덱스·그래프·허브
    # 재생성 + dev 콘텐츠 리프레시). 같은 프로세스/로그라 /progress 가 각 패널 표시.
    if result.get('ok'):
        import subprocess, sys, os
        round_slug = result['round']
        round_dir = round_slug.split('_', 1)[1] if '_' in round_slug else round_slug
        md_dir = DOCS_PROBLEMS / str(args.year) / round_dir
        slugs = sorted(p.stem for p in md_dir.glob('*.md'))
        # 텍스트 품질·정합성 게이트 (캐시/동기화 전 — ganah/gyo12 와 동일). PUA 손상 searchable_text
        # 자동 재전사 + format 오분류 교정. 캐시 전에 끝내야 손상 텍스트로 솔버를 만들지 않는다.
        # (손상 *탐지된* 문제만 vision 재전사 → 비용은 손상분에 한정)
        if slugs:
            print(f'\n══════ 체이닝 0/2: 텍스트 품질·정합성 게이트 {len(slugs)}문제 ══════', flush=True)
            subprocess.run([sys.executable, str(ROOT / 'scripts' / 'text_quality_gate.py'),
                            '--list', ','.join(slugs)])
            subprocess.run([sys.executable, str(ROOT / 'scripts' / 'consistency_gate.py'),
                            '--list', ','.join(slugs), '--fix'])
        if args.with_cache:
            print(f'\n══════ 체이닝 1/2: 풀이 캐시 {len(slugs)}문제 ══════', flush=True)
            subprocess.run([sys.executable, str(ROOT / 'scripts' / 'build_solution_cache.py'),
                            '--list', ','.join(slugs), '--parallel', '10'])   # 킬러-먼저는 build_solution_cache가 정렬
        # 동기화는 항상(--no-sync 아니면): 새 문제가 /problems·/concepts 에 안 보이는 것 방지
        if not args.no_sync:
            print('\n══════ 체이닝 2/2: 후처리 동기화 (개념 역인덱스·그래프 + dev 리프레시) ══════', flush=True)
            subprocess.run([sys.executable, str(ROOT / 'scripts' / 'post_ingest_sync.py')],
                           env={**os.environ, 'MATHSTUDY_ROOT': str(ROOT)})
        print('\n✓ 체이닝 완료', flush=True)
