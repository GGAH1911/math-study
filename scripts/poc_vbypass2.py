#!/usr/bin/env python3
"""Vision 병목 최종 확정 — 검증기의 '진짜 식'을 텍스트로 주면 Haiku가 푸나?
ground truth(검증기): (5/n + 3/n²)/(1/n − 2/n³), 극한 5. Haiku는 이미지를 'n − n²/2'로 오독했음.
T1 텍스트만 · T2 텍스트+sympy, pass@K. 이미지-Haiku 0/8과 대비."""
import re, json, os, subprocess, tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed

K = int(os.environ.get('VB2_K', '8'))
VENV_PY = __import__('os').environ.get('MS_PY', __import__('os').path.expanduser('~/.venvs/ms-ingest/bin/python'))  # ★인제스트 venv(레포 .venv 는 빈 마운트포인트)
GOLD = '5'
LATEX = r"\lim_{n\to\infty}\dfrac{\dfrac{5}{n}+\dfrac{3}{n^{2}}}{\dfrac{1}{n}-\dfrac{2}{n^{3}}}"


def ans_of(t):
    for b in reversed(re.findall(r'```json\s*(.*?)```', t, re.DOTALL)):
        try:
            return str(json.loads(b).get('answer')).strip()
        except Exception:
            pass
    return None


def haiku(with_tools, d):
    base = f"다음 극한의 값은? (객관식 5지선다)\n  ${LATEX}$\n  ① 1  ② 2  ③ 3  ④ 4  ⑤ 5\n\n"
    if with_tools:
        p = base + f"필요하면 `{VENV_PY}` 를 Bash로 실행해 sympy로 계산하라. 최종 답을 ```json\n{{\"answer\": <보기 1-5>}}\n``` 로."
        args = ['claude', '-p', '--model', 'haiku', '--effort', 'high', '--allowedTools', 'Bash',
                '--add-dir', d, '--max-turns', '15', '--output-format', 'json', '--', p]
    else:
        p = base + '풀이·설명 없이 최종 답만 ```json\n{"answer": <보기 1-5>}\n``` 로.'
        args = ['claude', '-p', '--model', 'haiku', '--effort', 'high', '--allowedTools', 'none',
                '--max-turns', '4', '--output-format', 'json', '--', p]
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=180)
        env = json.loads(r.stdout)
    except Exception:
        return None, 0.0
    return ans_of(env.get('result', '') or ''), env.get('total_cost_usd', 0) or 0.0


def main():
    d = tempfile.mkdtemp(prefix='vb2_')
    print(f"═══ Vision 병목 최종확정: 진짜 식을 텍스트로 → Haiku pass@{K} ═══")
    print(f"  식: (5/n + 3/n²)/(1/n − 2/n³) · 정답 {GOLD} · (이미지-Haiku = 0/8)\n", flush=True)
    tot = 0.0
    out = {}
    for arm, tools in [('T1 텍스트만(도구X)', False), ('T2 텍스트+sympy', True)]:
        print(f"── {arm} ──", flush=True)
        res = []
        with ThreadPoolExecutor(max_workers=4) as ex:
            for fut in as_completed([ex.submit(haiku, tools, d) for _ in range(K)]):
                a, c = fut.result(); tot += c; res.append(a == GOLD)
                print(f"    답 {str(a):>4} {'✅' if a == GOLD else '✗'}", flush=True)
        out[arm] = sum(res)
        print(f"  → {arm}: {sum(res)}/{K} = {100*sum(res)//K}%\n", flush=True)
    print(f"═══ 결론 ═══ ${tot:.2f}", flush=True)
    print(f"  이미지-Haiku       : 0/8 = 0%", flush=True)
    for arm, s in out.items():
        print(f"  텍스트-Haiku {arm[:8]}: {s}/{K} = {100*s//K}%", flush=True)
    win = max(out.values())
    if win >= K * 0.6:
        print(f"  ⇒ ✅✅ VISION이 유일 병목 확정 — 식을 텍스트로 주면 Haiku가 바로 풂.", flush=True)
        print(f"     'solved_by=opus'는 'Opus만 그 조밀한 식을 읽었다'는 뜻 (수학 우위 아님).", flush=True)
    else:
        print(f"  ⇒ 텍스트로도 잘 못 풂 → vision 외 수학 난이도도 존재.", flush=True)


if __name__ == '__main__':
    main()
