#!/usr/bin/env python3
"""기출문제 답안 검증·정정.

golden 정답 PDF를 파싱해서 우리 docs/problems/<회차>_<과목>_NN.md의
answer 필드와 비교, 불일치/누락만 자동 정정.

Usage:
    python3 scripts/verify_answers.py <golden_pdf> <round_prefix> [--apply]

예:
    python3 scripts/verify_answers.py /tmp/golden/2025_고3_5월_정답.pdf 2025_고3_5월모의고사
    # → diff만 출력 (dry-run, --apply 안 붙이면)
    python3 scripts/verify_answers.py /tmp/golden/2025_고3_5월_정답.pdf 2025_고3_5월모의고사 --apply
    # → 실제 patch + verified-rounds.json 업데이트

답안 PDF 형식 가정:
  "공통 (1번 ~ 22번)" 헤더 → 번호와 답(①~⑤ 또는 숫자) 토큰 교대
  "선택과목: 기하/미적분/확률과 통계 (23번 ~ 30번)" 헤더 → 동일
"""
import sys, re, subprocess, json
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parent.parent
PROBLEMS_DIR = REPO_ROOT / 'docs' / 'problems'
VERIFIED_JSON = REPO_ROOT / 'web' / 'src' / 'data' / 'verified-rounds.json'

SEL_MAP = {'①': '1', '②': '2', '③': '3', '④': '4', '⑤': '5'}


def parse_answer_pdf(pdf_path: Path) -> dict[str, dict[int, str]]:
    """PDF → {subject: {number: answer_str}}"""
    text = subprocess.run(
        ['pdftotext', str(pdf_path), '-'],
        capture_output=True, text=True, check=True,
    ).stdout

    headers: list[tuple[int, str]] = []
    for m in re.finditer(r'(공통\s*\([^)]+\)|선택과목[:\s]*[가-힣\s]+?\s*\([^)]+\))', text):
        name = m.group(0)
        if '공통' in name:
            sub = '공통'
        elif '기하' in name:
            sub = '기하'
        elif '미적분' in name:
            sub = '미적분'
        elif '확률' in name or '통계' in name:
            sub = '확률과통계'
        elif '단일' in name:
            sub = '단일'
        else:
            continue
        headers.append((m.start(), sub))
    # 학평/단일과목 fallback: 공통/선택과목 헤더가 없으면 "1번 ~ N번" 헤더 detect
    if not headers:
        m = re.search(r'1번\s*~\s*\d+번', text)
        if m:
            headers.append((m.start(), '단일'))
    # 검정고시 fallback: "문항번호" / "정 답" 표 그리드 — 헤더가 위 패턴과 다름
    if not headers:
        m = re.search(r'정\s*답\s*표', text) or re.search(r'검정고시', text)
        if m:
            headers.append((m.start(), '단일'))
    headers.append((len(text), None))

    subjects: dict[str, dict[int, str]] = {}
    for i in range(len(headers) - 1):
        start, sub = headers[i]
        if sub is None: continue
        end, _ = headers[i + 1]
        body = text[start:end]
        tokens = [t.strip() for t in body.split('\n') if t.strip()]
        # 헤더 토큰 skip
        skip = 0
        for j, tk in enumerate(tokens):
            if any(c in tk for c in ['공통', '선택과목', '~']):
                skip = j + 1
        tokens = tokens[skip:]
        ans: dict[int, str] = {}
        # 검정고시 분리 리스트 형식 detect 우선: body 안에 "문항번호"가
        # 2번 이상 = numbers/answers 분리 PDF. 페어 매칭은 number 토큰의
        # next로 다음 number 토큰을 잡아 false positive를 만들기 때문에
        # 이런 PDF는 페어 매칭 자체를 건너뛴다.
        is_split = body.count('문항번호') >= 2
        if not is_split:
            j = 0
            while j < len(tokens) - 1:
                tk = tokens[j]
                if tk.isascii() and tk.isdigit() and 1 <= int(tk) <= 30:
                    ans[int(tk)] = SEL_MAP.get(tokens[j + 1], tokens[j + 1])
                    j += 2
                else:
                    j += 1
        # 분리 리스트 형식 fallback.
        if is_split or len(ans) < 10:
            ans_list: dict[int, str] = {}
            blocks = re.split(r'문항번호', body)
            for blk in blocks[1:]:
                pivot = blk.find('정답')
                if pivot < 0: continue
                num_part, ans_part = blk[:pivot], blk[pivot+2:]
                nums = re.findall(r'\b(\d+)\b', num_part)
                # 답 토큰: ①②③④⑤ 또는 단답 숫자 — 줄 단위
                a_toks = []
                for line in ans_part.split('\n'):
                    s = line.strip()
                    if not s: continue
                    if s in SEL_MAP: a_toks.append(SEL_MAP[s])
                    elif s.isdigit(): a_toks.append(s)
                    else: break  # 답 영역 끝
                for n, a in zip(nums, a_toks):
                    nn = int(n)
                    if 1 <= nn <= 30:
                        ans_list[nn] = a
            if len(ans_list) > len(ans):
                ans = ans_list
        subjects[sub] = ans
    return subjects


def find_round_file(prefix: str, subject: str, num: int) -> Path | None:
    """우리 데이터에서 해당 회차+과목+번호 파일 찾기."""
    name = f'{prefix}_{subject}_{num:02d}.md'
    p = PROBLEMS_DIR / name
    return p if p.exists() else None


def patch_answer(filepath: Path, new_answer: str) -> tuple[str, bool]:
    """answer 필드 한 줄 교체. (이전값, 변경여부) 반환."""
    text = filepath.read_text(encoding='utf-8')
    m = re.search(r'^(answer:\s*)"?([^"\n]*)"?\s*$', text, re.MULTILINE)
    if not m:
        return ('', False)
    old = m.group(2).strip().strip('"')
    if old == new_answer:
        return (old, False)
    new_text = re.sub(
        r'^answer:\s*"?[^"\n]*"?\s*$',
        f'answer: "{new_answer}"',
        text, count=1, flags=re.MULTILINE,
    )
    filepath.write_text(new_text, encoding='utf-8')
    return (old, True)


def update_verified_rounds(prefix: str, subject_keys: list[str], source: str, corrections: list[str]) -> None:
    """verified-rounds.json에 회차별 entry 추가/업데이트.

    한 PDF가 여러 subject를 포함하므로, 각 subject별 round_key를 등재.
    """
    data = json.loads(VERIFIED_JSON.read_text(encoding='utf-8'))
    existing_keys = {r['key'] for r in data['rounds']}
    today = datetime.now().strftime('%Y-%m-%d')
    for sub in subject_keys:
        key = f'{prefix}_{sub}'
        if key in existing_keys:
            # 기존 entry 갱신 (덮어쓰기)
            for r in data['rounds']:
                if r['key'] == key:
                    r['verified_at'] = today
                    r['source'] = source
                    sub_corrs = [c for c in corrections if c.startswith(f'{sub} ')]
                    if sub_corrs:
                        r['corrected'] = sub_corrs
                    break
        else:
            sub_corrs = [c for c in corrections if c.startswith(f'{sub} ')]
            entry = {'key': key, 'verified_at': today, 'source': source}
            if sub_corrs:
                entry['corrected'] = sub_corrs
            data['rounds'].append(entry)
    VERIFIED_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    pdf = Path(sys.argv[1])
    prefix = sys.argv[2]
    apply = '--apply' in sys.argv

    print(f"=== golden PDF: {pdf} ===")
    print(f"=== round prefix: {prefix} ===")
    print(f"=== mode: {'APPLY (write files)' if apply else 'DRY-RUN (no writes)'} ===")
    print()

    golden = parse_answer_pdf(pdf)
    total = matched = fixed = filled = missing = 0
    corrections: list[str] = []
    seen_subjects: set[str] = set()
    for sub, ans_dict in golden.items():
        seen_subjects.add(sub)
        for num, gold in ans_dict.items():
            fp = find_round_file(prefix, sub, num)
            if not fp:
                missing += 1
                continue
            total += 1
            text = fp.read_text(encoding='utf-8')
            cur = re.search(r'^answer:\s*"?([^"\n]*)"?', text, re.MULTILINE)
            our = cur.group(1).strip().strip('"') if cur else ''
            if our == gold:
                matched += 1; continue
            if apply:
                old, ok = patch_answer(fp, gold)
                if ok:
                    if not our: filled += 1; corrections.append(f'{sub} {num}번 → {gold}')
                    else:       fixed += 1;  corrections.append(f'{sub} {num}번 {our}→{gold}')
                print(f"  {'FILLED' if not our else 'FIXED ':<6}  {sub} {num:>2}번  '{our}' → '{gold}'  {fp.name}")
            else:
                if not our: filled += 1; corrections.append(f'{sub} {num}번 → {gold}')
                else:       fixed += 1;  corrections.append(f'{sub} {num}번 {our}→{gold}')
                print(f"  {'WOULD-FILL' if not our else 'WOULD-FIX  '}  {sub} {num:>2}번  '{our}' → '{gold}'  {fp.name}")

    print()
    print(f"총 비교: {total}  정상: {matched}  불일치 수정: {fixed}  누락 채움: {filled}  파일 없음: {missing}")

    if apply and seen_subjects:
        update_verified_rounds(prefix, sorted(seen_subjects), f"가공 후/(정답).pdf [{pdf.name}]", corrections)
        print(f"\nverified-rounds.json 업데이트 → {sorted(seen_subjects)} (정정 {len(corrections)}건)")


if __name__ == '__main__':
    main()
