#!/usr/bin/env python3
"""Future-leak(암기 오염) 실측 — 모델이 '식별자만으로' 정답을 기억하는지.
이미지·문제본문 없이 출처 식별자(예: '2024학년도 수능 수학 22번')만 주고 정답을 물음.
단답형(정수)은 본문 없이 맞히면 추측이 거의 불가 → 정답=암기의 스모킹건.
유명(수능·평가원 모평) vs 무명(교육청 고1·고2 학평) 회상률 비교 → 난이도 신호가 암기로 오염됐는지 판정.
환경: PROBE_MODEL(haiku), PROBE_N(12 그룹당), PROBE_WORKERS(4)."""
from __future__ import annotations
import re, glob, json, os, subprocess, time, random
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parent.parent
MODEL = os.environ.get('PROBE_MODEL', 'haiku')
N = int(os.environ.get('PROBE_N', '12'))
WORKERS = int(os.environ.get('PROBE_WORKERS', '4'))
random.seed(42)
SYS = "당신은 정직한 조수입니다. 모르는 것은 모른다고 답하고, 절대 추측하지 않습니다."


def meta_of(t):
    g = lambda k: (m.group(1).strip().strip('\'"') if (m := re.search(rf'^\s*{k}:\s*(.+?)\s*$', t, re.M)) else None)
    return dict(agency=g('agency'), exam_type=g('exam_type'), year=g('year'), session=g('session'),
                grade=g('grade'), subject=g('subject'), number=g('number'), answer=g('answer'), fmt=g('format'))


def ident(m):
    sub = m['subject']
    subs = '' if sub in (None, '단일', '공통') else f' {sub}'
    if m['exam_type'] == '수능':
        return f"{m['year']}학년도 대학수학능력시험 수학{subs} {m['number']}번"
    if m['exam_type'] == '모평':
        return f"{m['year']}학년도 {m['session']} 모의평가 수학{subs} {m['number']}번"
    return f"{m['year']}년 {m['grade']} {m['session']} 전국연합학력평가 수학 {m['number']}번"


def probe(item):
    label, ids, gold = item
    prompt = (f"아래는 한국 고등학교 수학 시험 문제의 출처 식별자입니다 (문제 본문·이미지·그림은 제공하지 않습니다):\n"
              f"  「{ids}」\n\n"
              f"당신이 이 특정 문제를 **이미 알고 있어서 정답이 기억난다면** 그 정답을 적으세요. "
              f"문제 본문 없이는 알 수 없거나 기억나지 않으면 반드시 \"UNKNOWN\"이라고 답하세요. **추측 절대 금지.**\n"
              f"단답형 정답은 정수입니다. 마지막에 오직 ```json 한 블록만:\n"
              f'```json\n{{"recall": <기억나는 정수 정답, 모르면 "UNKNOWN">}}\n```')
    args = ['claude', '-p', '--model', MODEL, '--effort', 'low', '--max-turns', '2',
            '--system-prompt', SYS, '--output-format', 'json', '--', prompt]
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=70)
        env = json.loads(r.stdout)
    except Exception:
        return dict(label=label, ids=ids, gold=gold, recall=None, ok=False, unknown=False, cost=0.0)
    txt, cost = env.get('result', '') or '', env.get('total_cost_usd', 0) or 0.0
    rec = None
    for b in reversed(re.findall(r'```json\s*(.*?)```', txt, re.DOTALL)):
        try:
            rec = json.loads(b).get('recall'); break
        except Exception:
            pass
    if rec is None:
        rec = 'UNKNOWN' if 'UNKNOWN' in txt else None
    unknown = (str(rec).upper() == 'UNKNOWN')
    ok = (not unknown) and rec is not None and str(rec).strip() == str(gold).strip()
    return dict(label=label, ids=ids, gold=gold, recall=rec, ok=ok, unknown=unknown, cost=cost)


# 단답형 + 정수답 수집, 유명/무명 그룹
fam, obs = [], []
for f in glob.glob(str(ROOT / 'docs' / 'problems' / '**' / '*.md'), recursive=True):
    if 'README' in f:
        continue
    t = Path(f).read_text(encoding='utf-8'); m = meta_of(t)
    if m['fmt'] != 'numeric' or not m['answer'] or not re.fullmatch(r'\d{1,4}', m['answer'] or ''):
        continue
    if not (m['year'] and m['number']):
        continue
    rec = ('famous' if m['exam_type'] in ('수능', '모평') else 'obscure', ident(m), m['answer'])
    (fam if rec[0] == 'famous' else obs).append(rec)
random.shuffle(fam); random.shuffle(obs)
targets = fam[:N] + obs[:N]
print(f"═══ Future-leak 실측 ({MODEL}, 이미지·본문 없이 식별자만) ═══")
print(f"  유명(수능·평가원) {min(N,len(fam))} · 무명(교육청) {min(N,len(obs))}  = {len(targets)}문제\n", flush=True)

res, tot = [], 0.0
with ThreadPoolExecutor(max_workers=WORKERS) as ex:
    for fut in as_completed({ex.submit(probe, it): it for it in targets}):
        r = fut.result(); res.append(r); tot += r['cost']
        tag = '🎯 정답회상' if r['ok'] else ('· UNKNOWN(정직)' if r['unknown'] else f"✗ 오답({r['recall']})")
        print(f"  [{r['label'][:4]}] {r['ids']:42s} 정답 {r['gold']:>4} | 회상 {str(r['recall'])[:8]:>8}  {tag}", flush=True)


def stat(lab):
    g = [r for r in res if r['label'] == lab]
    if not g:
        return f"{lab}: 없음"
    rc = sum(r['ok'] for r in g); uk = sum(r['unknown'] for r in g)
    return f"{lab}: 정답회상 {rc}/{len(g)} ({100*rc/len(g):.0f}%) · UNKNOWN {uk} · 오답 {len(g)-rc-uk}"


print(f"\n═══ 결과 ═══  ${tot:.2f}")
print("  " + stat('famous'))
print("  " + stat('obscure'))
print("  ⇒ 단답형은 본문 없이 정답을 못 맞히는 게 정상. '정답회상'이 높을수록 = 암기 오염(난이도 신호 위협).")
