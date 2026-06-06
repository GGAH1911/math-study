#!/usr/bin/env python3
"""인제스트 후처리 동기화 — 새 문제가 /problems(콘텐츠) + /concepts(역인덱스) 둘 다 즉시 반영되게.

인제스트(ingest_v2/ingest_gyo3)는 markdown 만 쓰고 끝난다. 그러면:
  · /problems 목록 — getCollection 실시간이지만, dev 서버가 외부 ../docs 의 *새 폴더*를 라이브로
    못 잡으므로(서버 시작 후 생성된 회차 디렉토리) 콘텐츠 재-glob(서버 재시작)이 필요.
  · /concepts 개념→문제 역인덱스·그래프 — predev 체인(node)이 만든 JSON 이라 재생성 필요.
이 스크립트가 무결성 가드 + 그 둘을 한 번에 처리한다. 인제스트 파이프라인 끝에 자동 호출.

사용: python scripts/post_ingest_sync.py [--no-server]
  --no-server : dev 서버 재시작 생략 (개념 동기화만; /problems 가 이미 최신이거나 다운타임 회피 시)
환경: MATHSTUDY_ROOT (워크트리 오버라이드)
"""
import sys, os, re, glob, subprocess
from pathlib import Path

ROOT = Path(os.environ.get('MATHSTUDY_ROOT', Path(__file__).resolve().parent.parent)).resolve()
WEB = ROOT / 'web'
NO_SERVER = '--no-server' in sys.argv


def _scan_dupkeys():
    """frontmatter 중복키/파싱오류 탐지 — js-yaml(=Astro)은 중복키를 fatal 처리하므로 콘텐츠 빌드를 크래시시킨다."""
    import yaml
    bad = {}
    files = (glob.glob(str(ROOT / 'docs' / 'problems' / '**' / '*.md'), recursive=True) +
             glob.glob(str(ROOT / 'docs' / 'concepts' / '**' / '*.md'), recursive=True))
    for f in files:
        m = re.match(r'^---\n(.*?)\n---', Path(f).read_text(encoding='utf-8'), re.S)
        if not m:
            continue
        found = []

        class L(yaml.SafeLoader):
            pass

        def cm(loader, node, deep=False, _f=found):
            s = set()
            for kn, vn in node.value:
                k = loader.construct_object(kn, deep=deep)
                if k in s:
                    _f.append(k)
                s.add(k)
            return yaml.SafeLoader.construct_mapping(loader, node, deep)
        L.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, cm)
        try:
            yaml.load(m.group(1), Loader=L)
        except Exception as e:
            found.append(f'PARSE:{str(e)[:40]}')
        if found:
            bad[f] = found
    return bad


def _fix_dupkeys(path):
    """frontmatter 안에서 같은 들여쓰기 레벨의 중복 키 라인 제거(첫 occurrence 유지)."""
    lines = Path(path).read_text(encoding='utf-8').split('\n')
    out = []
    fm = 0
    seen = set()
    for ln in lines:
        if ln.strip() == '---':
            fm += 1
            if fm == 1:
                seen = set()
            out.append(ln)
            continue
        if fm == 1:
            mk = re.match(r'(\s*)([\w.\-]+)\s*:', ln)
            if mk:
                key = (len(mk.group(1)), mk.group(2))
                if key in seen:
                    continue        # 중복 → drop
                seen.add(key)
        out.append(ln)
    Path(path).write_text('\n'.join(out), encoding='utf-8')


def guard():
    bad = _scan_dupkeys()
    if not bad:
        print("  ✓ frontmatter 무결 (중복키/파싱오류 0)", flush=True)
        return True
    parse_errs = [f for f, v in bad.items() if any(str(x).startswith('PARSE') for x in v)]
    print(f"  ⚠ 중복키/파싱오류 {len(bad)}개 → 자동 정정", flush=True)
    for f, keys in bad.items():
        if f in parse_errs:
            continue                # 파싱오류는 자동수정 위험 → 아래서 abort
        _fix_dupkeys(f)
        print(f"    정정: {Path(f).name} ← 중복키 {keys}", flush=True)
    bad2 = _scan_dupkeys()
    if bad2:
        print(f"  🔴 자동정정 후에도 {len(bad2)}개 잔존 — 수동 확인 필요(서버 재시작 보류):", flush=True)
        for f, v in list(bad2.items())[:10]:
            print(f"    {f}: {v}", flush=True)
        return False
    print("  ✓ 정정 완료 (재스캔 0)", flush=True)
    return True


def node_sync():
    """개념 매핑 정정 + 역인덱스·그래프·허브 재생성 (JSON 출력 → Vite HMR 라이브 반영, 다운타임 0)."""
    steps = [
        ['node', 'scripts/fill-missing-problem-concepts.mjs', '--apply'],
        ['node', 'scripts/relink-restored-concepts.mjs', '--apply'],
        ['node', 'scripts/sync-assets.mjs'],
        ['node', 'scripts/build-concept-hubs.mjs'],
        ['node', 'scripts/build-problem-hubs.mjs'],
        ['node', 'scripts/build-concept-graph.mjs'],
        ['node', 'scripts/build-problem-index.mjs'],
    ]
    for cmd in steps:
        print(f"  ▶ {' '.join(cmd[1:])}", flush=True)
        if subprocess.run(cmd, cwd=str(WEB)).returncode != 0:
            print(f"  🔴 실패: {' '.join(cmd)}", flush=True)
            return False
    print("  ✓ 개념 역인덱스·그래프·허브 재생성 (HMR 반영)", flush=True)
    return True


def server_refresh():
    """콘텐츠 컬렉션 재-glob — dev 서버 재시작(가드 통과 후라 크래시루프 없음). 서버 떠 있을 때만."""
    sv = ROOT / 'server.sh'
    if not sv.exists():
        print("  (server.sh 없음 — 스킵)", flush=True)
        return True
    if subprocess.run(['pgrep', '-f', 'astro dev'], capture_output=True).returncode != 0:
        print("  (dev 서버 미가동 — 재시작 스킵)", flush=True)
        return True
    print("  ▶ dev 서버 재시작 (콘텐츠 재-glob → /problems 새 회차 반영, ~10s 다운타임)", flush=True)
    return subprocess.run([str(sv), 'restart'], cwd=str(ROOT)).returncode == 0


def main():
    print("══ 인제스트 후처리 동기화 ══", flush=True)
    print("[1/3] frontmatter 무결성 가드 (중복키 YAML 크래시 방지)", flush=True)
    if not guard():
        sys.exit("🔴 가드 실패 — 위 파일 수정 후 재실행 (서버 재시작 안 함)")
    print("[2/3] 개념 매핑·역인덱스·그래프 동기화", flush=True)
    if not node_sync():
        sys.exit("🔴 동기화 실패")
    print("[3/3] dev 서버 콘텐츠 리프레시", flush=True)
    if NO_SERVER:
        print("  (--no-server: 재시작 생략)", flush=True)
    else:
        server_refresh()
    print("✅ 후처리 동기화 완료", flush=True)


if __name__ == '__main__':
    main()
