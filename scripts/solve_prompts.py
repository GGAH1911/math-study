# 솔버 캐시 프롬프트 빌더 — build_solution_cache 에서 분리(자족적, param 만 사용). 동작 무변.
from __future__ import annotations


def build_prompt(img_paths: list[str], fmt: str, meta: str, hint: str = '', with_verifier: bool = True) -> str:
    use_verifier = with_verifier   # 솔버는 객관식·단답 모두 필수(유사문제 재생성+정답표 독립검증). 구제모드만 생략
    lines = ['  "answer": <네가 푼 보기 번호 1-5 정수>,' if fmt == 'choice'
             else '  "answer": <네가 푼 단답형 정답 정수(0-999)>,']
    lines.append('  "answer_value": "<최종 답의 값만, 설명·중간식 없이. 예: -7/64 또는 163>",')
    lines.append('  "score": <2|3|4 정수, 이미지 상단의 "[N점]" 배점 그대로>,')
    if use_verifier:
        lines.append('  "solution_steps": ["<핵심 단계 1, 한국어, KaTeX $...$ 허용>", "..."],')
        if fmt == 'choice':   # ④ 객관식: 보기번호가 아니라 실제 답값을 풀이로 검증 (CANDIDATE 강제 X)
            lines.append('  "verifier_python": "<자기완결 파이썬 검산기. **보기 번호가 아니라 이 문제의 실제 답 값**을 이미지에 주어진 원래 함수·방정식·조건으로 직접 풀이해 구하고(sympy·numpy, 근사식·하드코딩 금지, 원식 그대로; 필요시 수치 root-find), 그 값이 문제 조건을 만족하면 정확히 \'VERIFY_PASS\', 아니면 \'VERIFY_FAIL\' print. 파일·네트워크·os 금지, 수학 라이브러리만.>"')
        else:
            lines.append('  "verifier_python": "<자기완결 파이썬 검산기. **맨 윗줄에 `CANDIDATE = <네가 구한 답>` 정의**. 그 아래에서 **이미지에 주어진 원래 함수·방정식·조건을 코드로 표현**하고 CANDIDATE 를 역대입/대조해 만족하는지 sympy·numpy 로 확인(근사식·중간식 금지, 원식 그대로; 필요시 수치 root-find). \'if CANDIDATE==답\' 같은 자기비교 금지 — CANDIDATE 를 틀린 값으로 바꾸면 반드시 VERIFY_FAIL 이 나오게. 통과 시 정확히 \'VERIFY_PASS\', 아니면 \'VERIFY_FAIL\' print. 파일·네트워크·os 금지, 수학 라이브러리만.>"')
    else:
        lines.append('  "solution_steps": ["<핵심 단계 1, 한국어, KaTeX $...$ 허용>", "..."]')
    body = '\n'.join(lines)
    if len(img_paths) == 1:
        img_intro = f"문제 이미지: {img_paths[0]}\n{meta}\n\n위 이미지를 Read 로 연 뒤"
    else:
        listing = '\n'.join(f'    {i + 1}. {p}' for i, p in enumerate(img_paths))
        img_intro = (
            f"문제 이미지 — 세로로 길어 위→아래 {len(img_paths)}장으로 나눴고 경계가 약간 겹칩니다:\n"
            f"{listing}\n{meta}\n\n"
            f"위 {len(img_paths)}장을 **모두** Read 로 열어 **하나의 문제로 이어 붙여** 본 뒤"
        )
    return f"""{img_intro} 문제를 **스스로 끝까지 풀어라. 정답은 주어지지 않는다.** **마지막 메시지에 오직 하나의 ```json 블록**만 출력 (설명 산문 금지):

```json
{{
{body}
}}
```{(chr(10) + chr(10) + hint) if hint else ''}"""


def build_text_prompt(problem_text: str, fmt: str, meta: str) -> str:
    lines = ['  "answer": <네가 푼 보기 번호 1-5 정수>,' if fmt == 'choice'
             else '  "answer": <네가 푼 단답형 정답 정수(0-999)>,']
    lines.append('  "answer_value": "<최종 답의 값만, 설명·중간식 없이. 예: -7/64 또는 163>",')
    lines.append('  "score": <2|3|4 정수, 배점이 보이면 그대로, 없으면 4>,')
    lines.append('  "solution_steps": ["<핵심 단계 1, 한국어, KaTeX $...$ 허용>", "..."],')
    if fmt == 'choice':   # ④ 객관식: 보기번호가 아니라 실제 답값을 풀이로 검증 (CANDIDATE 강제 X)
        lines.append('  "verifier_python": "<자기완결 파이썬 검산기. **보기 번호가 아니라 이 문제의 실제 답 값**을 문제에 주어진 원래 함수·방정식·조건으로 직접 풀이해 구하고(sympy·numpy, 근사식·하드코딩 금지, 원식 그대로; 필요시 수치 root-find), 그 값이 문제 조건을 만족하면 정확히 \'VERIFY_PASS\', 아니면 \'VERIFY_FAIL\' print. 파일·네트워크·os 금지, 수학 라이브러리만.>"')
    else:
        lines.append('  "verifier_python": "<자기완결 파이썬 검산기. **맨 윗줄에 `CANDIDATE = <네가 구한 답>` 정의**. 그 아래에서 **문제에 주어진 원래 함수·방정식·조건을 코드로 표현**하고 CANDIDATE 를 역대입/대조해 만족하는지 sympy·numpy 로 확인(근사식·중간식 금지, 원식 그대로; 필요시 수치 root-find). \'if CANDIDATE==답\' 같은 자기비교 금지 — CANDIDATE 를 틀린 값으로 바꾸면 반드시 VERIFY_FAIL 이 나오게. 통과 시 정확히 \'VERIFY_PASS\', 아니면 \'VERIFY_FAIL\' print. 파일·네트워크·os 금지, 수학 라이브러리만.>"')
    body = '\n'.join(lines)
    return (f"다음은 한국 수능 수학 문제다 (텍스트):\n\n{problem_text}\n\n{meta}\n\n"
            f"위 문제를 **스스로 끝까지 풀어라. 정답은 주어지지 않는다.** "
            f"**마지막 메시지에 오직 하나의 ```json 블록**만 출력 (설명 산문 금지):\n\n"
            f"```json\n{{\n{body}\n}}\n```")


def build_openbook_prompt(problem_text: str, gold: str, fmt: str, steps_text: str = '',
                          lite: bool = False) -> str:
    """정답과 검증된 풀이단계를 주고, 원래 식에 역대입하는 검산기를 쓰게 하는 프롬프트.
    lite=True: 전체 재구성이 어려운 킬러용 — steps의 *핵심 관계식 하나*만 검증(게이트는 그대로)."""
    kind = '객관식(보기 번호 1-5)' if fmt == 'choice' else '단답형(정수)'
    steps_block = (f"\n[검증된 풀이 단계 — 이 논리를 코드로 옮겨라]\n{steps_text}\n"
                   if steps_text else '')
    if lite:
        return (
            f"다음은 한국 수능 수학 킬러 문제다 (텍스트):\n\n{problem_text}\n\n"
            f"이 문제의 정답은 이미 검증돼 있다: **정답 = {gold}** ({kind}).{steps_block}\n"
            f"문제 전체를 코드로 재구성하기 어렵다. 대신 **solution_steps 에서 정답이 만족하는 "
            f"'핵심 등식·관계식' 단 하나**를 골라(예: 최종 단계의 'M-m=7/2', 'f(3)=31', "
            f"'aₙ³tan²(…)→25π²' 같은 관계) 그 관계식만 sympy 로 표현하고 CANDIDATE 를 대입해 "
            f"성립하는지 확인하는 *경량* 검산기를 작성하라.\n\n"
            f"규칙:\n"
            f"1. 맨 윗줄: CANDIDATE = {gold}\n"
            f"2. steps 의 핵심 관계식을 sympy(Eq/solve/subs/simplify/isclose)로 표현하고 CANDIDATE 대입.\n"
            f"3. 'if CANDIDATE == {gold}' 자기비교 금지 — 반드시 steps 의 수식 관계로 판정. "
            f"CANDIDATE 를 틀린 값으로 바꾸면 VERIFY_FAIL 이 나와야 한다.\n"
            f"4. 통과 시 정확히 VERIFY_PASS, 아니면 VERIFY_FAIL print. sympy·numpy·math·fractions 만.\n\n"
            f"**마지막 메시지에 오직 하나의 ```json 블록**:\n"
            f"```json\n{{\n  \"verifier_python\": \"<경량 검산기 (CANDIDATE 로 시작)>\"\n}}\n```"
        )
    if fmt == 'choice':                          # 객관식: 보기번호 대신 실제 답값을 풀이로 검증 (2021 방식)
        return (
            f"다음은 한국 수능 수학 5지선다 문제다 (텍스트):\n\n{problem_text}\n\n"
            f"정답 보기번호 = {gold}.{steps_block}\n"
            f"임무: 보기번호가 아니라 **이 문제의 실제 답 값**을 풀이로 직접 구하고, 그 값이 원래 식·조건을 "
            f"만족하는지 확인하는 자기완결 파이썬 검산기를 작성하라.\n\n"
            f"규칙:\n"
            f"1. 'CANDIDATE = 보기번호' 같은 변수를 쓰지 마라. 문제의 원래 식·조건을 sympy/numpy 로 코드화하고 "
            f"풀이로 답을 도출하라 (근사식·중간식 하드코딩 금지, 원래 식 그대로).\n"
            f"2. 도출한 답이 문제 조건을 만족하면 정확히 'VERIFY_PASS', 아니면 'VERIFY_FAIL' 를 print.\n"
            f"3. sympy·numpy·math·fractions 만, 파일·os·네트워크 금지.\n\n"
            f"**마지막 메시지에 오직 하나의 ```json 블록**만 출력:\n"
            f"```json\n{{\n  \"verifier_python\": \"<자기완결 파이썬 검산기>\"\n}}\n```"
        )
    return (
        f"다음은 한국 수능 수학 문제다 (텍스트):\n\n{problem_text}\n\n"
        f"이 문제의 정답은 이미 검증돼 있다: **정답 = {gold}** ({kind}).{steps_block}\n"
        f"임무: 이 정답이 옳음을 **원래 문제의 식·조건으로 직접 확인**하는 자기완결 파이썬 검산기를 작성하라.\n\n"
        f"엄격 규칙:\n"
        f"1. 맨 윗줄에 검사할 답을 정확히 이렇게 정의: CANDIDATE = {gold}\n"
        f"2. 그 아래에서 **문제에 주어진 원래 함수·방정식·조건을 코드로 인코딩**하고, CANDIDATE 를 그 식에 "
        f"대입/대조해 만족하는지 sympy·numpy·math·fractions 로 확인하라. 문제에 나온 계수·상수를 코드에 그대로 써라.\n"
        f"3. 'if CANDIDATE == {gold}' 처럼 답을 자기 자신(또는 같은 상수)과 직접 비교하지 마라. "
        f"반드시 원래 식을 풀거나 대입한 결과로 판정하라.\n"
        f"4. CANDIDATE 를 틀린 값으로 바꾸면 반드시 VERIFY_FAIL 이 나오게, 진짜 문제 조건에 의존시켜라.\n"
        f"5. 통과 시 정확히 VERIFY_PASS, 아니면 VERIFY_FAIL 를 print. 파일·네트워크·os 금지(sympy·numpy·math·fractions 만).\n\n"
        f"**마지막 메시지에 오직 하나의 ```json 블록**만 출력 (산문 금지):\n"
        f"```json\n{{\n  \"verifier_python\": \"<자기완결 파이썬 검산기 (CANDIDATE 로 시작)>\"\n}}\n```"
    )


def build_promote_prompt(problem_text: str, gold: str, fmt: str, steps_text: str, lite_code: str) -> str:
    steps_block = f"\n[검증된 풀이 단계]\n{steps_text}\n" if steps_text else ''
    return (
        f"한국 수능 수학 문제:\n\n{problem_text}\n\n이 문제의 정답은 검증돼 있다: 정답 = {gold}.{steps_block}\n"
        f"아래는 *최종 관계식만* 확인하는 경량 검산기다(작동 확인됨). 이걸 **유사문제 재생성이 가능한 "
        f"완전 파라미터 솔버**로 확장하라:\n```python\n{lite_code}\n```\n\n"
        f"요구사항:\n"
        f"1. `def solve(<문제계수1>=<원값1>, <문제계수2>=<원값2>, ...):` — **문제 본문의 계수·각도·조건을 "
        f"키워드 인자(기본값=원문제 값)로 노출**하라.\n"
        f"2. solve 내부에서 그 인자들로부터 정답을 **forward 계산**(sympy)해 return 하라. 경량 관계식을 최종 단계로 써도 된다.\n"
        f"3. 맨 아래: `CANDIDATE = {gold}` 그리고 `print('VERIFY_PASS' if solve()==CANDIDATE else 'VERIFY_FAIL')`.\n"
        f"4. **계수를 바꾸면 답이 바뀌어야 한다** — 답을 코드에 박지 말고 계수에서 계산하라(이게 유사문제 재생성의 핵심).\n"
        f"5. sympy·numpy·math·fractions 만. 파일·os·네트워크 금지.\n\n"
        f"**마지막 메시지에 오직 하나의 ```json 블록**:\n"
        f"```json\n{{\n  \"verifier_python\": \"<def solve(...) 포함 완전 파라미터 솔버>\"\n}}\n```"
    )
