// 튜터 채팅의 순수 텍스트/DOM 헬퍼 — ChatPanel 에서 분리(동작 무변).
//  normalizeLlmMarkup: LLM 서식 실수 정규화 · renderMarkdown: 경량 마크다운→HTML(KaTeX 패스스루)
//  serializeFrag/latexFromSelection: 드래그 선택→마크다운+LaTeX 복원(인용용).
import { tryParseTable } from '../markdown';

// Lightweight markdown rendering: bold, italic, code spans, code blocks, paragraphs, KaTeX-aware passthrough.
// Strategy: split paragraphs, wrap code fences as <pre><code>, render inline.
// LLM(특히 Haiku 튜터)이 가끔 서식을 잘못 낸다: ① **굵게** 대신 <strong>/<em> 같은
// 원시 HTML 태그를 쓰고, ② 수식이 아닌 한글 산문을 $…$/$$…$$ 로 감싼다. 그대로 두면
// ①은 escape 돼 literal `<strong>` 이 보이고, ②는 KaTeX 가 실패해 raw `$…$` 가 노출된다
// (예: `$공통: 30 ← <strong>…</strong>$`). renderMarkdown 진입 직전에 마크다운/평문으로
// 정규화해 LLM 이 실수해도 깨지지 않게 한다.
export function normalizeLlmMarkup(text: string): string {
  // ① HTML 강조 태그 → 마크다운 (escape 전이라 안전; <br>/<input> 등은 안 건드림).
  let out = text
    .replace(/<\s*\/?\s*(?:strong|b)\s*>/gi, '**')
    .replace(/<\s*\/?\s*(?:em|i)\s*>/gi, '*');
  // ② \text{…} 밖에 '맨' 한글이 든 $…$ / $$…$$ 는 수식이 아니라 산문 → delimiter 제거.
  //    (\text{공통배수} 처럼 정상 수식 안의 한글은 strip 후 판정해 보존.)
  const isProse = (inner: string): boolean =>
    /[가-힣]/.test(inner.replace(/\\(?:text|mathrm|mathbf|mathsf|operatorname)\s*\{[^{}]*\}/g, ''));
  // ★먼저 $$…$$ display 블록을 통째로 보호한다. 안 그러면 아래 inline 산문-strip 의
  //   `\$([^$\n]+?)\$` 가 여는 `$$` 의 둘째 `$` 를 안쪽 math 섬($n$·$r$)의 `$` 와 잘못 짝지어
  //   (한 칸 오프셋) 섬 사이 한글을 산문으로 오인·delimiter 를 떼어내 \text 수식을 통째로
  //   깨뜨린다. display 내부는 수식이므로 산문-strip 대상이 아니다.
  const blocks: string[] = [];
  out = out.replace(/\$\$(?:(?!\$\$)[\s\S])*?\$\$/g, (m) => {
    blocks.push(m);
    return `KTXBLK${blocks.length - 1}KTXEND`;
  });
  out = out.replace(/\$\$([^$]+?)\$\$/g, (m, inner: string) => (isProse(inner) ? inner : m));
  out = out.replace(/\$([^$\n]+?)\$/g, (m, inner: string) => (isProse(inner) ? inner : m));
  out = out.replace(/KTXBLK(\d+)KTXEND/g, (_, i: string) => blocks[+i]);
  return out;
}

export function renderMarkdown(text: string): string {
  text = normalizeLlmMarkup(text);
  const escape = (s: string) =>
    s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const inline = (s: string) =>
    s
      // 링크 [text](url) → 클릭 가능한 <a>. 보안: 내부경로(/..)·http(s) 만 허용(javascript: 차단),
      // url 에 따옴표 있으면 거부. 가독성: 경로형 텍스트(algebra/math-1/지수와_로그)는 마지막
      // 세그먼트만 + `_`→공백 (지수와 로그). escape 이후 실행 — []()/_ 는 escape 가 안 건드림.
      .replace(/\[([^\]\n]+?)\]\(([^)\s]+?)\)/g, (m, txt: string, url: string) => {
        if (!/^(\/|https?:\/\/)/.test(url) || /["']/.test(url)) return m;
        const label = txt.includes('/') && !/\s/.test(txt)
          ? (txt.split('/').pop() || txt).replace(/_/g, ' ')
          : txt;
        return `<a href="${url}" class="text-[color:var(--color-accent)] underline decoration-dotted underline-offset-2 hover:decoration-solid">${label}</a>`;
      })
      // bold
      .replace(/\*\*([^\n*]+?)\*\*/g, '<strong>$1</strong>')
      // inline code — code 를 italic 보다 먼저 소비해 backtick sympy(`2*3`,`f * g`)의
      // 별표를 <em> 변환에서 보호한다.
      .replace(/`([^`\n]+?)`/g, '<code>$1</code>')
      // italic (single *) — 별표 안쪽 가장자리를 비공백으로 강제(`*x*` 만 매칭).
      // 여는 `*` 앞은 단어문자/별표가 아니어야 하므로 평문 곱셈(`5 * 3`, `2*4`)은
      // 건드리지 않는다.
      .replace(/(^|[^*\w])\*(?=\S)([^\n*]+?)(?<=\S)\*(?!\*)/g, '$1<em>$2</em>');

  const parts: string[] = [];
  // Preserve fenced code blocks
  const tokens = text.split(/(```[\s\S]*?```)/);
  for (const tok of tokens) {
    if (!tok) continue;
    if (tok.startsWith('```')) {
      const m = tok.match(/^```(\w*)\n?([\s\S]*?)```$/);
      const lang = m?.[1] ?? '';
      const rawCode = m?.[2] ?? '';
      // 언어 없는 펜스가 박스드로잉(┌─┐│├┤└┘) ASCII-아트 표면 진짜 HTML 표로 렌더한다 —
      // LLM 이 표를 코드블록에 넣어 평문처럼 보이던 문제. python 등 언어 지정 코드는 그대로.
      if (!lang && /[┌┐└┘├┤┬┴┼─━│┃]/.test(rawCode)) {
        const tbl = tryParseTable(rawCode, (cell) => inline(escape(cell)));
        if (tbl) { parts.push(tbl); continue; }
      }
      parts.push(`<pre data-lang="${lang}"><code>${escape(rawCode)}</code></pre>`);
    } else {
      // Split into paragraphs by blank line
      const paras = tok.split(/\n{2,}/);
      for (const para of paras) {
        if (!para.trim()) continue;
        // 표 detect — escape + inline은 셀 단위로 적용. 표가 paragraph 전체를
        // 차지하는 경우에만 매칭 (혼합 텍스트는 null 반환 → 기존 처리).
        const tableHtml = tryParseTable(para, (cell) => inline(escape(cell)));
        if (tableHtml) {
          parts.push(tableHtml);
          continue;
        }
        // ATX 헤딩(`#`~`######`) 지원 — 라인 단위. 헤딩 줄은 <h_>, 나머지 연속 줄은 <p>.
        // LLM 튜터가 `## 제목` 을 쓰면 리터럴 `##` 로 노출되던 것을 방지. h1·h2 는 페이지
        // 제목과 충돌하므로 모두 h4(##·#)·h5(### 이하)로 축소(채팅 본문에 맞는 크기).
        const lines = para.split('\n');
        const hasHeading = lines.some((l) => /^\s{0,3}#{1,6}\s+\S/.test(l));
        if (hasHeading) {
          let buf: string[] = [];
          const flush = () => {
            if (buf.length) {
              parts.push(`<p>${inline(escape(buf.join('\n'))).replace(/\n/g, '<br/>')}</p>`);
              buf = [];
            }
          };
          for (const line of lines) {
            const hm = line.match(/^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$/);
            if (hm) {
              flush();
              const tag = hm[1].length <= 2 ? 'h4' : 'h5';
              parts.push(`<${tag} class="chat-md-heading">${inline(escape(hm[2]))}</${tag}>`);
            } else {
              buf.push(line);
            }
          }
          flush();
          continue;
        }
        const escaped = escape(para);
        // Re-instate inline markdown after escape — but escape made angle brackets safe;
        // inline regex only touches *, _, ` so it's still safe.
        parts.push(`<p>${inline(escaped).replace(/\n/g, '<br/>')}</p>`);
      }
    }
  }
  return parts.join('');
}

// DOM 조각 → 마크다운 텍스트. 블록 경계는 줄바꿈, <br> 도 줄바꿈, <table> 은 마크다운 표(| … |)로
// 직렬화해 채팅의 구조(표·줄나눔)를 인용에 보존한다. .katex 는 이미 위에서 $tex$ 텍스트로 치환됨.
export function serializeFrag(node: Node): string {
  if (node.nodeType === Node.TEXT_NODE) return node.textContent ?? '';
  if (node.nodeType !== Node.ELEMENT_NODE) return '';
  const el = node as HTMLElement;
  const tag = el.tagName.toLowerCase();
  if (tag === 'br') return '\n';
  if (tag === 'table') {
    const rows = Array.from(el.querySelectorAll('tr'));
    const lines = rows.map((tr) => {
      const cells = Array.from(tr.querySelectorAll('th,td')).map((c) => serializeFrag(c).replace(/\n+/g, ' ').trim());
      return `| ${cells.join(' | ')} |`;
    });
    // 헤더 구분선(첫 행이 th 면) — 마크다운 표로 다시 렌더되게.
    if (rows.length && rows[0].querySelector('th')) {
      const n = rows[0].querySelectorAll('th,td').length;
      lines.splice(1, 0, `| ${Array(n).fill('---').join(' | ')} |`);
    }
    return '\n' + lines.join('\n') + '\n';
  }
  const inner = Array.from(el.childNodes).map(serializeFrag).join('');
  // 블록 요소면 앞뒤 줄바꿈(문단·리스트·표 행 구분 보존).
  const block = /^(p|div|li|tr|h[1-6]|ul|ol|blockquote|pre)$/.test(tag);
  return block ? `\n${inner}\n` : inner;
}

// 선택(Range) → 마크다운+LaTeX 복원. 드래그한 부분만 인용. 복사(클립보드)를 안 거쳐 KaTeX annotation
// (LaTeX 원본=SSOT)이 안 잘려 손실 0. .katex 는 annotation 으로, 표·줄바꿈 구조는 serializeFrag 로 보존.
export function latexFromSelection(range: Range, root: HTMLElement): string {
  const frag = range.cloneContents();
  // 1) 클론에 온전히 들어온 .katex 는 클론의 annotation 으로 치환.
  frag.querySelectorAll('.katex').forEach((el) => {
    const tex = (el.querySelector('annotation')?.textContent ?? '').trim();
    // ★annotation 없는 부분클론은 .katex-html 의 보이는 텍스트가 분수 등에서 순서가 뒤집혀(분모→분자)
    //   깨진다(`\frac{(x+2)(x-2)}{x-2}` → "x−2(x+2)(x−2)"). KaTeX 구조상 .katex-mathml(annotation)이
    //   .katex-html 앞이라, 보이는 부분에서 시작한 선택은 mathml 을 범위 밖으로 빠뜨려 annotation 이 없다.
    //   → 깨진 텍스트 대신 비우고, 아래 boundary 복구가 원본에서 전체 LaTeX 를 보강한다(중복·scramble 방지).
    el.replaceWith(document.createTextNode(tex ? ` $${tex}$ ` : ''));
  });
  const div = document.createElement('div'); div.appendChild(frag);
  let out = serializeFrag(div);
  // 2) 선택 양 끝이 .katex *내부*에서 잘렸으면 클론엔 annotation 없는 잔해만 → 원본에서 경계 .katex 를
  //    찾아 그 annotation 보강(경계 수식은 통째 포함, 안전).
  const texOf = (el: Element | null | undefined) => (el?.querySelector('annotation')?.textContent ?? '').trim();
  const boundK = (c: Node) => ((c.nodeType === 1 ? c as HTMLElement : c.parentElement)?.closest('.katex') ?? null);
  const sK = boundK(range.startContainer), eK = boundK(range.endContainer);
  if (sK && root.contains(sK)) { const t = texOf(sK); if (t && !out.includes(t)) out = ` $${t}$ ` + out; }
  if (eK && eK !== sK && root.contains(eK)) { const t = texOf(eK); if (t && !out.includes(t)) out = out + ` $${t}$ `; }
  return out
    .replace(/\u00a0/g, ' ')
    .replace(/[ \t]+/g, ' ')
    .replace(/ *\n */g, '\n')      // \uc904 \uc55e\ub4a4 \uacf5\ubc31 \uc815\ub9ac(\uc904\ubc14\uafc8\uc740 \ubcf4\uc874)
    .replace(/\n{3,}/g, '\n\n')    // \uacfc\ud55c \ube48 \uc904\ub9cc \ucd95\uc18c
    .trim();
}

export const reconstructPastedMath = (html: string): string | null => {
  try {
    const doc = new DOMParser().parseFromString(html, 'text/html');
    if (!doc.querySelector('.katex')) return null;
    doc.querySelectorAll('.katex').forEach((k) => {
      // ★LaTeX 원본은 MathML 의 <annotation> 에 있다. encoding 속성이 HTML 파싱서 유실될 수 있어
      //   속성 필터 없이 annotation 태그로 찾는다(엄격 셀렉터 실패→textContent 중복폴백이 'x3...x3' 깨짐 원인).
      const tex = (k.querySelector('annotation')?.textContent ?? '').trim();
      if (tex) { k.replaceWith(doc.createTextNode(` $${tex}$ `)); return; }
      // annotation 이 복사 과정에 잘렸으면 보이는 부분(.katex-html)만 — MathML 중복 텍스트 제거.
      const visible = k.querySelector('.katex-html')?.textContent ?? k.textContent ?? '';
      k.replaceWith(doc.createTextNode(visible));
    });
    const text = (doc.body.textContent ?? '')
      .replace(/\u00a0/g, ' ')
      .replace(/[ \t]*\n[ \t]*/g, '\n')
      .replace(/\n{3,}/g, '\n\n')
      .replace(/[ \t]{2,}/g, ' ')
      .trim();
    return text || null;
  } catch { return null; }
};
