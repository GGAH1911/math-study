#!/usr/bin/env python3
# cleanup_adhoc_concepts.py — 문제 frontmatter 의 concepts 에서 'ad-hoc 슬러그'(개념 그래프에
#   파일이 없는 즉석 개념명)를 정리한다. 사장님 지침: 최대한 기존 개념 노드에 연결, 새 개념은 최소.
#   ① _canonical_concept 로 정규화 매칭되면 그 정식 슬러그(nested 경로)로 치환(띄어쓰기/조사 차이 흡수).
#   ② 정규화로 못 잡으면 제거(그 문제는 unit + 다른 정상 개념을 이미 동반 → 정보손실 0, 사전검증됨).
#   결정적·LLM 0. dry-run 기본, --apply 로 실제 수정.
import sys, glob, re, os
sys.path.insert(0, 'scripts/ingest_kice')
import ingest_v2 as IV

APPLY = '--apply' in sys.argv
ROOT = str(IV.ROOT)

# 의미 매핑: 정규화(_canonical_concept)로는 못 잡지만 의미상 기존 정식 개념에 흡수되는 ad-hoc.
#   사장님 지침 "최대한 기존 노드에 연결" — 단순 제거 대신 의미가 가까운 기존 개념으로 치환.
#   (대상 개념이 실제 존재하는지 적용 전 검증함.)
SEMANTIC_MAP = {
    '거리_조건': '거리_조건과_도형', '거리_비': '거리와_비율',
    '자기닮음': '도형의_닮음', '자기_유사_도형': '도형의_닮음', '닮음과_자기유사성': '도형의_닮음',
    '벡터의_합과_크기': '벡터의_덧셈', '매개변수와_최댓값': '평면벡터', '좌표계_활용': '평면벡터',
    '교점_구하기': '교점', '교점의조건': '교점', '약수의_개수_함수': '약수의_개수',
    '정삼각형_단면': '회전체_부피', '정적분_조건과_미분의_역관계': '미적분의_기본정리',
    '적분_조건의_활용': '정적분의_활용', '조건을_만족하는_값': '정적분의_활용',
    '삼각형_조건': '경우의_수', '조합으로_3개_선택': '조합', '일직선상_점_제외': '조합',
    '그래프_색칠': '경우의_수', '치환을_통한_부등식': '삼각함수_부등식',
    '극한_조건으로_함수_결정': '함수의_극한', '함수_그래프의_사분면_분석': '함수와_그래프',
    '좌표_활용': '이차곡선', '축_위의_점': '공간좌표', '항합': '거듭제곱근',
    '구간별_정의함수': '구간별_함수', '명제의_진위_판정': '명제와_조건',
    '역산': '대입법', '특수값_대입': '대입법', '∞)': '극한',
    '축척_인자': '도형의_닮음',
    # '정의'(이차곡선 문제, 동반개념 충분) 는 제거로 둔다(의미 모호).
}

# 개념 잎 이름 → nested 슬러그(유일할 때만). 치환 시 정확한 경로 복원용.
_leaf2nested, _leafcnt = {}, {}
for p in glob.glob(f'{ROOT}/docs/concepts/**/*.md', recursive=True):
    rel = os.path.relpath(p, f'{ROOT}/docs/concepts')[:-3]
    leaf = os.path.basename(p)[:-3]
    _leafcnt[leaf] = _leafcnt.get(leaf, 0) + 1
for p in glob.glob(f'{ROOT}/docs/concepts/**/*.md', recursive=True):
    rel = os.path.relpath(p, f'{ROOT}/docs/concepts')[:-3]
    leaf = os.path.basename(p)[:-3]
    if _leafcnt[leaf] == 1:
        _leaf2nested[leaf] = rel
nested_leaves = set(_leafcnt)

stat = {'subbed': 0, 'removed': 0, 'files': 0}
sub_detail, rem_detail = {}, {}

for f in glob.glob(f'{ROOT}/docs/problems/**/*.md', recursive=True):
    t = open(f, encoding='utf-8').read()
    m = re.search(r'^concepts: \[(.*?)\]', t, re.M)
    if not m:
        continue
    refs = re.findall(r'docs/concepts/([^,\]]+)\.md', m.group(1))
    new_refs, changed = [], False
    for c in refs:
        leaf = c.split('/')[-1]
        if leaf in nested_leaves:
            new_refs.append(c)                       # 이미 정상(경로 그대로 유지)
            continue
        canon = IV._canonical_concept(leaf)          # ① 정규화 매칭(띄어쓰기/조사)
        target = None
        if canon != leaf and canon in nested_leaves:
            target = canon
        elif leaf in SEMANTIC_MAP and SEMANTIC_MAP[leaf] in nested_leaves:
            target = SEMANTIC_MAP[leaf]              # ② 의미 매핑(기존 개념 흡수)
        if target:
            new_refs.append(_leaf2nested.get(target, target))   # nested 경로로 치환
            changed = True
            stat['subbed'] += 1
            sub_detail[leaf] = target
        else:
            changed = True                           # ③ 제거(동반 정상개념+unit 유지)
            stat['removed'] += 1
            rem_detail[leaf] = rem_detail.get(leaf, 0) + 1
    if changed:
        # 중복 제거(순서 보존)
        seen, dedup = set(), []
        for c in new_refs:
            if c not in seen:
                seen.add(c); dedup.append(c)
        new_line = 'concepts: [' + ', '.join(f'docs/concepts/{c}.md' for c in dedup) + ']'
        t2 = t[:m.start()] + new_line + t[m.end():]
        stat['files'] += 1
        if APPLY:
            open(f, 'w', encoding='utf-8').write(t2)

print(f"{'[적용]' if APPLY else '[dry-run]'} 수정파일 {stat['files']} · 치환 {stat['subbed']} · 제거 {stat['removed']}")
print(f"\n[치환 {len(sub_detail)}종 ad-hoc → 정식]")
for k, v in sorted(sub_detail.items()):
    print(f"  {k} → {v}")
print(f"\n[제거 {len(rem_detail)}종 (문제는 unit+동반개념 유지)]")
for k, n in sorted(rem_detail.items()):
    print(f"  {k} ({n}문제)")
