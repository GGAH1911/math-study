r"""HWP(.hwp) → 본문 텍스트 + 인라인 LaTeX 수식 추출.

한컴 HWP 5.0 바이너리(OLE 복합문서 + zlib 압축 레코드)를 직접 파싱해, 단락 텍스트와
인라인 수식(EQEDIT)을 **문서 순서대로** 재구성한다. 수식은 hwp_eq2latex 로 LaTeX 변환.
pyhwp/libreoffice 가 수식을 못 뽑던 것을, 수식 명세(revision1.3) 기반으로 직접 해결.

레코드: header uint32 LE = tag(10b) | level(10b) | size(12b); size==0xFFF 면 다음 uint32.
  PARA_TEXT=67  CTRL_HEADER=71(ctrl_id eqed/gso/tbl)  EQEDIT=88
PARA_TEXT 내 코드 11(쌍) = 인라인 객체 마커(8 wchar 블록). objseq(eqed/gso/tbl) 순서로 채움.
"""
from __future__ import annotations
import re
import zlib
import olefile
from hwp_eq2latex import eq2latex

PARA_TEXT, CTRL_HEADER, EQEDIT = 67, 71, 88


def _records(data: bytes):
    i, N = 0, len(data)
    while i + 4 <= N:
        h = int.from_bytes(data[i:i + 4], 'little'); i += 4
        tag = h & 0x3FF; size = (h >> 20) & 0xFFF
        if size == 0xFFF:
            size = int.from_bytes(data[i:i + 4], 'little'); i += 4
        yield tag, data[i:i + size]
        i += size


def _decode_para(body: bytes) -> str:
    """PARA_TEXT → 텍스트(인라인 객체는 \x00OBJ\x00 마커)."""
    out = []; i = 0; N = len(body)
    while i + 1 < N:
        c = int.from_bytes(body[i:i + 2], 'little')
        if c in (1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 19, 20):  # 인라인/확장 컨트롤(8 wchar)
            if c == 11:
                out.append('\x00OBJ\x00')
            i += 16
        elif c in (10, 13):
            out.append('\n'); i += 2
        elif c == 9:
            out.append(' '); i += 2
        elif c < 32:
            i += 2
        else:
            out.append(chr(c)); i += 2
    return ''.join(out)


def _eq_from_eqedit(body: bytes) -> str:
    """EQEDIT 레코드 → 수식 스크립트.

    구조(명세): UINT32 속성, UINT16 길이, WCHAR[길이] 스크립트, … 폰트/버전 메타.
    구조 파싱이 선행 잡음 바이트·메타 혼입을 근본 제거.
    """
    try:
        if len(body) >= 6:
            ln = int.from_bytes(body[4:6], 'little')
            if 0 < ln <= (len(body) - 6) // 2:
                script = body[6:6 + ln * 2].decode('utf-16le', 'replace')
                if script.strip():
                    return script
    except Exception:
        pass
    # 폴백: 통 디코드 후 메타 제외 스캔
    s = body.decode('utf-16le', 'replace')
    parts = [p.strip() for p in s.split('\x00') if p.strip()]
    cand = [p for p in parts if not re.search(r'Version|hwpEQ|HYhwp|Equation\s*Font', p, re.I)]
    for p in cand:
        if re.search(r'over|sqrt|root|sum|int|left|right|times|cases|lim|\^|_', p, re.I):
            return p
    return cand[0] if cand else ''


def parse_hwp(path: str) -> str:
    """HWP → 전체 본문(인라인 수식 = $LaTeX$, 그림=[그림], 표=[표])."""
    ole = olefile.OleFileIO(path)
    comp = bool(ole.openstream('FileHeader').read()[36] & 1)
    paras, objseq, eqs = [], [], []
    for s in sorted('/'.join(x) for x in ole.listdir() if x[0] == 'BodyText'):
        raw = ole.openstream(s).read()
        data = zlib.decompress(raw, -15) if comp else raw
        for tag, body in _records(data):
            if tag == PARA_TEXT:
                paras.append(_decode_para(body))
            elif tag == CTRL_HEADER and len(body) >= 4:
                cid = body[0:4][::-1].decode('latin1', 'replace')
                if cid in ('eqed', 'gso ', 'tbl '):
                    objseq.append(cid)
            elif tag == EQEDIT:
                eqs.append(eq2latex(_eq_from_eqedit(body)))
    ole.close()
    oi = [0]; ei = [0]

    def fill(_m):
        t = objseq[oi[0]] if oi[0] < len(objseq) else 'eqed'
        oi[0] += 1
        if t == 'eqed':
            e = eqs[ei[0]] if ei[0] < len(eqs) else ''
            ei[0] += 1
            return f'${e}$' if e else ''
        return '[그림]' if t == 'gso ' else '[표]'

    text = '\n'.join(paras)
    text = re.sub('\x00OBJ\x00', fill, text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text


if __name__ == '__main__':
    import sys
    txt = parse_hwp(sys.argv[1])
    # 회차 헤더 + 문제 번호 분포
    rounds = re.findall(r'20\d\d학년도\s*\d+월[^\n]{0,30}', txt)
    print('회차 헤더:', rounds[:8])
    print('총 길이:', len(txt))
    print(txt[:1200])
