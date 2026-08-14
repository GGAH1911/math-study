#!/usr/bin/env python3
"""PoC 재설계 (공정) — 단일샷 pass@K vs 도구-에이전트 pass@K + 도구사용 실측.
이전 결함 수정: (1) B를 n=1 → pass@K, (2) raw 미저장 → stream-json으로 Bash(sympy) 호출 카운트+저장.
도구를 실제로 안 쓰면(Haiku가 무시) 그것도 결론에 반영. 환경: POC2_STEM, POC2_K(8)."""
from __future__ import annotations
import re, json, os, subprocess, sys, shutil, tempfile, glob
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parent.parent
IMGDIR = ROOT / 'web' / 'public' / 'problem-images'
VENV_PY = __import__('os').environ.get('MS_PY', __import__('os').path.expanduser('~/.venvs/ms-ingest/bin/python'))  # ★인제스트 venv(레포 .venv 는 빈 마운트포인트)
RAWDIR = Path('/tmp/ingest_logs/poc2_raw'); RAWDIR.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(ROOT / 'scripts'))
from tiling import tile_for_vision  # noqa: E402

K = int(os.environ.get('POC2_K', '8'))
STEM = os.environ.get('POC2_STEM', '2022_수능_미적분_23')


def find_meta(stem):
    for f in glob.glob(str(ROOT / 'docs' / 'problems' / '**' / (stem + '.md')), recursive=True):
        t = Path(f).read_text(encoding='utf-8')
        g = lambda k: (m.group(1).strip().strip('\'"') if (m := re.search(rf'^\s*{k}:\s*(.+?)\s*$', t, re.M)) else None)
        return g('answer'), g('format')
    return None, None


def anon(stem):
    tiles = tile_for_vision((IMGDIR / (stem + '.png')).resolve())
    d = tempfile.mkdtemp(prefix='poc2_'); out = []
    for i, t in enumerate(tiles):
        o = Path(d) / f'p_{i + 1}.png'; shutil.copy(t, o); out.append(str(o))
    return out, d


def listing(tiles):
    return '\n'.join(f'    {i + 1}. {p}' for i, p in enumerate(tiles))


def ans_of(txt):
    for b in reversed(re.findall(r'```json\s*(.*?)```', txt, re.DOTALL)):
        try:
            return str(json.loads(b).get('answer')).strip()
        except Exception:
            pass
    return None


def single(prompt, d):
    args = ['claude', '-p', '--model', 'haiku', '--effort', 'high', '--allowedTools', 'Read',
            '--add-dir', d, '--max-turns', '12', '--output-format', 'json', '--', prompt]
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=180)
        env = json.loads(r.stdout)
    except Exception:
        return None, 0.0
    return ans_of(env.get('result', '') or ''), env.get('total_cost_usd', 0) or 0.0


def agentic(prompt, d, raw_path):
    args = ['claude', '-p', '--model', 'haiku', '--effort', 'high', '--allowedTools', 'Read,Bash',
            '--add-dir', d, '--max-turns', '40', '--output-format', 'stream-json', '--verbose', '--', prompt]
    stdout, timed = '', False
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=600); stdout = r.stdout
    except subprocess.TimeoutExpired as e:
        stdout = (e.stdout or '') if isinstance(e.stdout, str) else ((e.stdout or b'').decode('utf-8', 'ignore')); timed = True
    Path(raw_path).write_text(stdout, encoding='utf-8')
    bash = sympy = turns = 0; cost = 0.0; result = ''
    for line in stdout.splitlines():
        try:
            ev = json.loads(line)
        except Exception:
            continue
        if ev.get('type') == 'assistant':
            for blk in ev.get('message', {}).get('content', []):
                if blk.get('type') == 'tool_use' and blk.get('name') == 'Bash':
                    bash += 1
                    cmd = str(blk.get('input', {}).get('command', ''))
                    if 'python' in cmd or 'sympy' in cmd:
                        sympy += 1
        elif ev.get('type') == 'result':
            result = ev.get('result', '') or ''; cost = ev.get('total_cost_usd', 0) or 0.0; turns = ev.get('num_turns', 0)
    return dict(ans=ans_of(result), bash=bash, sympy=sympy, turns=turns, cost=cost, timeout=timed)


def main():
    gold, fmt = find_meta(STEM)
    ft = '객관식 5지선다' if fmt == 'choice' else '단답형(정수)'
    tiles, d = anon(STEM)
    print(f"═══ PoC2: 단일샷 pass@{K} vs 도구-에이전트 pass@{K} (도구사용 실측) ═══")
    print(f"  대상 {STEM} · 정답 {gold} · 타일 {len(tiles)}장(익명)\n", flush=True)
    tot = 0.0

    pA = (f"문제 이미지:\n{listing(tiles)}\n형식: {ft}\n\n위 이미지를 Read로 연 뒤 끝까지 풀어라. "
          f'풀이 없이 마지막에 ```json\n{{"answer": <정수>}}\n``` 만.')
    pB = (f"문제 이미지:\n{listing(tiles)}\n형식: {ft}\n\n위 이미지를 Read로 본 뒤 **단계별로** 풀어라. "
          f"**암산 금지** — 모든 수치 계산은 반드시 `{VENV_PY}` 를 Bash로 실행해 sympy로 직접 확인하라. "
          f"적분·미분·방정식은 sympy로 풀어라(예: `{VENV_PY} -c \"import sympy as sp; ...\"`). 막히면 코드를 고쳐 다시 실행하라. "
          f'최종 답을 마지막에 ```json\n{{"answer": <정수>}}\n``` 로.')

    print(f"── A. 단일샷 pass@{K} (Read만) ──", flush=True)
    A = []
    with ThreadPoolExecutor(max_workers=4) as ex:
        for fut in as_completed([ex.submit(single, pA, d) for _ in range(K)]):
            a, c = fut.result(); tot += c; A.append(a == gold)
            print(f"    답 {str(a):>4} {'✅' if a == gold else '✗'}", flush=True)
    p1 = sum(A) / K

    print(f"\n── B. 도구-에이전트 pass@{K} (Read+Bash, sympy) ──", flush=True)
    B, bashes = [], []
    with ThreadPoolExecutor(max_workers=3) as ex:
        futs = {ex.submit(agentic, pB, d, str(RAWDIR / f'B_{i}.jsonl')): i for i in range(K)}
        for fut in as_completed(futs):
            r = fut.result(); tot += r['cost']; ok = (r['ans'] == gold); B.append(ok); bashes.append(r['bash'])
            tmo = ' [timeout]' if r['timeout'] else ''
            print(f"    답 {str(r['ans']):>4} {'✅' if ok else '✗'}  · Bash {r['bash']}회(sympy {r['sympy']}) · 턴 {r['turns']}{tmo}", flush=True)
    p2 = sum(B) / K
    used = sum(1 for b in bashes if b > 0)

    print(f"\n═══ 결과 ═══ ${tot:.2f}", flush=True)
    print(f"  A 단일샷    pass@{K} = {sum(A)}/{K} = {p1*100:.0f}%", flush=True)
    print(f"  B 도구반복  pass@{K} = {sum(B)}/{K} = {p2*100:.0f}%  (Bash 실제사용 {used}/{K}런, 평균 {sum(bashes)/K:.1f}회)", flush=True)
    delta = (p2 - p1) * 100
    if used < K * 0.5:
        verdict = f"⚠ 도구를 절반도 안 씀 ({used}/{K}) → Haiku가 Bash 지시를 무시함. '반복+도구' 자체가 발동 안 돼 판정 불가."
    elif p2 > p1 + 12:
        verdict = f"✅ 도구반복이 +{delta:.0f}%p 높음 → '반복+도구 > 단일샷' 입증."
    elif p2 < p1 - 12:
        verdict = f"✗ 도구반복이 오히려 {-delta:.0f}%p 낮음 → 이 문제엔 도구가 역효과."
    else:
        verdict = f"≈ 차이 미미({delta:+.0f}%p) → 이 문제에선 도구가 유의미한 도움 안 됨."
    print(f"  ⇒ {verdict}", flush=True)
    print(f"  (raw 저장: {RAWDIR}/B_*.jsonl — 실제 sympy 코드 확인 가능)", flush=True)
    shutil.rmtree(d, ignore_errors=True)


if __name__ == '__main__':
    main()
