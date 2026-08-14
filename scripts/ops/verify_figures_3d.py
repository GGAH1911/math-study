#!/usr/bin/env python3
"""미리 만들어 둔 3D 도형 스펙이 여전히 유효한지 검사한다.

세 가지를 본다:
  ① 렌더러가 아는 type·속성만 쓰는가 — Geometry3D.tsx **타입 정의**에서 뽑는다(주석 아님).
     ★모르는 속성은 예외를 내지 않고 **조용히 무시**된다. 2026-08 에 polygon.points 를
       257개 위젯이 쓰다가 도형이 통째로 사라진 적이 있다.
  ② 좌표가 3D 인가 — [x, y] 두 성분이면 납작해진 것이다.
  ③ verify 코드를 실제로 돌려 [VERIFY FAIL] 이 없는가 (--deep 일 때만. sympy 실행이라 느리다)

사용: python3 scripts/ops/verify_figures_3d.py [--deep]
"""
from __future__ import annotations
import hashlib, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / 'web/src/data/figures-3d'
# 타입 정의는 2026-08-14 에 geometry3d-core.ts 로 갈라졌다(Geometry3D.tsx 래칫 초과).
TSX = ROOT / 'web/src/lib/geometry3d-core.ts'
RUNNER = ROOT / 'scripts/ops/sympy_run.py'


def vocabulary() -> dict[str, set[str]]:
    """타입 정의에서 {shape type: 허용 속성 집합} 을 뽑는다."""
    src = TSX.read_text(encoding='utf-8')
    # ★유니온 **전체**를 잡아야 한다. `;\n` 까지만 잡으면 polyhedron 브랜치 첫 줄
    #   (`| { type: 'polyhedron';`) 의 세미콜론에서 끊겨 polyhedron 이하 6개 타입의
    #   속성 어휘가 통째로 비고, 정상 스펙이 전부 "모르는 속성" 으로 오탐된다.
    #   유니온의 끝은 `};` + **빈 줄** 이므로 거기까지 간다.
    m = re.search(r'export type Geom3DShape =(.*?);\s*\n\s*\n', src, re.S)
    if not m:
        sys.exit(f'Geom3DShape 타입 정의를 못 찾았다 — {TSX.relative_to(ROOT)} 구조가 바뀌었나?')
    vocab: dict[str, set[str]] = {}
    for branch in m.group(1).split('| {')[1:]:
        t = re.search(r"type:\s*'([a-zA-Z0-9]+)'", branch)
        if not t:
            continue
        vocab[t.group(1)] = set(re.findall(r'(\w+)\??:', branch)) | {'type'}
    return vocab



def _is_prose(v: str) -> bool:
    """도형 위 글씨가 '설명'인지. 한글이 섞인 긴 문자열 또는 괄호 설명을 잡는다.

    짧은 이름표(`구 S`, `평면 BCD`, `xy평면`)는 통과시킨다 — 그건 라벨이 맞다.
    KaTeX 수식($...$)은 아무리 길어도 통과 — `$\\dfrac{5\\sqrt{3}}{3}$` 같은 건 정상이다.
    """
    core = re.sub(r'\$[^$]*\$', '', v).strip()          # 수식 부분은 길이에서 뺀다
    has_hangul = bool(re.search(r'[가-힣]', core))
    if not has_hangul:
        return False
    return len(core) > 13 or bool(re.search(r'\([^)]{6,}\)', core))


SPEC_KEYS = {'shapes', 'cameraPosition', 'cameraTarget', 'cameraUp', 'axes', 'gridSize', 'bgColor', 'title', 'displayScale'}


def check(path: Path, vocab: dict[str, set[str]], deep: bool) -> list[str]:
    bad: list[str] = []
    try:
        e = json.loads(path.read_text(encoding='utf-8'))
    except Exception as ex:
        return [f'JSON 파싱 실패: {ex}']
    for k in ('spec', 'conditions', 'verify'):
        if k not in e:
            bad.append(f'필수 필드 `{k}` 없음')
    spec = e.get('spec') or {}
    for k in spec:
        if k not in SPEC_KEYS:
            bad.append(f'spec 최상위에 모르는 키 `{k}`')
    ds = spec.get('displayScale')
    if ds is not None:
        # ★축을 따로 늘리면 각도·길이가 눈으로는 거짓말을 한다. 구·원이 있으면 찌그러져
        #   "접한다" 가 안 보이므로 금지하고, 배율도 상식선(1/8배 ~ 8배)으로 묶는다.
        if not (isinstance(ds, list) and len(ds) == 3 and all(isinstance(v, (int, float)) and 0.125 <= v <= 8 for v in ds)):
            bad.append(f'displayScale 이 [sx,sy,sz] (각 0.125-8) 가 아니다: {ds}')
        elif all(v == 1 for v in ds):
            bad.append('displayScale 이 [1,1,1] 이다 — 뺄 것 (캡션만 붙는다)')
        for s_ in (spec.get('shapes') or []):
            if s_.get('type') in ('sphere',):
                bad.append('구가 있는데 displayScale 을 썼다 — 구가 타원체가 되어 접점이 안 보인다')
                break
    # ★본문이 바뀌었는데 스펙이 그대로면 **틀린 그림이 조용히 남는다.** 레지스트리가
    #   docs/ 바깥이라 재인제스트·교정에도 살아남는 것이 장점이자 위험이다.
    sha = e.get('source_sha')
    if sha:
        hits = list((ROOT / 'docs/problems').rglob(f'{path.stem}.md'))
        if hits:
            cur = hashlib.sha256(hits[0].read_bytes()).hexdigest()[:16]
            if cur != sha:
                bad.append(f'문제 본문이 바뀌었다(source_sha {sha} → {cur}) — 스펙이 낡았을 수 있다. '
                           f'확인 후 재작성하거나 source_sha 를 갱신해라')
    cu = spec.get('cameraUp')
    if cu is not None and cu != [0, 0, 1]:
        # ★up 을 비틀면 OrbitControls 의 '극점' 이 엉뚱한 방향에 생긴다. 사용자가 그쪽을 보는
        #   순간 상하 회전이 **잠긴다**(2026-08-14: 시선이 up 과 나란해져 드래그가 안 먹었다).
        #   화면 배치를 바꾸고 싶으면 **좌표를 강체 회전**해라 — 길이·각이 보존되므로 verify 가
        #   그대로 통과하고, up 은 표준 +z 로 남아 회전이 자연스럽다.
        bad.append(f'cameraUp={cu} — 회전이 잠기는 극점을 만든다. 좌표를 강체 회전해라(주석 참조)')
    shapes = spec.get('shapes')
    if not isinstance(shapes, list) or not shapes:
        bad.append('shapes 가 비었다')
        shapes = []
    for i, s in enumerate(shapes):
        t = s.get('type')
        if t not in vocab:
            bad.append(f'shapes[{i}]: 렌더러가 모르는 type `{t}`')
            continue
        for k in s:
            if k not in vocab[t]:
                bad.append(f'shapes[{i}]({t}): 모르는 속성 `{k}` — 조용히 무시된다')
        for key in ('at', 'from', 'to', 'center', 'origin', 'normal'):
            v = s.get(key)
            if isinstance(v, list) and len(v) != 3:
                bad.append(f'shapes[{i}]({t}).{key}: 성분 {len(v)}개 — 3D 는 세 개여야 한다')
        for v in (s.get('vertices') or []):
            if isinstance(v, list) and len(v) != 3:
                bad.append(f'shapes[{i}]({t}).vertices: 성분 {len(v)}개인 점이 있다')
        # ④ 라벨에 설명 문장이 들어갔는가 — 도형 위 글씨는 **이름·수식**이어야 한다.
        #    ★2026-08-14 검수에서 "H 에서 평면 ABD 에 내린 수선" 같은 문장이 도형을 덮어
        #      정작 봐야 할 입체가 안 보였다. 설명은 note 필드에 쓴다.
        for key in ('label', 'text'):
            v = s.get(key)
            if isinstance(v, str) and _is_prose(v):
                bad.append(f'shapes[{i}]({t}).{key}: 설명 문장이다 — note 로 옮겨라: "{v[:40]}"')
    if deep and e.get('verify'):
        r = subprocess.run([sys.executable, str(RUNNER)], input=e['verify'].encode('utf-8'),
                           capture_output=True, timeout=300)
        out = r.stdout.decode('utf-8', 'replace')
        if 'Traceback' in out or r.returncode != 0:
            bad.append(f'verify 실행 오류: {out.strip().splitlines()[-1] if out.strip() else "출력 없음"}')
        for line in out.splitlines():
            if '[VERIFY FAIL]' in line:
                bad.append(f'verify {line.strip()}')
        if '[VERIFY OK]' not in out:
            bad.append('verify 가 [VERIFY OK] 를 하나도 안 냈다 — 검증하는 척만 한 코드다')
    return bad


def main() -> int:
    deep = '--deep' in sys.argv
    vocab = vocabulary()
    files = sorted(DIR.glob('*.json')) if DIR.exists() else []
    if not files:
        print('ℹ️  등록된 3D 스펙이 없다.')
        return 0
    fails = 0
    for f in files:
        bad = check(f, vocab, deep)
        if bad:
            fails += 1
            print(f'🔴 {f.stem}')
            for b in bad:
                print(f'     {b}')
    if fails:
        print(f'\n{len(files)}건 중 {fails}건 실패')
        return 1
    print(f'✅ 3D 스펙 {len(files)}건 — 렌더러 어휘 일치'
          f'{" · verify 전부 통과" if deep else " (깊은 검사는 --deep)"}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
