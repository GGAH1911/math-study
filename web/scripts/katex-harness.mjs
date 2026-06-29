// 채팅 KaTeX 렌더 파이프라인 충실 재현 하네스 — 실제 katex + ChatPanel 의 실제 함수.
// 목적: malformed LLM 수식이 제대로 렌더되는지 + 정상 식 회귀 없는지 "관측".
// 실행: node web/scripts/katex-harness.mjs   (cwd=repo root 또는 web/)
import katex from 'katex';
import { normalizeKatex, KATEX_STRICT, KATEX_ERROR_COLOR, renderMathSegments } from '../src/lib/katex-normalize.mjs';

// ───────── ChatPanel 함수 충실 복제 (현재 코드 그대로) ─────────
function normalizeLlmMarkup(text) {
  let out = text
    .replace(/<\s*\/?\s*(?:strong|b)\s*>/gi, '**')
    .replace(/<\s*\/?\s*(?:em|i)\s*>/gi, '*');
  const isProse = (inner) =>
    /[가-힣]/.test(inner.replace(/\\(?:text|mathrm|mathbf|mathsf|operatorname)\s*\{[^{}]*\}/g, ''));
  // $$…$$ 블록 보호 후 산문-strip (실제 ChatPanel 과 동일)
  const blocks = [];
  out = out.replace(/\$\$(?:(?!\$\$)[\s\S])*?\$\$/g, (m) => { blocks.push(m); return `KTXBLK${blocks.length - 1}KTXEND`; });
  out = out.replace(/\$\$([^$]+?)\$\$/g, (m, inner) => (isProse(inner) ? inner : m));
  out = out.replace(/\$([^$\n]+?)\$/g, (m, inner) => (isProse(inner) ? inner : m));
  out = out.replace(/KTXBLK(\d+)KTXEND/g, (_, i) => blocks[+i]);
  return out;
}

const escape = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const inline = (s) =>
  s.replace(/\[([^\]\n]+?)\]\(([^)\s]+?)\)/g, (m, txt, url) => {
    if (!/^(\/|https?:\/\/)/.test(url) || /["']/.test(url)) return m;
    const label = txt.includes('/') && !/\s/.test(txt) ? (txt.split('/').pop() || txt).replace(/_/g, ' ') : txt;
    return `<a href="${url}">${label}</a>`;
  })
    .replace(/\*\*([^\n*]+?)\*\*/g, '<strong>$1</strong>')
    .replace(/`([^`\n]+?)`/g, '<code>$1</code>')
    .replace(/(^|[^*\w])\*(?=\S)([^\n*]+?)(?<=\S)\*(?!\*)/g, '$1<em>$2</em>');

// 표 파서 (간이): | a | b | \n |---| 형태를 <table> 로. 셀에 inline(escape) 적용.
function tryParseTable(para, cellFn) {
  const lines = para.split('\n').filter((l) => l.trim());
  if (lines.length < 2 || !lines.every((l) => l.trim().startsWith('|'))) return null;
  const rows = lines.map((l) => l.trim().replace(/^\||\|$/g, '').split('|').map((c) => c.trim()));
  const body = rows.filter((r) => !r.every((c) => /^[-:\s]*$/.test(c)));
  const tr = (cells, tag) => '<tr>' + cells.map((c) => `<${tag}>${cellFn(c)}</${tag}>`).join('') + '</tr>';
  return '<table>' + tr(body[0], 'th') + body.slice(1).map((r) => tr(r, 'td')).join('') + '</table>';
}

function renderMarkdown(text) {
  text = normalizeLlmMarkup(text);
  const parts = [];
  const tokens = text.split(/(```[\s\S]*?```)/);
  for (const tok of tokens) {
    if (!tok) continue;
    if (tok.startsWith('```')) { parts.push(`<pre>${escape(tok)}</pre>`); continue; }
    const paras = tok.split(/\n{2,}/);
    for (const para of paras) {
      if (!para.trim()) continue;
      const tableHtml = tryParseTable(para, (cell) => inline(escape(cell)));
      if (tableHtml) { parts.push(tableHtml); continue; }
      const lines = para.split('\n');
      const hasHeading = lines.some((l) => /^\s{0,3}#{1,6}\s+\S/.test(l));
      if (hasHeading) {
        let buf = [];
        const flush = () => { if (buf.length) { parts.push(`<p>${inline(escape(buf.join('\n'))).replace(/\n/g, '<br/>')}</p>`); buf = []; } };
        for (const line of lines) {
          const hm = line.match(/^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$/);
          if (hm) { flush(); const tag = hm[1].length <= 2 ? 'h4' : 'h5'; parts.push(`<${tag}>${inline(escape(hm[2]))}</${tag}>`); }
          else buf.push(line);
        }
        flush();
        continue;
      }
      parts.push(`<p>${inline(escape(para)).replace(/\n/g, '<br/>')}</p>`);
    }
  }
  return parts.join('');
}

function decodeEntities(s) {
  return s
    .replace(/&amp;(le|ge)=?;/g, (_, k) => (k === 'le' ? '\\le' : '\\ge'))
    .replace(/&le;=?/g, '\\le').replace(/&ge;=?/g, '\\ge')
    .replace(/&lt;=/g, '\\le').replace(/&gt;=/g, '\\ge')
    .replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
}

const MATH_TOKEN = String.raw`(?:[A-Za-z0-9\-+*/^=,.]+|\\[A-Za-z]+(?:\{[^}]*\})*|\||\(|\)|\{|\})`;
const ENTITY_OP = String.raw`(?:&lt;|&gt;|&le;|&ge;|&amp;le;|&amp;ge;)=?`;
const INEQUALITY_RUN = new RegExp(`(${MATH_TOKEN}(?:\\s+${MATH_TOKEN})*)(\\s*${ENTITY_OP}\\s*${MATH_TOKEN}(?:\\s+${MATH_TOKEN})*)+`, 'g');
const LATEX_CMD_RUN = /(\\[A-Za-z]+(?:\{[^}]{0,80}\})*(?:\s+(?![A-Za-z]{3,}(?![A-Za-z]))[A-Za-z0-9\-+*/^=.,()|\\{}]+)*)/g;

function recoverBareMath(html) {
  // 골든도 본체와 동일하게 렌더된 KaTeX 스팬(<annotation> 의 raw LaTeX)을 마스킹 후 복구
  //   (안 하면 annotation 안 \frac 등을 또 렌더해 오염 → 드래그 인용 깨짐). renderMathSegments 와 패리티.
  const SENT = String.fromCharCode(1);
  const masks = [];
  {
    let masked = '', i = 0;
    while (i < html.length) {
      const s = html.indexOf('<span class="katex', i);
      if (s === -1) { masked += html.slice(i); break; }
      masked += html.slice(i, s);
      const re = /<span\b|<\/span>/g; re.lastIndex = s;
      let depth = 0, end = html.length, m;
      while ((m = re.exec(html))) {
        if (m[0] === '</span>') { if (--depth === 0) { end = m.index + m[0].length; break; } }
        else depth++;
      }
      masks.push(html.slice(s, end));
      masked += `${SENT}${masks.length - 1}${SENT}`;
      i = end;
    }
    html = masked;
  }
  html = html.replace(INEQUALITY_RUN, (full) => {
    if (/[<>]/.test(full)) return full;
    try { return katex.renderToString(decodeEntities(full), { displayMode: false, throwOnError: true, strict: KATEX_STRICT }); } catch { return full; }
  });
  html = html.replace(LATEX_CMD_RUN, (full) => {
    if (/[<>]/.test(full)) return full;
    const tex = decodeEntities(full).trim();
    if (tex.length < 2) return full;
    try { return katex.renderToString(tex, { displayMode: false, throwOnError: true, strict: KATEX_STRICT }); } catch { return full; }
  });
  html = html.replace(new RegExp(`${SENT}(\\d+)${SENT}`, 'g'), (_, n) => masks[+n]);
  return html;
}

function applyKatex(html) {
  html = html.replace(/\$\$((?:<br\s*\/?>|[^<>])+?)\$\$/g, (_, tex) => {
    try { return katex.renderToString(normalizeKatex(decodeEntities(tex.replace(/<br\s*\/?>/g, '\n'))), { displayMode: true, throwOnError: true, strict: KATEX_STRICT, errorColor: KATEX_ERROR_COLOR }); } catch { return _; }
  });
  html = html.replace(/\$((?:\\text\{[^{}]*\}|[^\n$<>])+?)\$/g, (_, tex) => {
    try { return katex.renderToString(normalizeKatex(decodeEntities(tex)), { displayMode: false, throwOnError: true, strict: KATEX_STRICT, errorColor: KATEX_ERROR_COLOR }); } catch { return _; }
  });
  html = recoverBareMath(html);
  return html;
}

function render(text) { return applyKatex(renderMarkdown(text)); }

// ───────── 관측: 렌더된 katex span 수 vs 남은 raw 수식 ─────────
function observe(name, text, expectRendered) {
  const html = render(text);
  const rendered = (html.match(/class="katex/g) || []).length;
  // 남은 raw 수식 신호: 본문에 살아있는 $ 또는 raw \text/\frac (katex span 밖)
  const strippedSpans = html.replace(/<span class="katex[\s\S]*?<\/span><\/span>/g, '');
  const rawDollar = (strippedSpans.match(/\$/g) || []).length;
  const rawCmd = (strippedSpans.match(/\\(?:text|frac|nP|nC|sqrt)/g) || []).length;
  const ok = rendered >= expectRendered && rawDollar === 0 && rawCmd === 0;
  console.log(`${ok ? '✅' : '❌'} ${name}: 렌더 ${rendered}개 (기대≥${expectRendered}), raw$ ${rawDollar}, rawCmd ${rawCmd}`);
  if (!ok) {
    console.log('   IN :', text.slice(0, 120).replace(/\n/g, '⏎'));
    console.log('   OUT:', strippedSpans.replace(/<[^>]+>/g, '').slice(0, 160).replace(/\n/g, '⏎'));
  }
  return ok;
}

const CASES = [
  // [이름, 입력, 기대 렌더 수] — DB 에서 가져온 실제 Haiku 출력 포함
  ['DB실제 정의(다중 $섬+따옴표)', '$$_nP_r = \\text{"$n$개의 서로 다른 것 중에서 $r$개를 선택해서 일렬로(순서대로) 배열하는 경우의 수"}$$', 1],
  ['DB실제 공식', '$$_nP_r = n \\times (n-1) \\times (n-2) \\times \\cdots \\times (n-r+1) = \\frac{n!}{(n-r)!}$$', 1],
  ['곱슬따옴표 변환', '$$\\text{"$n$개의 것"}$$', 1],  // " → “ ” 확인 (아래 별도 검사)
  ['표: 순열기호 4셀', '| 상황 | 예제 | 순열 기호 |\n|---|---|---|\n| 줄 세우기 | "5명" | $_5P_5$ |\n| 자리 | "6명" | $_6P_3$ |\n| 역할 | "10명" | $_10P_3$ |\n| 숫자 | "0123" | $_4P_3$ |', 4],
  ['실제 정의+표 한 메시지', '순열이란:\n$$_nP_r = \\text{"$n$개의 서로 다른 것 중에서 $r$개를 배열하는 경우의 수"}$$\n\n| 상황 | 순열 기호 |\n|---|---|\n| 줄 세우기 | $_5P_5$ |\n| 자리 | $_6P_3$ |', 3],
  ['정상 inline', '값은 $_5P_5$ 이고 $_6C_2 = 15$ 이다', 2],
  ['정상 display', '$$x^2 + y^2 = r^2$$', 1],
  ['정상 \\text 한글', '$\\text{공통배수}=30$ 이다', 1],
  ['정상 \\text 비한글 math', '$f(x) = \\text{이고 } x^2$', 1],
  ['부등식', '범위는 $-2 < x < 2$ 이다', 1],
  ['헤딩+수식', '## 순열\n공식은 $_nP_r$ 이다', 1],
  // 회귀: \text{} 안 수학 관계 유니코드(≠ 등)는 text mode hard-throw → 통째 raw 였음.
  ['\\text 안 ≠ 관계기호', '$$\\boxed{\\begin{align}&\\Rightarrow \\text{분자 ≠ 1인 각도} \\\\ &30°, 45° \\end{align}}$$', 1],
];

let pass = 0;
for (const [n, t, e] of CASES) if (observe(n, t, e)) pass++;
console.log(`\n${pass}/${CASES.length} 통과`);

// ───────── SSOT 회귀 게이트: 통합 renderMathSegments 가 (구) applyKatex 와 바이트 동일? ─────────
// applyKatex(위 골든 = 구 ChatPanel 코드 충실복제) vs renderMathSegments(html,{htmlInput,recoverBare}).
console.log('\n=== SSOT 패리티 (통합 함수 vs 골든 applyKatex, 바이트 동일) ===');
let parityPass = 0;
for (const [n, t] of CASES) {
  const base = renderMarkdown(t);
  const golden = applyKatex(base);
  const unified = renderMathSegments(base, katex, { htmlInput: true, recoverBare: true });
  const same = golden === unified;
  if (same) parityPass++;
  else {
    console.log(`❌ ${n}: 불일치`);
    // 첫 차이 지점만 출력
    let i = 0; while (i < golden.length && golden[i] === unified[i]) i++;
    console.log('   golden:', golden.slice(Math.max(0, i - 30), i + 30).replace(/\n/g, '⏎'));
    console.log('   unified:', unified.slice(Math.max(0, i - 30), i + 30).replace(/\n/g, '⏎'));
  }
}
console.log(`${parityPass === CASES.length ? '✅' : '❌'} 패리티 ${parityPass}/${CASES.length} 바이트 동일`);

process.exit(pass === CASES.length && parityPass === CASES.length ? 0 : 1);
