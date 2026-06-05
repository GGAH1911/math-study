#!/usr/bin/env python3
"""오염 결정 테스트 — 같은 문제를 (A)실명 경로 vs (B)익명 경로로 answer-only 풀이, 정답률 비교.
파일명(stem=연도·시험·번호)이 단서면 실명>익명. 같으면 이미지로만 푼 것=오염 없음.
유명 기출(수능·평가원) 위주(암기 가능성 ↑). 환경: AB_MODEL(haiku), AB_N(10), AB_TO(120)."""
import re, glob, json, os, subprocess, random, shutil, sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parent.parent
IMGDIR = ROOT / 'web' / 'public' / 'problem-images'
sys.path.insert(0, str(ROOT / 'scripts'))
from tiling import tile_for_vision  # noqa: E402

MODEL = os.environ.get('AB_MODEL', 'haiku')
N = int(os.environ.get('AB_N', '10'))
TO = int(os.environ.get('AB_TO', '120'))
random.seed(7)
SYS = "당신은 한국 수능 수학 문제를 정확히 푸는 전문가입니다. 첨부 이미지를 Read로 본 뒤 풉니다. 추측 금지."
ANON = Path('/tmp/ab_anon')
ANON.mkdir(exist_ok=True)


def meta(t):
    g = lambda k: (m.group(1).strip().strip('\'"') if (m := re.search(rf'^\s*{k}:\s*(.+?)\s*$', t, re.M)) else None)
    return dict(exam=g('exam_type'), ans=g('answer'), fmt=g('format'))


def prompt(tiles, fmt):
    ft = '객관식 5지선다' if fmt == 'choice' else '단답형(정수)'
    listing = '\n'.join(f'    {i + 1}. {p}' for i, p in enumerate(tiles))
    return (f"문제 이미지:\n{listing}\n문항 형식: {ft}\n\n위 이미지를 Read로 연 뒤 끝까지 풀어라. "
            f'풀이·설명 없이 마지막에 오직 ```json\n{{"answer": <정수>}}\n``` 만.')


def solve(tiles, fmt):
    args = ['claude', '-p', '--model', MODEL, '--effort', 'low', '--allowedTools', 'Read',
            '--add-dir', str(Path(tiles[0]).parent), '--disallowedTools', 'Bash,Edit,Write,Glob,Grep,WebFetch,WebSearch',
            '--max-turns', '10', '--system-prompt', SYS, '--output-format', 'json', '--', prompt(tiles, fmt)]
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=TO)
        env = json.loads(r.stdout)
    except Exception:
        return None, 0.0
    cost = env.get('total_cost_usd', 0) or 0.0
    txt = env.get('result', '') or ''
    for b in reversed(re.findall(r'```json\s*(.*?)```', txt, re.DOTALL)):
        try:
            return str(json.loads(b).get('answer')).strip(), cost
        except Exception:
            pass
    return None, cost


def anon_tiles(stem, real_tiles):
    d = ANON / f'{abs(hash(stem)) % 10**8}'
    d.mkdir(exist_ok=True)
    out = []
    for i, t in enumerate(real_tiles):
        o = d / f'p_{i + 1}.png'
        shutil.copy(t, o)
        out.append(str(o))
    return out


def run(item):
    path, stem, m = item
    img = IMGDIR / (stem + '.png')
    if not img.exists():
        return None
    real = [str(t) for t in tile_for_vision(img.resolve())]
    ansA, cA = solve(real, m['fmt'])                       # 실명 경로 (현 파이프라인)
    ansB, cB = solve(anon_tiles(stem, real), m['fmt'])     # 익명 경로
    g = m['ans']
    return dict(stem=stem, gold=g, ansA=ansA, ansB=ansB, okA=(ansA == g), okB=(ansB == g), cost=cA + cB)


def main():
    fam = []
    for f in glob.glob(str(ROOT / 'docs' / 'problems' / '**' / '*.md'), recursive=True):
        if 'README' in f:
            continue
        m = meta(Path(f).read_text(encoding='utf-8'))
        if m['exam'] in ('수능', '모평') and m['ans']:        # 유명 기출
            fam.append((Path(f), Path(f).stem, m))
    random.shuffle(fam)
    tg = fam[:N]
    print(f"═══ 오염 A/B (실명 vs 익명 경로, {MODEL}) — 유명기출 {len(tg)} ═══\n", flush=True)
    res, tot = [], 0.0
    with ThreadPoolExecutor(max_workers=3) as ex:
        for fut in as_completed({ex.submit(run, it): it for it in tg}):
            r = fut.result()
            if not r:
                continue
            res.append(r); tot += r['cost']
            print(f"  {r['stem']:32s} 정답 {str(r['gold']):>4} | 실명 {str(r['ansA']):>4}{'✓' if r['okA'] else '✗'}"
                  f" · 익명 {str(r['ansB']):>4}{'✓' if r['okB'] else '✗'}", flush=True)
    A = sum(r['okA'] for r in res); B = sum(r['okB'] for r in res)
    print(f"\n═══ 결과 ═══ ${tot:.2f}", flush=True)
    print(f"  실명 경로 정답 {A}/{len(res)} · 익명 경로 정답 {B}/{len(res)}", flush=True)
    print(f"  ⇒ 실명>익명 = 파일명(정체)을 단서로 씀=오염.  실명≈익명 = 이미지로만 푼 것=오염 없음.", flush=True)


if __name__ == '__main__':
    main()
