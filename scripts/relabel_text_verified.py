#!/usr/bin/env python3
"""재라벨 백필 — escalated 문제(solved_by≠haiku)를 text-Haiku로 검증, 통과하면
기존 풀이는 **보존**하고 solved_by=haiku + text_ok:true 만 마킹.
효과: (1) 난이도 정화(vision 누명 제거), (2) 튜터 텍스트 게이트 활성.
검증 기준 = build의 text-first와 동일: ans==gold (+ 객관식은 역대입 검증기).
멱등: text_ok 있으면 skip. 환경: RL_LIMIT(0=전체), RL_WORKERS(5)."""
from __future__ import annotations
import re, glob, os, sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import build_solution_cache as B  # noqa: E402  (call_model_text, run_verifier, extract_searchable 재사용)

LIMIT = int(os.environ.get('RL_LIMIT', '0'))
WORKERS = int(os.environ.get('RL_WORKERS', '5'))


def meta(t):
    g = lambda k: (m.group(1).strip().strip('\'"') if (m := re.search(rf'^\s*{k}:\s*(.+?)\s*$', t, re.M)) else None)
    return dict(ans=g('answer'), fmt=g('format'), sb=g('solved_by'))


def targets():
    out = []
    for f in glob.glob(str(ROOT / 'docs' / 'problems' / '**' / '*.md'), recursive=True):
        if 'README' in f:
            continue
        t = Path(f).read_text(encoding='utf-8')
        if not re.search(r'^solution:', t, re.M):
            continue
        if re.search(r'^\s*text_ok:\s*true', t, re.M):      # 멱등
            continue
        m = meta(t)
        if m['sb'] not in ('sonnet', 'opus'):               # 이미지로 escalate된 것만
            continue
        st = B.extract_searchable(t)
        if not m['ans'] or len(st) < 40:
            continue
        if m['fmt'] == 'choice' and '①' not in st:          # 보기 없으면 제외
            continue
        out.append((Path(f), m, st))
    return out


def relabel(item):
    p, m, st = item
    metastr = f"문항 형식: {'객관식 5지선다' if m['fmt'] == 'choice' else '단답형(정수 정답)'}"
    sol = B.call_model_text(st, m['fmt'], metastr, 'haiku', 'high')
    if not sol or str(sol.get('answer')).strip().strip('\'"') != m['ans']:
        return dict(stem=p.stem, ok=False, was=m['sb'])
    if m['fmt'] == 'choice':                                 # 객관식은 역대입 검증기까지(우연 1/5 차단)
        okv, _ = B.run_verifier(sol.get('verifier_python', ''))
        if not okv:
            return dict(stem=p.stem, ok=False, was=m['sb'])
    # 마킹: solved_by → haiku + text_ok: true (기존 풀이/generated_by/steps/verifier 전부 보존)
    t = p.read_text(encoding='utf-8')

    def repl(mm):
        ind = mm.group(1)
        return f"{ind}solved_by: haiku\n{ind}text_ok: true"
    t2, n = re.subn(r'^(\s*)solved_by:\s*\w+\s*$', repl, t, count=1, flags=re.M)
    if n != 1 or 'text_ok: true' not in t2:
        return dict(stem=p.stem, ok=False, was=m['sb'], err='no-anchor')
    p.write_text(t2, encoding='utf-8')
    return dict(stem=p.stem, ok=True, was=m['sb'])


def main():
    tg = targets()
    if LIMIT:
        tg = tg[:LIMIT]
    print(f"═══ 재라벨 백필 (escalated → text-Haiku 검증 → solved_by=haiku + text_ok) — {len(tg)}개 ═══", flush=True)
    print(f"  (기존 풀이·generated_by·steps 전부 보존. 검증 실패분은 그대로 유지 = 진짜 난이도/도형)\n", flush=True)
    res = []
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for fut in as_completed({ex.submit(relabel, it): it for it in tg}):
            r = fut.result(); res.append(r)
            mark = f"✅ 재라벨 ({r['was']}→haiku)" if r['ok'] else '· 유지(text 미검증)'
            print(f"  [{len(res)}/{len(tg)}] {r['stem']:34s} {mark}", flush=True)
    ok = sum(r['ok'] for r in res)
    from collections import Counter
    by = Counter(r['was'] for r in res if r['ok'])
    print(f"\n═══ 완료 ═══ {ok}/{len(res)} 재라벨  ({dict(by)})", flush=True)
    print(f"  → {ok}개: solved_by=haiku + text_ok(튜터 텍스트 게이트 활성) · 나머지 {len(res)-ok}개: 그대로(진짜 난이도)", flush=True)


if __name__ == '__main__':
    main()
