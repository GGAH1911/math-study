// 튜터 응답 검증/표시 순수 헬퍼 — ChatPanel send 에서 분리(동작 무변).
//  sanitizeForDisplay: python 검증블록을 표시에서 숨김 · evalArith/findArithErr: 최종 응답의 순수
//  산술 등식 자체검산(CSP 안전 shunting-yard, eval 미사용).

export const sanitizeForDisplay = (s: string) => {
  // ① 닫힌 python block 제거.
  let stripped = s.replace(/```(?:python|py|sympy)[\s\S]*?```/g, '');
  // ② 스트리밍 중 아직 닫는 ``` 가 안 온 미완성 펜스도 잘라낸다. 안 그러면
  //    여는 펜스부터 끝까지 raw python 이 사용자에게 노출됨.
  let hadOpenPy = false;
  const openIdx = stripped.search(/```(?:python|py|sympy)\b/);
  if (openIdx !== -1) {
    stripped = stripped.slice(0, openIdx);
    hadOpenPy = true;
  }
  stripped = stripped.trim();
  const hadPy = hadOpenPy || stripped !== s.trim();
  if (hadPy && stripped.length < 50) return '⚙ 정확한 좌표 계산 중…';
  return stripped;
};

export const evalArith = (e: string): number | null => {
  const toks = e.match(/\d+\.?\d*|[+\-*/()]/g); if (!toks) return null;
  const out: (number | string)[] = []; const ops: string[] = [];
  const prec: Record<string, number> = { '+': 1, '-': 1, '*': 2, '/': 2 };
  for (const t of toks) {
    if (/\d/.test(t)) out.push(parseFloat(t));
    else if (t === '(') ops.push(t);
    else if (t === ')') { while (ops.length && ops[ops.length - 1] !== '(') out.push(ops.pop()!); ops.pop(); }
    else { while (ops.length && (prec[ops[ops.length - 1]] ?? 0) >= prec[t]) out.push(ops.pop()!); ops.push(t); }
  }
  while (ops.length) out.push(ops.pop()!);
  const st: number[] = [];
  for (const t of out) {
    if (typeof t === 'number') st.push(t);
    else { const b = st.pop(); const a = st.pop(); if (a === undefined || b === undefined) return null; st.push(t === '+' ? a + b : t === '-' ? a - b : t === '*' ? a * b : a / b); }
  }
  return st.length === 1 ? st[0] : null;
};
export const findArithErr = (text: string): { expr: string; claimed: string; correct: string } | null => {
  const clean = text.replace(/\\boxed\{([^}]*)\}/g, '$1').replace(/\\cdot|\\times/g, '*').replace(/\\div/g, '/').replace(/\\[a-zA-Z]+|[$]/g, ' ');
  // ★체인 "X = <순수산술> = <숫자>" 에서 두 등호 *사이* 전체 산술을 캡처(앞 등호 필수) — 이전엔
  //   부분 매칭이 "8+12-18+9" 의 "8+" 를 앞 매칭에 뺏겨 "12-18+9=11" 오탐(3≠11)했음. 비체인은 패스(오탐<누락).
  const re = /=\s*([0-9][0-9\s+\-*/().]*?)\s*=\s*(-?[0-9]+(?:\.[0-9]+)?)/g;
  let m: RegExpExecArray | null;
  while ((m = re.exec(clean)) !== null) {
    const e = m[1].replace(/\s/g, '');
    if (!/^[0-9+\-*/().]+$/.test(e) || !/[+\-*/]/.test(e)) continue;
    const v = evalArith(e);
    if (v === null || !isFinite(v)) continue;
    if (Math.abs(v - parseFloat(m[2])) > 1e-6) return { expr: m[1].trim(), claimed: m[2], correct: String(Number.isInteger(v) ? v : +v.toFixed(4)) };
  }
  return null;
};
