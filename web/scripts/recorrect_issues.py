#!/usr/bin/env python3
# 별도 재교정 러너(연속 루프) — verify가 flag한 issue(corrector_verify: issues)를 agy(무료)로 재교정. verify와 독립.
#   ★연속 루프: 새 issue가 쌓이면 계속 처리(verify가 쌓는 족족). flock 단일인스턴스.
#   성공 시 corrector_verify/issues 마커 제거(→ '교정됨·미검증' = 나중 fixed verify가 재검증).
#   agy 빈출력(쿼터소진)이면 30s 대기 후 1회 재시도, 그래도 비면 skip(다음 루프/keepalive가 살림).
#   격리(agy 재시도도 실패) → opus 손교정 대상으로 남김.
#   로그: /tmp/ingest_logs/recorrect_issues.log
import glob, re, subprocess, os, time, sys, fcntl
REPO = __import__('os').environ.get('MATHSTUDY_ROOT') or __import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__))))  # ★레포 위치 자동(이동 내성)
LOG = '/tmp/ingest_logs/recorrect_issues.log'
os.makedirs('/tmp/ingest_logs', exist_ok=True)
def log(m):
    line = f"[{time.strftime('%H:%M:%S')}] {m}"
    print(line, flush=True)
    open(LOG, 'a', encoding='utf-8').write(line + '\n')

def find_targets():
    out = []
    for md in glob.glob(f'{REPO}/docs/problems/**/*.md', recursive=True):
        t = open(md, encoding='utf-8').read()
        if not re.search(r'^corrector_verify: issues', t, re.M): continue
        if re.search(r'^corrector_quarantine: true', t, re.M): continue  # 격리는 opus
        slug = os.path.basename(md)[:-3]; m = re.match(r'^(.+)_([^_]+)_(\d+)$', slug)
        if m: out.append((slug, m.group(1), m.group(2), m.group(3), md))
    return out

def agy_recorrect(rnd, subj, num):
    return subprocess.run(['node', f'{REPO}/web/scripts/corrector.mjs', rnd, subj, num],
                          env={**os.environ, 'CORR_BACKEND': 'agy'}, capture_output=True, text=True, cwd=f'{REPO}/web')

def clear_verify(md):
    t = open(md, encoding='utf-8').read()
    t = re.sub(r'\ncorrector_verify:.*(?=\n)', '', t)
    t = re.sub(r'\ncorrector_verify_issues:(?:\n  - .*)*(?=\n)', '', t)
    open(md, 'w', encoding='utf-8').write(t)

# 단일 인스턴스
lk = open('/tmp/recorrect_issues.lock', 'w')
try:
    fcntl.flock(lk, fcntl.LOCK_EX | fcntl.LOCK_NB)
except OSError:
    log('이미 실행 중 — 중복 기동 안 함'); sys.exit(0)

log('=== 재교정 러너 시작(연속 루프, agy 무료) ===')
while True:
    targets = find_targets()
    if not targets:
        time.sleep(60); continue   # 새 issue 대기(verify가 쌓을 때까지)
    log(f'배치 {len(targets)}건 (corrector_verify:issues)')
    done = fail = quota = 0
    for slug, rnd, subj, num, md in targets:
        r = agy_recorrect(rnd, subj, num)
        t = open(md, encoding='utf-8').read()
        if re.search(r'^corrector_quarantine: true', t, re.M):
            fail += 1; log(f'  ⚠ 격리(agy 재시도도 실패) → opus: {slug}')
        elif r.returncode == 3:  # agy 빈출력(쿼터)
            time.sleep(30); r2 = agy_recorrect(rnd, subj, num); t = open(md, encoding='utf-8').read()
            if r2.returncode == 3:
                quota += 1; log(f'  agy 쿼터소진 skip(다음 루프): {slug}')
            elif not re.search(r'^corrector_quarantine: true', t, re.M):
                clear_verify(md); done += 1; log(f'  ✓ 재교정(재시도): {slug}')
            else:
                fail += 1; log(f'  ⚠ 격리: {slug}')
        else:
            clear_verify(md); done += 1; log(f'  ✓ 재교정: {slug}')
    log(f'배치 완료: 재교정 {done} · 격리(opus) {fail} · 쿼터skip {quota}')
    time.sleep(20)
