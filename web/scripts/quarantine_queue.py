#!/usr/bin/env python3
# quarantine_queue.py — 격리(corrector_quarantine: true) 문제를 오케스트레이터(opus)가 직접 손교정하기 위한 큐 뷰.
#   각 문제의 slug·타일이미지경로·격리사유·현재 searchable_text 를 출력. opus 가 이미지 보고 정확히 교정.
import re, glob, os, sys, json
REPO = __import__('os').environ.get('MATHSTUDY_ROOT') or __import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__))))  # ★레포 위치 자동(이동 내성)

def tile_path(round_, subj, num):
    # LLM 이미지 소비는 타일만 — tile_for_vision 우선, 없으면 images 통이미지(작은 문제는 동일).
    for base in (f'{REPO}/db/raw/{round_}/tile_for_vision', f'{REPO}/db/raw/{round_}/images'):
        for n in (f'{round_}_{subj}_{int(num):02d}', f'{round_}_{subj}_{num}'):
            p = f'{base}/{n}.png'
            if os.path.exists(p):
                return p
    return None

def main():
    qlog = {}
    qf = '/tmp/ingest_logs/corrector_quarantine.log'
    if os.path.exists(qf):
        for line in open(qf, encoding='utf-8'):
            parts = line.split('\t')
            if parts: qlog[parts[0]] = line.strip()
    out = []
    for md in sorted(glob.glob(f'{REPO}/docs/problems/**/*.md', recursive=True)):
        t = open(md, encoding='utf-8').read()
        is_quar = bool(re.search(r'^corrector_quarantine:\s*true', t, re.M))
        iss = re.search(r'\ncorrector_verify_issues:\n((?:  - .*\n?)+)', t)   # MAXATT 상한(격리 안 됨, issues 잔존)도 포함
        if not (is_quar or iss): continue
        slug = os.path.basename(md)[:-3]
        m = re.match(r'^(.+)_([가-힣A-Za-z]+)_(\d+)$', slug)
        if not m: continue
        round_, subj, num = m.group(1), m.group(2), m.group(3)
        st = re.search(r'\nsearchable_text: \|\n((?:  .*\n?)*)', t)
        out.append({
            'slug': slug, 'md': md, 'tile': tile_path(round_, subj, num),
            'kind': '격리' if is_quar else 'MAXATT상한',
            'reason': qlog.get(slug, '(사유 미기록)') if is_quar else (iss.group(1).strip() if iss else ''),
            'searchable_text': (st.group(1) if st else '').rstrip(),
        })
    if '--json' in sys.argv:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        nq = sum(1 for o in out if o['kind'] == '격리'); nm = len(out) - nq
        print(f'큐: {len(out)}건 (격리 {nq} · MAXATT상한 {nm})')
        for o in out:
            print(f"\n■ {o['slug']} [{o['kind']}]\n  타일: {o['tile']}\n  사유: {o['reason'][:160]}")

if __name__ == '__main__':
    main()
