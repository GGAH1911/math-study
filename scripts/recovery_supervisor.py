#!/usr/bin/env python3
"""야간 자가 복구 supervisor — solution-cache 빌드를 끝까지 밀어붙인다.

문제: background 프로세스가 harness reaping/외부 kill 로 ~20-40분마다 죽고,
API 사용량 한도(rate limit)에 걸리면 대량 gen-fail 한다. 사람이 못 지킬 때
이 supervisor 가:
  1. 미캐시 목록을 매 pass 새로 생성(캐시되며 줄어듦) → --list 로 그것만 실행.
  2. pass 가 죽거나 끝나면 자동으로 다음 pass.
  3. breaker(연속 gen-fail=API 한도) 감지 시 45분 sleep 후 재시도(한도 리셋 대기).
  4. 한 pass 가 캐시를 0개 늘리면(= 남은 건 데이터오류/불가) 중단.
각 pass 는 자식 subprocess 라, supervisor 가 살아있는 한 reaping 돼도 다음 pass 가 이어감.
캐시는 문제마다 즉시 파일 기록 → 죽어도 누적 보존.
"""
import os, re, glob, time, subprocess

ROOT = __import__('os').environ.get('MATHSTUDY_ROOT') or __import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__)))  # ★레포 위치 자동(이동 내성)
os.chdir(ROOT)
SLOG = '/tmp/recovery_supervisor.log'
PASS_LOG = '/tmp/recovery_pass.log'
PARALLEL = '16'
MAX_PASSES = 40


def log(m):
    line = f'[{int(time.time())}] {m}'
    with open(SLOG, 'a') as f:
        f.write(line + '\n')
    print(line, flush=True)


def cached_count():
    r = subprocess.run("grep -rl '^solution:' docs/problems --include='*.md' | wc -l",
                       shell=True, capture_output=True, text=True)
    try: return int(r.stdout.strip())
    except Exception: return -1


_TIER = {'killer': 0, 'mid': 1, 'early': 2}
def gen_uncached():
    items = []
    for f in glob.glob('docs/problems/**/*.md', recursive=True):
        if 'README' in f:
            continue
        t = open(f, encoding='utf-8').read()
        if re.search(r'^solution:', t, re.M):
            continue
        g = lambda k: (re.search(rf'^\s*{k}:\s*(.+?)\s*$', t, re.M) or [None, '?'])[1]
        try: sc = -int(g('score') or 0)
        except Exception: sc = 0
        try: num = -int(g('number') or 0)
        except Exception: num = 0
        items.append(((_TIER.get(g('killer_tier'), 3), sc, num), f.split('/')[-1][:-3]))
    items.sort(reverse=True)  # easy-first
    slugs = [s for _, s in items]
    open('/tmp/uncached.txt', 'w').write(','.join(slugs))
    return len(slugs)


def kill_preexisting():
    me = os.getpid()
    for c in glob.glob('/proc/[0-9]*/cmdline'):
        try:
            pid = int(c.split('/')[2])
            cmd = open(c).read().replace('\0', ' ')
        except Exception:
            continue
        if pid != me and 'build_solution_cache.py --list' in cmd and cmd.strip().startswith('python'):
            try: os.kill(pid, 9); log(f'killed pre-existing recovery pid {pid}')
            except Exception: pass


log(f'=== supervisor START · cached={cached_count()}/2844 ===')
kill_preexisting()
time.sleep(2)
prev = cached_count()

for p in range(1, MAX_PASSES + 1):
    n = gen_uncached()
    log(f'[pass {p}] uncached={n} cached={cached_count()}/2844')
    if n <= 0:
        log('ALL CACHED — done.'); break
    with open(PASS_LOG, 'w') as pf:
        subprocess.run(
            f'python3 scripts/build_solution_cache.py --list "$(cat /tmp/uncached.txt)" --parallel {PARALLEL}',
            shell=True, stdout=pf, stderr=subprocess.STDOUT)
    now = cached_count()
    breaker = '연속 실패' in open(PASS_LOG, encoding='utf-8', errors='ignore').read()
    log(f'[pass {p}] end: cached {prev}→{now} (+{now-prev}) breaker={breaker}')
    if breaker:
        log(f'[pass {p}] API 한도 의심 → 45분 sleep 후 재시도'); time.sleep(2700)
    elif now <= prev:
        log(f'[pass {p}] 진행 0 — 남은 건 데이터오류/불가. 중단.'); break
    else:
        time.sleep(120)
    prev = now

log(f'=== supervisor END · cached={cached_count()}/2844 ===')
