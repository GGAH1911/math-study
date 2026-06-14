"""로제타 자동 확장 — 신규 회차에 hancom_rosetta.json 에 없는 PUA 가 나오면,
그 글리프를 렌더해 비전(claude_p)으로 식별하고 사전에 append.

인제스트가 새 PDF 를 처리하기 전에 extend(pdf) 를 호출하면, 미식별 글리프가 자동 등록되어
이후 디코드가 100% 커버된다. (사장님 지시: 신규 인제스트에서 로제타에 없는 게 나오면 LLM 개입.)
"""
from __future__ import annotations
import os
import re
import json
import subprocess
from pathlib import Path

import pikepdf
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables._c_m_a_p import cmap_format_4
from PIL import Image, ImageDraw, ImageFont

import hancom_decode as H

_DICT_PATH = Path(__file__).resolve().parent.parent / "hancom_rosetta.json"


def unmapped_codes(pdf) -> list[int]:
    """PDF 텍스트레이어의 PUA 중 현재 사전에 없는 코드."""
    try:
        raw = subprocess.run(['pdftotext', '-raw', str(pdf), '-'],
                             capture_output=True, text=True, timeout=90).stdout
    except Exception:
        return []
    return sorted({ord(c) for c in raw if 0xE000 <= ord(c) <= 0xF8FF and ord(c) not in H.ROSETTA})


def _parse_tou(raw: str) -> dict:
    m = {}
    for blk in re.findall(r'beginbfchar(.*?)endbfchar', raw, re.S):
        for a, b in re.findall(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', blk):
            m[int(a, 16)] = int(b, 16)
    for blk in re.findall(r'beginbfrange(.*?)endbfrange', raw, re.S):
        for a, b, c in re.findall(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', blk):
            a, b, c = int(a, 16), int(b, 16), int(c, 16)
            for k in range(a, b + 1):
                m[k] = c + (k - a)
    return m


def render_unmapped(pdf, codes, out_png='/tmp/rosetta_new_glyphs.png') -> tuple[str | None, list[int]]:
    """codes 의 글리프를 PDF 임베드 폰트에서 찾아 라벨된 시트로 렌더. (png경로, 렌더된 코드들)."""
    need = set(codes); found = {}; ti = 0
    p = pikepdf.open(str(pdf))
    for obj in p.objects:
        if not need:
            break
        try:
            if str(obj.get('/Subtype', '')) != '/Type0':
                continue
            tu = obj.get('/ToUnicode')
            if tu is None:
                continue
            tou = _parse_tou(bytes(tu.read_bytes()).decode('latin1'))
            hit = need & set(tou.values())
            if not hit:
                continue
            desc = obj.get('/DescendantFonts')[0]; fd = desc.get('/FontDescriptor')
            ff = fd.get('/FontFile2') if fd is not None else None
            if ff is None:
                continue
            path = f'/tmp/rex_{ti}.ttf'; open(path, 'wb').write(bytes(ff.read_bytes())); ti += 1
            font = TTFont(path); go = font.getGlyphOrder(); n = len(go)
            sub = cmap_format_4(4); sub.platformID = 3; sub.platEncID = 1; sub.language = 0
            sub.cmap = {0x3041 + i: go[i] for i in range(n) if go[i] != '.notdef'}
            ct = newTable('cmap'); ct.tableVersion = 0; ct.tables = [sub]; font['cmap'] = ct; font.save(path)
            pua2cid = {v: k for k, v in tou.items()}
            for code in list(hit):
                cid = pua2cid.get(code)
                if cid is not None and cid < n and code not in found:
                    found[code] = (path, cid); need.discard(code)
        except Exception:
            pass
    if not found:
        return None, []
    items = sorted(found.items()); cols = 8
    rows = max(1, (len(items) + cols - 1) // cols); cw, ch = 135, 108
    img = Image.new('RGB', (cols * cw, rows * ch), 'white'); dr = ImageDraw.Draw(img)
    sm = ImageFont.load_default(); fc = {}
    for idx, (code, (path, cid)) in enumerate(items):
        fc.setdefault(path, ImageFont.truetype(path, 44))
        x = (idx % cols) * cw; y = (idx // cols) * ch
        dr.rectangle([x, y, x + cw - 2, y + ch - 2], outline='#ccc')
        dr.text((x + 3, y + 2), f'{code:04X}', fill='red', font=sm)
        try:
            dr.text((x + 36, y + 36), chr(0x3041 + cid), fill='black', font=fc[path])
        except Exception:
            pass
    img.save(out_png)
    return out_png, [c for c, _ in items]


def extend(pdf, log=print) -> dict:
    """신규 PUA 자동 식별 → 사전 append. 반환: 새로 추가된 {code_hex: symbol}."""
    codes = unmapped_codes(pdf)
    if not codes:
        return {}
    log(f'[rosetta_extend] 미식별 PUA {len(codes)}종: {[f"{c:04X}" for c in codes[:12]]}')
    png, rendered = render_unmapped(pdf, codes)
    if not png:
        log('[rosetta_extend] 글리프 렌더 실패 — 수동 확인 필요')
        return {}
    try:
        from ingest_round import claude_p  # 프로젝트 비전 호출(claude CLI)
    except Exception as e:
        log(f'[rosetta_extend] claude_p import 실패: {e}')
        return {}
    cur = json.load(open(_DICT_PATH, encoding='utf-8'))
    existing = ''.join(sorted({v for v in cur.values() if len(v) == 1}))
    # ★collapse 방지: 구조 글리프(가로줄/합/곱/적분)를 빼기·그리스문자와 섞지 않게 비전에 명시.
    # (E046 마이너스/E06D 바, E067 합/E096 Σ 같은 정보손실 충돌의 재발 차단.)
    user = (f"첨부 이미지 {os.path.abspath(png)} 에 수식 글리프들이 격자로 있다. 각 칸 상단 빨간 라벨은 "
            f"유니코드 PUA 코드(hex 4자리), 그 아래가 실제 글리프다. 각 코드가 어떤 수학기호/문자인지 식별하라.\n"
            f"★구조 글리프는 모양이 비슷해도 반드시 구분(정보 손실 방지):\n"
            f"- 수평 가로줄(분수선·근호 윗줄·선분/벡터 윗줄)이면 반드시 '‾' 로 — 빼기 '-' 와 절대 같게 쓰지 말 것.\n"
            f"- 빼기/음수 기호만 '-'.\n"
            f"- 합 연산자(∑, 큰 기호·상하한 받음)는 '∑', 그리스 대문자 시그마(문자)는 'Σ'.\n"
            f"- 곱 연산자(∏)는 '∏', 그리스 대문자 파이(문자)는 'Π'. 큰 적분기호는 '∫'.\n"
            f"이미 사전에 있는 1글자 기호: {existing}\n"
            f'JSON 객체 하나만 출력: {{"E0XX": "기호", ...}}. 모르면 생략. 설명·코드펜스 금지.')
    out = claude_p("너는 한컴 수식 글리프 식별기다. 오직 JSON 만 출력.", user,
                   model='sonnet', max_turns=1, add_dir=os.path.dirname(os.path.abspath(png)), timeout=120)
    if not out:
        return {}
    out = re.sub(r'^```(?:json)?\s*|\s*```$', '', out.strip(), flags=re.M)
    m = re.search(r'\{.*\}', out, re.S)
    if not m:
        return {}
    try:
        mapping = json.loads(m.group(0))
    except Exception:
        return {}
    # 사전 append + 저장 — 구조기호 중복(collapse) 가드.
    _STRUCT = {'-', '‾', '∑', 'Σ', '∏', 'Π', '∫'}
    existing_syms = set(cur.values())
    added = {}
    for k, v in mapping.items():
        kk = k.upper().replace('U+', '').strip()
        if re.fullmatch(r'[0-9A-F]{4,5}', kk) and v and kk not in cur:
            if v in existing_syms and v in _STRUCT:
                log(f'[rosetta_extend] ⚠ collapse 주의: {kk}→{v!r} (이미 다른 코드가 쓰는 구조기호). '
                    f'정말 같은 글리프인지 재확인 — 구조가 다르면 별개 기호로(가로줄=‾, 합=∑ 등).')
            cur[kk] = v; added[kk] = v
    if added:
        json.dump({k: cur[k] for k in sorted(cur)}, open(_DICT_PATH, 'w'),
                  ensure_ascii=False, indent=1)
        H.ROSETTA = H.load_rosetta()  # 메모리 갱신
        log(f'[rosetta_extend] 사전 확장 {len(added)}종: {added}')
    return added


if __name__ == '__main__':
    import sys
    print(extend(sys.argv[1]))
