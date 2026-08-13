#!/usr/bin/env python3
"""개념 매핑 A/B — 고친 파이프라인에서 haiku 가 충분한지 실측한다.

★왜 필요한가: 2026-08-13 에 매핑 사고의 원인 3건(죽은 ROOT·비재귀 glob·이름만으로 식별)을
  고쳤다. 원인은 하네스였지 모델이 아니었다 — 같은 haiku 호출이 만든 exam_intent 는 41건 중
  22건에서 고교 개념을 정확히 지목했다. 하지만 고친 뒤의 과제는 성격이 다르다:
  **1,565개 중에서 고르는 변별**이다. 그건 재봐야 안다. 5,198개 참조를 재매핑하기 전에
  모델을 정하는 게 순서다 — 틀린 모델로 전수를 돌리면 두 번 일한다.

★심판은 **원본 문제 이미지**를 본다. DB 전사본을 기준으로 삼으면 오늘 이미 밟은 함정
  (기준 오염)을 그대로 반복한다. 전사가 틀리면 채점도 같이 틀린다.

★비용: 전부 claude 구독(claude -p). 유료 포털은 쓰지 않는다.

사용: python3 scripts/ab_concept_mapping.py [--n 16] [--models haiku,sonnet]
"""
from __future__ import annotations
import argparse, glob, json, os, random, re, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts' / 'ingest_kice'))

import types
for _m in ('psycopg', 'fitz', 'psycopg.rows'):          # DB·PDF 는 이 측정에 불필요
    sys.modules.setdefault(_m, types.ModuleType(_m))
sys.modules['psycopg'].rows = sys.modules['psycopg.rows']
sys.modules['psycopg.rows'].dict_row = None

from ingest_round import load_concept_index, scope_for, unit_menu    # noqa: E402
from run_stage1 import map_problem, _CLAUDE_ENV, _CLEAN_DIR            # noqa: E402


def problem_meta(path: Path) -> dict:
    t = path.read_text(encoding='utf-8')
    g = lambda p, d='': (re.search(p, t, re.M).group(1).strip() if re.search(p, t, re.M) else d)  # noqa: E731
    body = t.split('## 문제', 1)[-1]
    return {
        'path': str(path.relative_to(ROOT)),
        'slug': path.stem,
        'subject': g(r'^  subject: (.+)$'),
        'grade': g(r'^  grade: (.+)$'),
        'number': g(r'^  number: (\d+)$', '0'),
        'score': g(r'^  score: (\d+)$', '3'),
        'image': g(r'^problem_image: (.+)$'),
        'current': g(r'^concepts: \[(.*?)\]$'),
        'intent': g(r'^exam_intent: "?(.*?)"?$'),
        'body': re.sub(r'\n{3,}', '\n\n', body)[:2500],
    }


JUDGE_SYSTEM = (
    '너는 한국 수능 수학 교육과정 전문가다. 문제 이미지를 직접 읽고, 두 개의 개념 매핑 후보 중 '
    '어느 쪽이 교육과정상 맞는지 판정한다. 관대하게 굴지 마라 — 학년이 어긋나면 틀린 것이다. '
    'JSON 만 출력한다.'
)


def judge(meta: dict, a: dict, b: dict, menu: str) -> dict | None:
    img = ROOT / 'web' / 'public' / meta['image'].lstrip('/')
    prompt = f"""아래 이미지를 Read 로 열어 문제를 직접 읽어라: {img}

이 문제는 {meta['subject']} 영역 {meta['number']}번({meta['score']}점)이다.

후보 A
  단원: {a.get('unit')}
  개념: {', '.join(a.get('concepts') or []) or '(없음)'}

후보 B
  단원: {b.get('unit')}
  개념: {', '.join(b.get('concepts') or []) or '(없음)'}

선택 가능한 단원 목록(참고):
{menu}

각 후보를 채점하라.
- unit_ok: 단원이 이 문제에 맞는가(학년 포함)
- concept_score: 개념 1-3개가 문제의 핵심을 짚었는가 0-5점
JSON: {{"A":{{"unit_ok":true|false,"concept_score":0-5,"why":"한 줄"}},
        "B":{{"unit_ok":true|false,"concept_score":0-5,"why":"한 줄"}},
        "winner":"A"|"B"|"tie"}}"""
    # ★심판은 이미지를 **직접 읽어야** 한다 → Read 툴 허용. run_stage1.claude_p 는
    #   allowedTools 를 안 넘겨서 여기서 따로 호출한다.
    args = ['claude', '-p', '--model', 'opus', '--max-turns', '8',
            '--output-format', 'text', '--no-session-persistence',
            '--allowedTools', 'Read',
            '--add-dir', str(ROOT / 'web' / 'public' / 'problem-images'),
            '--system-prompt', JUDGE_SYSTEM, prompt]
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=420,
                           cwd=_CLEAN_DIR, env=_CLAUDE_ENV, stdin=subprocess.DEVNULL)
        out = r.stdout.strip() if r.returncode == 0 else None
        if not out:
            print(f'    ! 심판 실패 rc={r.returncode} {r.stderr[:160]!r}', flush=True)
    except subprocess.TimeoutExpired:
        print('    ! 심판 타임아웃', flush=True)
        out = None
    if not out:
        return None
    m = re.search(r'\{.*\}', out, re.S)
    try:
        return json.loads(m.group(0)) if m else None
    except Exception:
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=16)
    ap.add_argument('--models', default='haiku,sonnet')
    ap.add_argument('--seed', type=int, default=17)
    ap.add_argument('--out', default='/tmp/ab_concept_mapping.json')
    args = ap.parse_args()
    models = args.models.split(',')
    random.seed(args.seed)

    # 표본: 절반은 **이번에 틀린 것으로 확인된** 중학-전용 매핑, 절반은 무작위.
    # 한쪽만 보면 "고치면 좋아진다" 는 당연한 결론만 나온다 — 멀쩡한 것을 망치지 않는지도 봐야 한다.
    mis, fine = [], []
    for f in glob.glob(str(ROOT / 'docs/problems/**/*.md'), recursive=True):
        t = Path(f).read_text(encoding='utf-8')[:6000]
        m = re.search(r'^concepts: \[(.*?)\]', t, re.M)
        if not m or not m.group(1).strip():
            continue
        if not any(k in f for k in ('수능', '고3', '모평')):
            continue
        refs = [r.strip() for r in m.group(1).split(',') if r.strip()]
        (mis if all(re.search(r'/(middle-[123])/', r) for r in refs) else fine).append(Path(f))
    half = args.n // 2
    sample = random.sample(mis, min(half, len(mis))) + random.sample(fine, args.n - min(half, len(mis)))
    print(f'표본 {len(sample)}건 (기존 오매핑 {min(half,len(mis))} + 정상 {args.n-min(half,len(mis))})', flush=True)

    results = []
    for i, p in enumerate(sample, 1):
        meta = problem_meta(p)
        scope = scope_for(meta['subject'], meta['grade'])
        index = load_concept_index(scope)
        if not index:
            print(f'[{i}] {meta["slug"]}: 스코프 후보 없음 — 건너뜀', flush=True)
            continue
        props = {}
        for mdl in models:
            t0 = time.time()
            # ★비전 직독 — 마크다운 본문에는 문제 텍스트가 없고(<img> 뿐), DB 전사본은
            #   첨자가 뭉개져 있다. 이미지가 유일한 기준이다(심판과 같은 근거로 맞춘다).
            img = ROOT / 'web' / 'public' / meta['image'].lstrip('/')
            r = map_problem(meta['body'], int(meta['number'] or 0), int(meta['score'] or 3),
                            index, subject=meta['subject'], grade=meta['grade'], model=mdl,
                            image=img if img.exists() else None)
            props[mdl] = {'unit': (r or {}).get('unit'), 'concepts': (r or {}).get('concepts') or [],
                          'sec': round(time.time() - t0, 1)}
            print(f'[{i}] {meta["slug"]} {mdl}: {props[mdl]["unit"]} '
                  f'({len(props[mdl]["concepts"])}개, {props[mdl]["sec"]}s)', flush=True)
        # 라벨을 섞어 심판이 모델을 모르게 한다.
        order = models[:] if random.random() < 0.5 else models[::-1]
        v = judge(meta, props[order[0]], props[order[1]], unit_menu(index))
        results.append({'slug': meta['slug'], 'subject': meta['subject'], 'was_mis': p in mis,
                        'current': meta['current'], 'props': props,
                        'order': order, 'judge': v})
        Path(args.out).write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding='utf-8')
        if v:
            print(f'    심판: A={v["A"]["unit_ok"]}/{v["A"]["concept_score"]} '
                  f'B={v["B"]["unit_ok"]}/{v["B"]["concept_score"]} → {v["winner"]} '
                  f'(A={order[0]}, B={order[1]})', flush=True)

    # 집계
    agg = {m: {'unit_ok': 0, 'score': 0, 'n': 0, 'sec': 0.0} for m in models}
    wins = {m: 0 for m in models}; ties = 0
    for r in results:
        if not r['judge']:
            continue
        for slot, mdl in zip(('A', 'B'), r['order']):
            j = r['judge'][slot]
            agg[mdl]['unit_ok'] += 1 if j['unit_ok'] else 0
            agg[mdl]['score'] += j['concept_score']
            agg[mdl]['n'] += 1
            agg[mdl]['sec'] += r['props'][mdl]['sec']
        w = r['judge']['winner']
        if w == 'tie':
            ties += 1
        else:
            wins[r['order'][0 if w == 'A' else 1]] += 1
    print('\n=== 집계 ===', flush=True)
    for m in models:
        a = agg[m]
        if not a['n']:
            continue
        print(f"  {m:8s} 단원정확 {a['unit_ok']}/{a['n']} ({a['unit_ok']/a['n']*100:.0f}%) · "
              f"개념점수 {a['score']/a['n']:.2f}/5 · 평균 {a['sec']/a['n']:.1f}s · 승 {wins[m]}", flush=True)
    print(f'  무승부 {ties}', flush=True)
    print(f'\n결과 저장: {args.out}', flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
