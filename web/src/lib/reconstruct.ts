// 문제 재구성 렌더러 — searchable_text(한글 산문 + LaTeX/유니코드 수식 혼합, 구분자 없음)를
// KaTeX HTML 로. 한글/원문자(①②·ㄱㄴㄷ)는 텍스트, 나머지(ASCII·수식기호·LaTeX)는 수식으로
// 분리해 렌더. 순수 수식 줄은 display(가운데). 선택지(①~⑤)는 별도 행으로 정렬.
import katex from 'katex';

const strictFn = (code: string): 'ignore' | 'warn' =>
  code === 'unicodeTextInMathMode' || code === 'unknownSymbol' ? 'ignore' : 'warn';

function isTextChar(cp: number): boolean {
  return (
    (cp >= 0xac00 && cp <= 0xd7a3) || // 한글 음절
    (cp >= 0x3130 && cp <= 0x318f) || // 한글 호환 자모 (ㄱㄴㄷ)
    (cp >= 0x2460 && cp <= 0x24ff) || // 원문자 ①②③
    (cp >= 0x2150 && cp <= 0x218f) || // 로마 숫자 ⅰⅱⅲ + 분수기호 (KaTeX 메트릭 없음)
    (cp >= 0x3000 && cp <= 0x303f) || // CJK 구두점
    (cp >= 0xff00 && cp <= 0xffef) // 전각
  );
}

function esc(s: string): string {
  return s.replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' })[c] as string);
}

// 큰 연산자(lim/∑/∏)는 inline 모드에서 첨자가 우측에 붙는다 → \limits 로 첨자를 연산자 아래로 강제.
// (∫는 제외: inline 적분 상·하한은 옆에 붙는 게 표준)
function fixBigOps(s: string): string {
  return s
    .replace(/\\lim(?![a-zA-Z])/g, '\\lim\\limits')
    .replace(/\\(sum|prod)(?![a-zA-Z])/g, '\\$1\\limits');
}

// 함수명(ln/sin/cos/log 등)에 \ 접두 — 안 그러면 KaTeX가 l·n·x 변수 italic 으로 렌더.
// decode가 "lnx"·"sinx" 처럼 변수에 붙여놔도 매칭(replace가 함수명만 치환, 변수 x는 남김).
// 이미 \ 붙은 건 lookbehind 로 skip. 긴 이름(arcsin/sinh) 먼저.
function fixFunctions(s: string): string {
  return s.replace(
    /(?<!\\)(arcsin|arccos|arctan|sinh|cosh|tanh|sin|cos|tan|sec|csc|cot|log|ln)/g,
    '\\$1 ',
  );
}

// 닫히지 않은 중괄호 보충(연립방정식 { 등 일반 '{' 가 } 없이 끝나 KaTeX 불균형 에러 → 보충).
function balanceBraces(t: string): string {
  let depth = 0;
  for (let i = 0; i < t.length; i++) {
    if (i > 0 && t[i - 1] === '\\') continue; // 이스케이프 \{ \} 무시
    if (t[i] === '{') depth++;
    else if (t[i] === '}') depth = Math.max(0, depth - 1);
  }
  return depth > 0 ? t + '}'.repeat(depth) : t;
}

function km(m: string, display = false): string {
  const t = fixFunctions(fixBigOps(m.trim()));
  if (!t) return esc(m);
  // 빨강 KaTeX 에러(katex-error)를 절대 내지 않도록: 원본 → 중괄호 보충 순으로 시도,
  // 둘 다 파싱 실패하면 평문(esc)으로. (부분 렌더의 빨강보다 깔끔. 진짜 깨진 건 decode 후속.)
  for (const cand of [t, balanceBraces(t)]) {
    try {
      return katex.renderToString(cand, { throwOnError: true, strict: strictFn, displayMode: display });
    } catch {
      /* 다음 후보 시도 */
    }
  }
  return esc(m);
}

const hasHangul = (s: string) => /[가-힣ㄱ-ㅎㅏ-ㅣ]/.test(s);
const CHOICE_RE = /[①②③④⑤⑥⑦⑧⑨⑩]/;

// 한 조각을 텍스트/수식 세그먼트로 분리해 인라인 렌더
const isKo = (ch: string) => /[가-힣ㄱ-ㅎㅏ-ㅣ]/.test(ch);

// depth(중괄호 {} + \begin/\end 환경) 인식 인라인 렌더.
// 핵심: 수식 구성 '안'(depth>0)의 한글은 \text{}로 감싸 그대로 수식에 둔다 — 그래야
// 집합 {x|x는 자연수}·\begin{cases}…경우…\end{cases} 처럼 중괄호/환경 안에 한글이 있어도
// 구성이 안 깨지고 KaTeX 가 렌더한다. depth 0의 한글은 평문(text)으로 분리.
function renderInline(s: string): string {
  const segs: Array<[boolean | 'sp' | 'blank', string]> = [];
  let cur = '';
  let curType: boolean | null = null; // true=text, false=math
  let textRun = ''; // 수식 안에서 모으는 한글(+공백) → \text{}
  let d = 0; // 수식 깊이
  const flushTR = () => {
    if (textRun) {
      cur += `\\text{${textRun.replace(/[{}\\]/g, '').trim()}}`;
      textRun = '';
    }
  };
  const flush = () => {
    flushTR();
    if (cur) {
      segs.push([curType ?? true, cur]);
      cur = '';
      curType = null;
    }
  };
  for (let i = 0; i < s.length; i++) {
    const ch = s[i];
    const escd = i > 0 && s[i - 1] === '\\'; // 이스케이프 \{ \}
    const isBegin = ch === '\\' && s.startsWith('\\begin', i);
    const isEnd = ch === '\\' && s.startsWith('\\end', i);
    const bump = () => {
      if (ch === '{' && !escd) d++;
      else if (ch === '}' && !escd) d = Math.max(0, d - 1);
      else if (isBegin) d++;
      else if (isEnd) d = Math.max(0, d - 1);
    };
    if (d > 0) {
      // 수식 구성 안: 전부 math 세그먼트로. 한글(+공백)은 \text 로 모은다.
      if (curType !== false) {
        flush();
        curType = false;
      }
      if (isKo(ch) || (textRun && ch === ' ')) {
        textRun += ch;
        continue;
      }
      flushTR();
      cur += ch;
      bump();
      continue;
    }
    // depth 0: (가)~(하) = 빈칸추론 답칸 → 네모 박스(빈칸). 인라인("f(15) = (가)")도 박스로.
    const blank = s.slice(i).match(/^[(（]\s*([가-하])\s*[)）]/);
    if (blank) {
      flush();
      segs.push(['blank', blank[1]]);
      i += blank[0].length - 1;
      continue;
    }
    // depth 0: 한글=text, 공백=리터럴 보존, 그 외=math.
    if (ch === ' ') {
      flush();
      segs.push(['sp', ' ']);
      continue;
    }
    const t = isTextChar(ch.codePointAt(0)!);
    if (curType === null) curType = t;
    else if (t !== curType) {
      flush();
      curType = t;
    }
    cur += ch;
    if (!t) bump();
  }
  flush();
  return segs
    .map(([t, x]) => (t === 'sp' ? ' ' : t === 'blank' ? `<span class="recon-blank">(${esc(x)})</span>` : t ? esc(x) : km(x)))
    .join('');
}

export interface ReconOpts {
  figureHtml?: string;
  /** 도형을 본문 몇 번째 줄 뒤에 넣을지 (0 = 맨 위). 미지정이면 본문 끝(선택지 앞). */
  figureAfterLine?: number;
  /** 다중 그림: 각 {html, afterLine}. 있으면 figureHtml/figureAfterLine 대신 사용(여러 그림 각 위치). */
  figures?: Array<{ html: string; afterLine?: number }>;
  /** 표(셀 2D 배열들) — 본문 {{TABLEn}} 자리에 HTML <table>로 렌더. */
  tables?: string[][][];
}

// 표(셀 2D 배열) → HTML <table>. 첫 행=헤더, 셀 값은 renderInline(수식/한글 혼합).
function renderTable(rows: string[][]): string {
  if (!rows || !rows.length) return '';
  const cell = (s: string, tag: string) => `<${tag}>${renderInline(s ?? '')}</${tag}>`;
  const head = `<tr>${rows[0].map((c) => cell(c, 'th')).join('')}</tr>`;
  const bodyR = rows.slice(1).map((r) => `<tr>${r.map((c) => cell(c, 'td')).join('')}</tr>`).join('');
  return `<table class="recon-table"><thead>${head}</thead><tbody>${bodyR}</tbody></table>`;
}

export function renderReconstruct(text: string, opts: ReconOpts = {}): string {
  if (!text || !text.trim()) return '';
  // 번호·배점은 recon-head(헤더)에 이미 있으니 본문서 제거(중복 방지): 선행 "11." + "[3점]".
  text = text.replace(/^\s*\d{1,2}\.\s*/, '').replace(/\[\s*\d+\s*점\s*\]/g, '');
  // 방향A: 이 렌더러는 구분자($) 없는 형식(한글=텍스트·수식=math 자동 분리)이 SSOT다.
  // Gemini 교정이 LaTeX 관례로 $...$ 델리미터를 넣어도 여기서 제거해 무해화(아무리 새도 안 깨짐).
  text = text.replace(/\$/g, '');
  // 파이프(|)만 있는 줄 = cases 중괄호 연장선/HWP 레이아웃 잔재(예: 27번 cases 위 '| |')라 제외.
  // 절댓값 |x| 등 의미있는 파이프는 내용이 같이 있어 이 필터(공백+파이프만)에 안 걸린다.
  const lines = text.split('\n').filter((l) => l.trim() && !/^[\s|‖∣｜]+$/.test(l))
    .flatMap((l) => l.split(/\s+(?=\([가-하]\)\s)/))  // 한 줄에 붙은 (가)(나)(다) 조건을 각 줄로
    .flatMap((l) => {  // 조건 줄 끝에 붙은 질문("…의 값은?")은 박스 밖으로 떼어냄
      const m = l.match(/^(\([가-하]\)\s.*?다\.)\s+(.+(?:값은|값을|구하|얼마|\?).*)$/);
      return m ? [m[1], m[2]] : [l];
    });
  const body: string[] = [];
  const choiceLines: string[] = [];
  for (const l of lines) {
    const mi = l.search(CHOICE_RE);
    if (mi > 0) {
      // 한 줄에 본문+선택지 혼재(LLM 한줄요약 형식) → 첫 마커 앞=본문, 마커부터=선택지로 분리.
      // (안 그러면 본문이 nowrap 선택지 span 에 갇혀 오버플로우.)
      const pre = l.slice(0, mi).trim();
      if (pre) body.push(pre);
      choiceLines.push(l.slice(mi));
    } else if (mi === 0) {
      choiceLines.push(l);
    } else {
      body.push(l);
    }
  }

  // 테두리 박스 영역들 — 빈칸추론·<보기>·(가)(나)(다) 조건. [start, end) 범위 목록.
  const boxes: Array<[number, number]> = [];
  // 1) 빈칸추론: "다음은 … 과정이다" 다음 줄 ~ "위의 … 알맞은/값은" 전.
  const introIdx = body.findIndex((l) => /과정이다|구하는 과정/.test(l));
  if (introIdx >= 0) {
    const s = introIdx + 1;
    const ci = body.findIndex((l, i) => i >= s && /^\s*위의|알맞은\s*(수|값|식|것)|에 알맞은/.test(l));
    const e = ci > s ? ci : body.length;
    if (s < e) boxes.push([s, e]);
  }
  // 2) <보기>: 독립된 "보 기" 헤더 줄 ~ 본문 끝(선택지는 이미 분리됨).
  const bogiIdx = body.findIndex((l) => /^\s*[<〈\[]?\s*보\s*기\s*[>〉\]]?\s*$/.test(l));
  if (bogiIdx >= 0) boxes.push([bogiIdx, body.length]);
  // 3) 조건 (가)(나)(다)… 또는 불렛(•/∙) 목록: 첫 마커 ~ 질문/결론/새 섹션("다음은/과정이다/위의") 전.
  const condStart = body.findIndex((l) => /^\s*[(（]\s*가\s*[)）]/.test(l) || /^\s*[•∙·▪◦●]/.test(l));
  if (condStart >= 0) {
    let e = condStart + 1;
    while (
      e < body.length &&
      !/구하시오|값은|개수는|경우의 수는|얼마|\[\s*\d+\s*점\s*\]|\?|다음은|과정이다|^\s*위의/.test(body[e])
    )
      e++;
    if (e > condStart) boxes.push([condStart, e]);
  }
  const boxOpen = new Set(boxes.map((b) => b[0]));
  const boxClose = new Set(boxes.map((b) => b[1]));

  // 불렛(•/∙) 항목은 좌측정렬 + 불렛 뒤 공백 보장 (decode가 공백 누락하고 순수수식이면
  // recon-disp 로 가운데정렬되던 것 교정 — 불렛은 목록이라 좌측정렬이 맞음).
  const BULLET_RE = /^\s*([•∙·▪◦●])\s*/;
  const renderLine = (line: string) => {
    const bm = line.match(BULLET_RE);
    if (bm) {
      return `<div class="recon-line recon-bullet">${esc(bm[1])} ${renderInline(line.replace(BULLET_RE, ''))}</div>`;
    }
    return hasHangul(line)
      ? `<div class="recon-line">${renderInline(line)}</div>`
      : `<div class="recon-line recon-disp">${km(line, true)}</div>`;
  };

  // 도형 삽입: figures 배열 우선, 없으면 figureHtml(단일) 호환.
  const figList = (opts.figures && opts.figures.length)
    ? opts.figures
    : (opts.figureHtml ? [{ html: opts.figureHtml, afterLine: opts.figureAfterLine }] : []);
  // placeholder 모드: 본문에 {{FIGn}} 마커가 있으면 그 자리에 figList[n] 삽입(위치=추출 시 PDF 레이아웃으로 결정).
  const PH_RE = /^\s*\{\{FIG(\d+)\}\}\s*$/;
  const placeholderIdx = new Set<number>();
  for (const l of body) { const m = l.match(PH_RE); if (m) placeholderIdx.add(+m[1]); }
  // placeholder 안 쓰인 도형만 afterLine(미지정=본문 끝)으로 배치.
  const clampLine = (n?: number) => Math.max(0, Math.min(body.length, typeof n === 'number' ? n : body.length));
  const figByLine = new Map<number, string[]>();
  figList.forEach((f, idx) => { if (placeholderIdx.has(idx)) return; const a = clampLine(f.afterLine); if (!figByLine.has(a)) figByLine.set(a, []); figByLine.get(a)!.push(f.html); });

  let html = '';
  if (figByLine.has(0)) html += figByLine.get(0)!.join('');
  for (let i = 0; i < body.length; i++) {
    const pm = body[i].match(PH_RE);
    if (pm) { const fi = +pm[1]; if (figList[fi]) html += figList[fi].html; continue; }  // {{FIGn}} → 그 자리에 도형
    const tm = body[i].match(/^\s*\{\{TABLE(\d+)\}\}\s*$/);
    if (tm) { const ti = +tm[1]; if (opts.tables?.[ti]) html += renderTable(opts.tables[ti]); continue; }  // {{TABLEn}} → 표
    if (boxOpen.has(i)) html += '<div class="recon-box">';
    html += renderLine(body[i]);
    if (boxClose.has(i + 1)) html += '</div>';
    if (figByLine.has(i + 1)) html += figByLine.get(i + 1)!.join('');
  }

  if (choiceLines.length) {
    const parts = choiceLines
      .join(' ')
      .split(/(?=[①②③④⑤⑥⑦⑧⑨⑩])/)
      .map((s) => s.trim())
      .filter(Boolean);
    const items = parts
      .map((p) => {
        const mk = p.match(/^([①②③④⑤⑥⑦⑧⑨⑩])\s*([\s\S]*)$/);
        const num = mk ? mk[1] : '';
        const rest = mk ? mk[2] : p;
        return `<span class="recon-choice"><span class="recon-cnum">${num}</span>${rest ? renderInline(rest) : ''}</span>`;
      })
      .join('');
    html += `<div class="recon-choices">${items}</div>`;
  }
  return html;
}
