#!/usr/bin/env python3
# concept_remap.py — '교정된 searchable_text' 로 개념 매핑을 다시 한다.
#   설계 이유: 어댑터 매핑은 추출 중(=교정 前, PUA 깨진 원문)으로 unit/concepts 를 뽑는다.
#   교정이 텍스트를 고친 뒤 여기서 다시 매핑하면 '교정된 깨끗한 텍스트' 기반이라 더 정확하다.
#   (box_backfill 과 같은 '교정 후 결정적 후처리' 단계. 단 여기는 LLM=haiku 매핑.)
#
#   · run_stage1.map_problem(haiku·claude_p clean cwd 캐시) 재사용 → unit/concepts/intent/tier/cognitive
#   · IV._canonical_concept + _ensure_concept_exists 로 그래프 정합(중복 stub·고아 방지) — 어댑터와 동일 경로
#   · frontmatter(unit·concepts·exam_intent·killer_tier·cognitive_type) + 본문 '## 매핑된 개념' 만 갱신,
#     searchable_text·도식·정답 등 나머지는 보존
#   · 대상=corrector_done. 라운드 슬러그 필터(예: 2019_수능). LLM 매핑은 병렬, 그래프 쓰기는 순차(레이스 방지)
#   사용: .venv/bin/python -u scripts/ingest_kice/concept_remap.py [라운드슬러그]
import sys, re, os, glob, time
import concurrent.futures as cf
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ingest_v2 as IV               # noqa: E402
from run_stage1 import map_problem   # noqa: E402

REPO = str(IV.ROOT)
UNITS = IV.load_concept_index()


def _esc_yaml(s):                    # YAML double-quoted scalar: \\ 와 " escape (LaTeX 백슬래시 대응)
    return (s or '').replace('\\', '\\\\').replace('"', '\\"')


def _slug(s):
    return s.strip().replace(' ', '_')


def _read_body(txt):
    m = re.search(r'\nsearchable_text: \|\n((?:  .*\n?)*)', txt)
    if not m:
        return None
    return '\n'.join(l[2:] if l.startswith('  ') else l for l in m.group(1).splitlines()).strip()


def do_map(md):
    """병렬 단계: 교정된 본문으로 map_problem 호출(그래프 쓰기 없음)."""
    txt = open(md, encoding='utf-8').read()
    if 'corrector_done: true' not in txt:
        return (md, 'skip-uncorrected', None)
    body = _read_body(txt)
    if not body or len(body) < 10:
        return (md, 'no-searchable', None)
    base = os.path.basename(md)[:-3]
    nm = re.search(r'_(\d+)$', base)
    number = int(nm.group(1)) if nm else 0
    sc = re.search(r'\[(\d)\s*점\]', body)
    score = int(sc.group(1)) if sc else 4
    try:
        meta = map_problem(body, number, score, UNITS)
    except Exception as e:
        return (md, 'exc', repr(e)[:80])
    if not (isinstance(meta, dict) and meta.get('unit')):
        return (md, 'map-fail', None)
    return (md, 'mapped', meta)


def apply_map(md, meta):
    """순차 단계: 정규화 + 개념 보장(그래프 쓰기) + frontmatter/본문 갱신."""
    us = IV._canonical_concept(meta['unit'])
    if not us:
        return 'map-fail', None
    IV._ensure_concept_exists(us, parent_unit=None, concept_type='unit')
    concepts = []
    for c in (meta.get('concepts') or []):
        cc = IV._canonical_concept(c)
        if cc and cc != us and cc not in concepts:
            concepts.append(cc)
            IV._ensure_concept_exists(cc, parent_unit=us, concept_type='definition')
    txt = open(md, encoding='utf-8').read()
    orig = txt
    paths = list(dict.fromkeys([f'docs/concepts/{us}.md'] + [f'docs/concepts/{c}.md' for c in concepts]))
    txt = re.sub(r'(?m)^unit: .*$', f'unit: {us}', txt, count=1)
    # ★키가 아예 없는 파일이 있다(인제스트가 반쪽으로 끝난 흔적). sub 만 쓰면 조용히 아무것도
    #   안 하고 지나가므로, 없으면 unit 줄 뒤에 만들어 넣는다.
    # ★concepts 는 세 형태가 있다: `concepts: [a, b]` · `concepts:` + 블록 리스트 · 키 없음.
    #   한 형태만 가정하면 나머지에서 **중복 줄이 생겨 YAML 이 깨진다**(2026-08-14 사이트 정지 2회).
    #   그래서 어떤 형태든 **기존 블록을 통째로 걷어내고** 새 줄을 넣는다.
    new_line = 'concepts: [' + ', '.join(paths) + ']'
    lines, out, i, replaced = txt.split('\n'), [], 0, False
    while i < len(lines):
        if lines[i].startswith('concepts:'):
            i += 1
            while i < len(lines) and lines[i].startswith('  - '):   # 블록 리스트 본체
                i += 1
            if not replaced:
                out.append(new_line); replaced = True
            continue
        out.append(lines[i]); i += 1
    txt = '\n'.join(out)
    if not replaced:            # 키가 아예 없던 파일 — unit 줄 뒤에 만든다
        txt = re.sub(r'(?m)^(unit: .*)$', r'\1\n' + new_line, txt, count=1)
    if meta.get('exam_intent'):
        txt = re.sub(r'(?m)^exam_intent: ".*?"$', f'exam_intent: "{_esc_yaml(meta["exam_intent"])}"', txt, count=1)
    if meta.get('killer_tier'):
        txt = re.sub(r'(?m)^killer_tier: .*$', f'killer_tier: {meta["killer_tier"]}', txt, count=1)
    if meta.get('cognitive_type'):
        txt = re.sub(r'(?m)^cognitive_type: .*$', f'cognitive_type: {meta["cognitive_type"]}', txt, count=1)
    # 링크 주소는 **전체 상대경로**(학년이 들어 있어야 렌더러가 올바로 해석한다), 라벨은 **잎 이름**.
    # 라벨에 전체 경로를 쓰면 "algebra math 1 지수와 로그 …" 처럼 읽을 수 없는 글자가 된다.
    links = '\n'.join(
        f'- [{_slug(c).rsplit("/", 1)[-1].replace("_", " ")}](../concepts/{_slug(c)}.md)'
        for c in ([us] + concepts))
    txt = re.sub(r'(?ms)^## 매핑된 개념\n(?:- .*\n)*', f'## 매핑된 개념\n{links}\n', txt, count=1)
    if txt != orig:
        open(md, 'w', encoding='utf-8').write(txt)
    return 'OK', f'{us} + {len(concepts)}'


def main():
    flt = sys.argv[1] if len(sys.argv) > 1 else None
    files = sorted(glob.glob(f'{REPO}/docs/problems/**/*.md', recursive=True))
    if flt:
        files = [f for f in files if flt in os.path.basename(f)]
    print(f'══ concept_remap 시작 {time.strftime("%F %T")} · {len(files)} md{f" (필터 {flt})" if flt else ""} · 대상=corrector_done · 교정후 재매핑(haiku·캐시)', flush=True)
    stat = Counter(); t0 = time.time()
    # 1) LLM 매핑(병렬) — 그래프 쓰기 없음(레이스 방지)
    with cf.ThreadPoolExecutor(max_workers=int(os.environ.get('REMAP_WORKERS', '6'))) as ex:
        mapped = list(ex.map(do_map, files))
    # 2) 정규화 + 개념보장 + 갱신(순차)
    for md, status, meta in mapped:
        if status != 'mapped':
            stat[status] += 1
            if status in ('map-fail', 'exc'):
                print(f'  ⚠ {os.path.basename(md)[:-3]} → {status}{": " + meta if isinstance(meta, str) else ""}', flush=True)
            continue
        try:
            res, detail = apply_map(md, meta)
        except Exception as e:
            res, detail = 'exc', repr(e)[:80]
        stat[res] += 1
        if res == 'OK':
            print(f'  ✅ {os.path.basename(md)[:-3]} → {detail}', flush=True)
        else:
            print(f'  ⚠ {os.path.basename(md)[:-3]} → {res}: {detail}', flush=True)
    print(f'══ 완료 {time.time()-t0:.0f}s · {dict(stat)} ══', flush=True)


if __name__ == '__main__':
    main()
