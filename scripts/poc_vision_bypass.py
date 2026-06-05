#!/usr/bin/env python3
"""Vision 병목 확정 — 식을 '정확한 텍스트'로 주면 Haiku가 푸나? (이미지 우회)
1) Opus(강 vision)로 식 전사 → 독립검증: sympy로 limit 계산 == 정답?
2) Haiku 텍스트 풀이 pass@K: T1 텍스트만(도구X) · T2 텍스트+sympy.
   PoC2의 이미지-Haiku 0/8과 비교 → 텍스트로 풀리면 vision이 유일 병목 확정.
환경: VB_STEM(2022_수능_미적분_23), VB_K(8)."""
from __future__ import annotations
import re, json, os, subprocess, sys, shutil, tempfile, glob
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import sympy as sp

ROOT = Path(__file__).resolve().parent.parent
IMGDIR = ROOT / 'web' / 'public' / 'problem-images'
VENV_PY = '/home/insung/Projects/math-study/.venv/bin/python'
sys.path.insert(0, str(ROOT / 'scripts'))
from tiling import tile_for_vision  # noqa: E402

K = int(os.environ.get('VB_K', '8'))
STEM = os.environ.get('VB_STEM', '2022_수능_미적분_23')


def find_gold(stem):
    for f in glob.glob(str(ROOT / 'docs' / 'problems' / '**' / (stem + '.md')), recursive=True):
        t = Path(f).read_text(encoding='utf-8')
        m = re.search(r'^answer:\s*"?(\d+)"?', t, re.M)
        return m.group(1) if m else None
    return None


def anon(stem):
    tiles = tile_for_vision((IMGDIR / (stem + '.png')).resolve())
    d = tempfile.mkdtemp(prefix='vb_'); out = []
    for i, t in enumerate(tiles):
        o = Path(d) / f'p_{i + 1}.png'; shutil.copy(t, o); out.append(str(o))
    return out, d


def listing(tiles):
    return '\n'.join(f'    {i + 1}. {p}' for i, p in enumerate(tiles))


def claude_json(model, prompt, tools, add_dir, turns, timeout):
    args = ['claude', '-p', '--model', model, '--effort', 'high', '--allowedTools', tools,
            '--add-dir', add_dir, '--max-turns', str(turns), '--output-format', 'json', '--', prompt]
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        env = json.loads(r.stdout)
    except Exception:
        return '', 0.0
    return env.get('result', '') or '', env.get('total_cost_usd', 0) or 0.0


def ans_of(txt):
    for b in reversed(re.findall(r'```json\s*(.*?)```', txt, re.DOTALL)):
        try:
            return str(json.loads(b).get('answer')).strip()
        except Exception:
            pass
    return None


def transcribe_opus(tiles, d):
    p = (f"문제 이미지:\n{listing(tiles)}\n\n위 이미지의 극한식을 한 글자도 틀리지 않게 읽어라. "
         f"분자와 분모를 각각 변수 n에 대한 **sympy 파싱 가능한 식**으로 적어라(예: '1/n - 2/n**2'). "
         f"마지막에 오직 ```json\n{{\"latex\": \"<읽기용 LaTeX, lim 포함>\", \"num\": \"<분자>\", \"den\": \"<분모>\"}}\n```")
    txt, cost = claude_json('opus', p, 'Read', d, 12, 300)
    for b in reversed(re.findall(r'```json\s*(.*?)```', txt, re.DOTALL)):
        try:
            return json.loads(b), cost
        except Exception:
            pass
    return None, cost


def validate(j, gold):
    n = sp.Symbol('n')
    try:
        num = sp.sympify(str(j['num']).replace('^', '**'))
        den = sp.sympify(str(j['den']).replace('^', '**'))
        val = sp.limit(num / den, n, sp.oo)
        ok = (sp.simplify(val - sp.Integer(int(gold))) == 0)
        return str(val), ok
    except Exception as e:
        return f'parse-err: {e}', False


def haiku_text(latex, with_tools, d):
    base = (f"다음 극한의 값은? (객관식 5지선다)\n  ${latex}$\n  ① 1  ② 2  ③ 3  ④ 4  ⑤ 5\n\n")
    if with_tools:
        prompt = base + (f"필요하면 `{VENV_PY}` 를 Bash로 실행해 sympy로 계산하라. "
                         f'최종 답을 마지막에 ```json\n{{"answer": <보기번호 1-5>}}\n``` 로.')
        txt, cost = claude_json('haiku', prompt, 'Bash', d, 20, 240)
    else:
        prompt = base + '풀이·설명 없이 최종 답만 ```json\n{"answer": <보기번호 1-5>}\n``` 로.'
        txt, cost = claude_json('haiku', prompt, 'none', d, 4, 120)
    return ans_of(txt), cost


def main():
    gold = find_gold(STEM)
    tiles, d = anon(STEM)
    print(f"═══ Vision 병목 확정: 이미지 우회(텍스트) Haiku pass@{K} ═══")
    print(f"  대상 {STEM} · 정답 {gold} · (이미지-Haiku PoC2 baseline = 0/8)\n", flush=True)
    tot = 0.0

    # 1. Opus 전사 + 독립검증
    print("── 1. Opus 전사 (강 vision) + 독립검증 ──", flush=True)
    j, c = transcribe_opus(tiles, d); tot += c
    if not j:
        print("  ✗ Opus 전사 실패 — 중단"); shutil.rmtree(d, ignore_errors=True); return
    val, ok = validate(j, gold)
    print(f"  Opus가 읽은 식: {j.get('latex', '')}", flush=True)
    print(f"  분자={j.get('num')} / 분모={j.get('den')}  → sympy limit = {val}", flush=True)
    print(f"  독립검증(limit==정답{gold}): {'✅ 전사 정확' if ok else '⚠ 불일치(전사 의심)'}\n", flush=True)
    latex = j.get('latex') or f"\\lim_{{n\\to\\infty}} \\dfrac{{{j.get('num')}}}{{{j.get('den')}}}"

    # 2. Haiku 텍스트 풀이 pass@K
    for arm, tools in [('T1 텍스트만(도구X)', False), ('T2 텍스트+sympy', True)]:
        print(f"── {arm} · Haiku pass@{K} ──", flush=True)
        res = []
        with ThreadPoolExecutor(max_workers=4) as ex:
            for fut in as_completed([ex.submit(haiku_text, latex, tools, d) for _ in range(K)]):
                a, c = fut.result(); tot += c; r = (a == gold); res.append(r)
                print(f"    답 {str(a):>4} {'✅' if r else '✗'}", flush=True)
        print(f"  → {arm}: {sum(res)}/{K} = {100*sum(res)/K:.0f}%\n", flush=True)
        if not tools:
            t1 = sum(res)
        else:
            t2 = sum(res)

    print(f"═══ 결론 ═══ ${tot:.2f}", flush=True)
    print(f"  이미지-Haiku (PoC2)      : 0/8 = 0%", flush=True)
    print(f"  텍스트-Haiku (T1, 도구X) : {t1}/{K} = {100*t1/K:.0f}%", flush=True)
    print(f"  텍스트-Haiku (T2, +sympy): {t2}/{K} = {100*t2/K:.0f}%", flush=True)
    if max(t1, t2) >= K * 0.5:
        print(f"  ⇒ ✅ Vision이 유일 병목 확정 — 식을 텍스트로 주면 Haiku가 풂. '난이도=opus'는 사실 'Haiku가 못 읽음'.", flush=True)
    elif ok:
        print(f"  ⇒ 텍스트로도 잘 못 풂 → vision 외 수학 난이도도 있음(부분 병목).", flush=True)
    else:
        print(f"  ⇒ Opus 전사가 미검증이라 판정 보류.", flush=True)
    shutil.rmtree(d, ignore_errors=True)


if __name__ == '__main__':
    main()
