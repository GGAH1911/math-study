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
      // 수식 안 빈칸 (가)~(하)도 \boxed 로 박스 처리 — d=0 의 recon-blank 와 시각 통일(\frac{(나)}{…} 같은 수식 내부 답칸).
      const bmIn = s.slice(i).match(/^[(（]\s*([가-하])\s*[)）]/);
      if (bmIn) {
        flushTR();
        cur += `\\boxed{\\text{(${bmIn[1]})}}`;
        i += bmIn[0].length - 1;
        continue;
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
    // depth 0: 한글=text, 그 외=math.
    if (ch === ' ') {
      // 수식 세그먼트 중 공백은 수식에 그대로 유지 — \left\{ … \right\} 처럼 공백 포함 수식이 공백마다
      // 쪼개져 단독 \left/\right 가 짝 없이 KaTeX 깨지던 것 방지. 텍스트 사이 공백만 리터럴 보존.
      if (curType === false) { cur += ' '; continue; }
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
  /** 인라인 도형(임베드 객체 src) — 본문 줄 중간 {{INLn}} 자리에 인라인 <img>로 렌더(블록 {{FIGn}}과 별개). */
  inlineFigures?: string[];
  /** figures 의 이미지 src(인덱스 일치) — {{FIGn}} 이 문장 중간에 있으면 그 자리에 인라인 <img>로 렌더('○○ 모양의 도형' 인라인 기호). */
  figureSrcs?: string[];
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
    .flatMap((l) => l.split(/(?<=\.)\s+(?=\([가-하]\)\s)/))  // ★원본 줄바꿈 SSOT: 문장끝(.) 다음의 조건 "(나)"만 분리(레거시 한줄-cram 보조). 인라인/수식 빈칸("개수는 (가) 이고","×(가)")은 분리X — 줄바꿈 보존된 콘텐츠엔 no-op
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

  // 테두리 박스 영역들 [start, end). 박스는 오직 {{BOXn_START}}/{{BOXn_END}} 마커로만 판정한다
  //   (extract_figures.detect_boxes 가 PDF 실제 테두리=벡터선으로 삽입·box_backfill 가 기존 코퍼스 백필).
  //   ★텍스트 휴리스틱(과정이다/조건 (가)/보기 헤더 추론) 폐기 — 문구 열거 유지보수 불가 + 오탐. 교정 시 마커가 결정적으로 붙는다.
  const boxes: Array<[number, number]> = [];
  const skipLines = new Set<number>();   // 마커 줄 자체는 렌더 제외
  const boxStartRe = /^\s*\{\{BOX(\d+)_START\}\}\s*$/;
  const boxEndRe = /^\s*\{\{BOX(\d+)_END\}\}\s*$/;
  const starts = new Map<string, number>();
  body.forEach((l, i) => {
    const ms = l.match(boxStartRe);
    if (ms) { starts.set(ms[1], i); skipLines.add(i); return; }
    const me = l.match(boxEndRe);
    if (me) { skipLines.add(i); const s = starts.get(me[1]); if (s !== undefined) boxes.push([s + 1, i]); }
  });
  const boxOpen = new Set(boxes.map((b) => b[0]));
  const boxClose = new Set(boxes.map((b) => b[1]));

  // 불렛(•/∙) 항목은 좌측정렬 + 불렛 뒤 공백 보장 (decode가 공백 누락하고 순수수식이면
  // recon-disp 로 가운데정렬되던 것 교정 — 불렛은 목록이라 좌측정렬이 맞음).
  const BULLET_RE = /^\s*([•∙·▪◦●])\s*/;
  const inlFigs = opts.inlineFigures ?? [];
  const figSrcs = opts.figureSrcs ?? [];
  // 문장 중간 {{FIGn}} 직후가 '모양/꼴/공통부분' = 본문에 박히는 인라인 도형 기호('○○ 모양의 도형').
  // → 그 자리에 인라인 <img>로 렌더 + 블록 배치에서 제외. ('NN. {{FIG}} 그림과 같이…' 블록그림은 신호 없어 제외 안 됨.)
  const inlineFigIdx = new Set<number>();
  for (const m of text.matchAll(/\{\{FIG(\d+)\}\}\s*(?:모양|꼴|공통부분)/g)) inlineFigIdx.add(+m[1]);
  // 본문 줄 중간 {{INLn}}/{{FIGn}}(인라인 기호) → 인라인 <img>(텍스트 흐름 안). 마커 기준으로 쪼개 사이사이 renderInline.
  const renderInlineWithFig = (s: string): string => {
    if (!/\{\{(?:INL|FIG)\d+\}\}/.test(s)) return renderInline(s);
    return s
      .split(/(\{\{(?:INL|FIG)\d+\}\})/)
      .map((p) => {
        const mi = p.match(/^\{\{INL(\d+)\}\}$/);
        if (mi) {
          const src = inlFigs[+mi[1]];
          return src ? `<img src="${src}" alt="도형" class="recon-inl" style="height:1.3em;vertical-align:-0.28em;display:inline" />` : '';
        }
        const mf = p.match(/^\{\{FIG(\d+)\}\}$/);
        if (mf) {
          const src = figSrcs[+mf[1]];
          return src && inlineFigIdx.has(+mf[1])
            ? `<img src="${src}" alt="도형" class="recon-inl" style="height:1.5em;vertical-align:-0.4em;display:inline" />`
            : '';   // 인라인 신호 없는 {{FIGn}}(블록 도형)은 그 자리에선 제거(블록으로 따로 배치됨)
        }
        return p ? renderInline(p) : '';
      })
      .join('');
  };
  const renderLine = (line: string) => {
    const bm = line.match(BULLET_RE);
    if (bm) {
      return `<div class="recon-line recon-bullet">${esc(bm[1])} ${renderInlineWithFig(line.replace(BULLET_RE, ''))}</div>`;
    }
    // 도출 줄(= < > ≤ ≥ 로 시작 + 빈칸 외 한글 없음): display 수식 + 빈칸 \boxed + 좌측정렬(recon-deriv)로 통일.
    //   빈칸 든 줄(인라인·소형 좌측)과 순수식 줄(가운데·대형)이 따로 놀던 = 체인 정렬·크기 불일치 해결.
    //   독립 식·(*) 같은 비-관계 시작 줄은 가운데(recon-disp) 유지.
    const noBlank = line.replace(/[(（]\s*[가-하]\s*[)）]/g, '');
    if (/^\s*[=<>≤≥≠]/.test(line.trim()) && !hasHangul(noBlank)) {
      const boxed = line.replace(/[(（]\s*([가-하])\s*[)）]/g, '\\boxed{\\text{($1)}}');
      return `<div class="recon-line recon-disp recon-deriv">${km(boxed, true)}</div>`;
    }
    return hasHangul(line)
      ? `<div class="recon-line">${renderInlineWithFig(line)}</div>`
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
  figList.forEach((f, idx) => { if (placeholderIdx.has(idx) || inlineFigIdx.has(idx)) return; const a = clampLine(f.afterLine); if (!figByLine.has(a)) figByLine.set(a, []); figByLine.get(a)!.push(f.html); });

  let html = '';
  if (figByLine.has(0)) html += figByLine.get(0)!.join('');
  for (let i = 0; i < body.length; i++) {
    if (skipLines.has(i)) continue;   // {{BOXn_START/END}} 마커 줄 자체는 출력 안 함(박스 경계 표시용)
    // ★ box open/close 는 placeholder 줄에도 적용해야 div 균형이 맞는다. 빈칸추론 박스의 open 인덱스가
    //   {{FIGn}} 줄("과정이다" 바로 다음이 도형)이면, continue 로 건너뛸 경우 open <div> 만 누락되고
    //   close </div> 는 실행돼 </div> 가 1개 과다 → 부모 article 조기 종료 → 레이아웃 붕괴(16번 사례).
    if (boxOpen.has(i)) html += '<div class="recon-box">';
    const pm = body[i].match(PH_RE);
    const tm = body[i].match(/^\s*\{\{TABLE(\d+)\}\}\s*$/);
    if (pm) { const fi = +pm[1]; if (figList[fi]) html += figList[fi].html; }          // {{FIGn}} → 그 자리에 도형
    else if (tm) { const ti = +tm[1]; if (opts.tables?.[ti]) html += renderTable(opts.tables[ti]); }  // {{TABLEn}} → 표
    else html += renderLine(body[i]);
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
