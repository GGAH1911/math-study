import { Component, memo, type ReactNode, useState, useRef, useEffect, useCallback, useMemo } from 'react';
import MathField from './MathField.tsx';
import Graph, { GraphModal, type PlotSpec } from './Graph.tsx';
import Geometry, { type GeomSpec } from './Geometry.tsx';
import Geometry3D, { type Geom3DSpec } from './Geometry3D.tsx';
import Numberline, { type NumberlineSpec } from './Numberline.tsx';
import StatsChart, { type ChartSpec } from './StatsChart.tsx';
import Interactive from './Interactive.tsx';
import PromotionCard from './PromotionCard.tsx';
import type { InteractiveSpec } from '../data/interactive-samples';
import { ensureKatex, KATEX_STRICT, KATEX_ERROR_COLOR, normalizeKatex } from '../lib/mathish';
import { tryParseTable } from '../lib/markdown';
import { runSympyLocal, prewarmPyodide } from '../lib/pyodide-client';
import { buildNoteUserPrompt, NOTE_FOLLOWUPS, isNoteRequest, type NoteFollowup } from '../lib/note-prompts';
import { prepareImage, imagesFromDataTransfer } from '../lib/image-utils';
import ImageCropper from './ImageCropper.tsx';
import { isVisionDisabled } from '../lib/vision';

type ChatModalState =
  | { kind: 'plot' | 'svg'; spec?: PlotSpec; svg?: string }
  | { kind: 'geom'; geomSpec: GeomSpec }
  | { kind: 'geom3d'; geom3dSpec: Geom3DSpec }
  | { kind: 'numberline'; numberlineSpec: NumberlineSpec }
  | { kind: 'chart'; chartSpec: ChartSpec }
  | { kind: 'interactive'; interactiveSpec: InteractiveSpec };

type ChatMessage = {
  role: 'user' | 'assistant';
  content: string;
  promoted?: { path: string };
  images?: string[];   // 비전(LLM)용 타일 dataURL (user 메시지에만). 표시엔 displayImage 사용.
  displayImage?: string; // 사용자 표시용 통이미지 dataURL(작게). 타일과 분리해 "조각" 노출 안 함.
};

type Props = {
  slug: string;
  unitTitle: string;
  collection?: 'concepts' | 'problems' | 'dashboard';
  // fill=true → 부모 컨테이너 높이를 꽉 채우는 flex 레이아웃 (메시지 flex-1 스크롤,
  // 입력은 하단 고정). problem 페이지의 고정 채팅 컬럼/하단 dock 용. 기본(false)은
  // 기존 inline 카드 (concepts/dashboard 페이지).
  fill?: boolean;
};

const STORAGE_PREFIX = 'math-study:chat:';
const MAX_HISTORY_TURNS = 12; // include up to last N messages in API request

// sub-dir 진입 후 호환: 'algebra/근의_공식' 같은 새 slug 로 로딩 시,
// 기존 flat slug 'math-study:chat:근의_공식' 도 fallback 으로 확인하고 lazy 이전.
function loadHistory(slug: string): ChatMessage[] {
  if (typeof window === 'undefined') return [];
  try {
    const newKey = STORAGE_PREFIX + slug;
    const raw = window.localStorage.getItem(newKey);
    if (raw) return JSON.parse(raw) as ChatMessage[];
    if (slug.includes('/')) {
      const leaf = slug.split('/').pop() ?? slug;
      const legacyKey = STORAGE_PREFIX + leaf;
      const legacy = window.localStorage.getItem(legacyKey);
      if (legacy) {
        window.localStorage.setItem(newKey, legacy);
        window.localStorage.removeItem(legacyKey);
        return JSON.parse(legacy) as ChatMessage[];
      }
    }
    return [];
  } catch {
    return [];
  }
}

function saveHistory(slug: string, msgs: ChatMessage[]): void {
  try {
    // 이미지 dataURL 은 용량이 커 localStorage quota 를 빠르게 소진 → 저장 시 제외.
    const slim = msgs.map((m) => (m.images?.length ? { ...m, images: undefined } : m));
    window.localStorage.setItem(STORAGE_PREFIX + slug, JSON.stringify(slim));
  } catch {
    /* quota or disabled — ignore */
  }
}

// 대화 이력 DB 동기화(계정별 · 기기 넘어 유지). localStorage 는 빠른 캐시로 병행.
async function loadDbHistory(collection: string, slug: string): Promise<ChatMessage[] | null> {
  try {
    const r = await fetch(`/api/chat-history?collection=${encodeURIComponent(collection)}&slug=${encodeURIComponent(slug)}`);
    if (!r.ok) return null;
    const d = await r.json();
    return Array.isArray(d.messages) ? (d.messages as ChatMessage[]) : null;
  } catch { return null; }
}
function saveDbHistory(collection: string, slug: string, msgs: ChatMessage[]): void {
  try {
    const slim = msgs.map((m) => (m.images?.length ? { ...m, images: undefined } : m));
    fetch('/api/chat-history', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ collection, slug, messages: slim }),
    }).catch(() => { /* offline/실패 무시 — localStorage 에 캐시됨 */ });
  } catch { /* ignore */ }
}

// Lightweight markdown rendering: bold, italic, code spans, code blocks, paragraphs, KaTeX-aware passthrough.
// Strategy: split paragraphs, wrap code fences as <pre><code>, render inline.
// LLM(특히 Haiku 튜터)이 가끔 서식을 잘못 낸다: ① **굵게** 대신 <strong>/<em> 같은
// 원시 HTML 태그를 쓰고, ② 수식이 아닌 한글 산문을 $…$/$$…$$ 로 감싼다. 그대로 두면
// ①은 escape 돼 literal `<strong>` 이 보이고, ②는 KaTeX 가 실패해 raw `$…$` 가 노출된다
// (예: `$공통: 30 ← <strong>…</strong>$`). renderMarkdown 진입 직전에 마크다운/평문으로
// 정규화해 LLM 이 실수해도 깨지지 않게 한다.
function normalizeLlmMarkup(text: string): string {
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

function renderMarkdown(text: string): string {
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
      const code = escape(m?.[2] ?? '');
      parts.push(`<pre data-lang="${lang}"><code>${code}</code></pre>`);
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

// Split a message body into a list of segments. ```plot``` and ```svg```
// fenced blocks become "graph" segments; everything else stays as a "md"
// (markdown) segment. Order preserved.
export type PromoteSpec = {
  to: 'unknown' | 'learning' | 'proficient' | 'mastered';
  reason?: string;
  // 선택: LLM이 명시한 추가 증거 path (problem md, mistake md 등).
  evidence?: string[];
};

type Segment =
  | { type: 'md'; content: string }
  | { type: 'graph'; kind: 'plot' | 'svg'; spec?: PlotSpec; svg?: string; raw: string }
  | { type: 'geom'; spec: GeomSpec; raw: string }
  | { type: 'geom3d'; spec: Geom3DSpec; raw: string }
  | { type: 'numberline'; spec: NumberlineSpec; raw: string }
  | { type: 'chart'; spec: ChartSpec; raw: string }
  | { type: 'interactive'; spec: InteractiveSpec; raw: string }
  | { type: 'promote'; spec: PromoteSpec; raw: string }
  | { type: 'error'; kind: string; message: string; body: string };

// LLM 이 그린 SVG 의 활성 콘텐츠 제거(injection 방어). LLM=본인 모델이라 실위험은
// 낮지만, script/foreignObject/iframe·이벤트 핸들러(on*=)·javascript: URL 을 떼어내
// dangerouslySetInnerHTML 경로로 들어가도 안전하게 한다.
function sanitizeSvg(svg: string): string {
  return svg
    .replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/<\/?(?:script|foreignObject|iframe|object|embed)\b[^>]*>/gi, '')
    .replace(/\son\w+\s*=\s*(?:"[^"]*"|'[^']*'|[^\s>]+)/gi, '')
    .replace(/(?:href|xlink:href)\s*=\s*("\s*javascript:[^"]*"|'\s*javascript:[^']*')/gi, '');
}

export function parseGraphSegments(text: string): Segment[] {
  const out: Segment[] = [];
  const re = /```(plot|svg|geometry3d|geometry|numberline|chart|interactive|promote)\n?([\s\S]*?)```/g;
  let last = 0;
  let m: RegExpExecArray | null;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) out.push({ type: 'md', content: text.slice(last, m.index) });
    const kind = m[1];
    const body = m[2].trim();
    // Surface JSON parse failures with a visible error segment instead of
    // silently falling back to raw markdown — otherwise the user just sees
    // a code block dump with no hint that the LLM emitted broken JSON.
    // LLM 이 박는 JSON 의 흔한 invalid 패턴 자동 sanitize.
    const sanitizeJSON = (s: string): string => {
      let out = s;
      // (1) string literal 안 raw newline/tab → \n / \t 로 escape
      out = out.replace(/"((?:[^"\\]|\\.)*)"/g, (_m, inner: string) => {
        const fixed = inner
          .replace(/\r\n/g, '\\n')
          .replace(/\n/g, '\\n')
          .replace(/\r/g, '\\n')
          .replace(/\t/g, '\\t');
        return `"${fixed}"`;
      });
      // (2) string 안 LaTeX backslash (\frac, \alpha, \sqrt, \tan, \nu, \rho, \beta 등) → \\
      //   JSON 표준 escape \b\f\n\r\t 는 LaTeX 명령(\frac=\f, \tan=\t, \nu=\n, \rho=\r, \beta=\b)과
      //   글자가 겹쳐 단순히 "비표준만 double" 하면 \frac→[FF]rac 로 깨진다. 그래서:
      //   기존 \\ 와 \uXXXX(유니코드)만 보존하고, *나머지 모든 lone backslash 를 double*.
      //   (수식 라벨엔 실제 제어문자 newline/tab 이 거의 없어 안전. \" \/ 는 글자 아니라 제외.)
      out = out.replace(/"((?:[^"\\]|\\.)*)"/g, (_m, inner: string) => {
        const fixed = inner
          .replace(/\\\\/g, '')                    // 이미 유효한 \\ 보호
          .replace(/\\u([0-9a-fA-F]{4})/g, '$1')   // 유효한 \uXXXX 보호
          .replace(/\\([^"/])/g, '\\\\$1')               // 남은 lone \X (LaTeX 포함) → \\X
          .replace(//g, '\\u')                     // \uXXXX 복원
          .replace(//g, '\\\\');                   // \\ 복원
        return `"${fixed}"`;
      });
      // (3) value/배열 자리의 raw 수식(pi·sqrt·sin·cos·tan·*·/·괄호) → 평가 결과.
      //     `:` 뿐 아니라 `[`·`,` 뒤(배열 원소: "range":[0, 0.4*pi], [pi, 2*pi])도 처리한다.
      //     후행 구분자는 lookahead 로 보존 → 연속 배열 원소([2*pi, 2.4*pi])도 둘 다 잡힘.
      //     순수 숫자(-3, 5.5)는 math 토큰이 없어 그대로 둔다(유효 JSON).
      out = out.replace(
        /([:[,]\s*)((?:pi|sqrt|sin|cos|tan|[0-9.eE+\-*/() \t])+?)(?=\s*[,}\]])/g,
        (_m: string, pre: string, expr: string) => {
          if (!/(pi|sqrt|sin|cos|tan|[*/])/.test(expr)) return _m;   // math 토큰 없으면 순수 숫자 → 유지
          try {
            const safe = expr
              .replace(/\bsqrt\b/g, 'Math.sqrt').replace(/\bsin\b/g, 'Math.sin')
              .replace(/\bcos\b/g, 'Math.cos').replace(/\btan\b/g, 'Math.tan')
              .replace(/\bpi\b/g, 'Math.PI');
            const v = Function(`"use strict"; return (${safe});`)();
            if (typeof v === 'number' && Number.isFinite(v)) return `${pre}${v}`;
          } catch { /* 평가 실패 — 원본 유지 */ }
          return _m;
        });
      // (5) 배열/값 자리 분수 `a/b` → 소수. (4)는 `:` 직후만 잡아
      //     `"points":[[4/3,5/3]]` 같은 배열 요소 분수(콜론 직후가 아님)를 놓친다.
      //     콜론·`[`·`,` 뒤의 숫자 분수만 평가 → 문자열 안 `$1/2$`(선행 `=` 등)은 무관.
      out = out.replace(/([:\[,]\s*)(-?\d+(?:\.\d+)?)\s*\/\s*(-?\d+(?:\.\d+)?)/g,
        (_m, pre: string, a: string, b: string) => {
          const v = Number(a) / Number(b);
          return Number.isFinite(v) ? `${pre}${v}` : _m;
        });
      // (6) 구조적 invalid 보정. 문자열 리터럴을 먼저 placeholder 로 마스킹해
      //     문자열 안 내용(label 의 `,}` / `//` / `key:` 등)은 절대 안 건드리고
      //     구조만 손본다: trailing comma · 주석 · NaN/Infinity · 따옴표 없는 key.
      {
        const strs: string[] = [];
        let masked = out.replace(/"(?:[^"\\]|\\.)*"/g, (mm) => `\x00${strs.push(mm) - 1}\x00`);
        masked = masked
          .replace(/,(\s*[}\]])/g, '$1')                              // trailing comma
          .replace(/\/\/[^\n]*/g, '')                                 // // 주석
          .replace(/\/\*[\s\S]*?\*\//g, '')                           // /* */ 주석
          .replace(/\bNaN\b/g, 'null')                                // NaN
          .replace(/-?\bInfinity\b/g, 'null')                         // ±Infinity
          .replace(/([{,]\s*)([A-Za-z_$][\w$]*)(\s*:)/g, '$1"$2"$3');  // unquoted key
        out = masked.replace(/\x00(\d+)\x00/g, (_mm, i: string) => strs[Number(i)]);
      }
      return out;
    };
    const tryParseJSON = <T,>(make: (spec: T) => Segment): void => {
      try { out.push(make(JSON.parse(body) as T)); return; }
      catch { /* 1차 실패 — sanitize 후 재시도 */ }
      try { out.push(make(JSON.parse(sanitizeJSON(body)) as T)); }
      catch (e) {
        out.push({
          type: 'error', kind,
          message: (e as Error).message ?? 'JSON parse failed',
          body,
        });
      }
    };
    if (kind === 'plot') {
      tryParseJSON<PlotSpec>((spec) => ({ type: 'graph', kind, spec, raw: m![0] }));
    } else if (kind === 'geometry') {
      tryParseJSON<GeomSpec>((spec) => ({ type: 'geom', spec, raw: m![0] }));
    } else if (kind === 'geometry3d') {
      tryParseJSON<Geom3DSpec>((spec) => ({ type: 'geom3d', spec, raw: m![0] }));
    } else if (kind === 'numberline') {
      tryParseJSON<NumberlineSpec>((spec) => ({ type: 'numberline', spec, raw: m![0] }));
    } else if (kind === 'chart') {
      tryParseJSON<ChartSpec>((spec) => ({ type: 'chart', spec, raw: m![0] }));
    } else if (kind === 'interactive') {
      tryParseJSON<InteractiveSpec>((spec) => ({ type: 'interactive', spec, raw: m![0] }));
    } else if (kind === 'promote') {
      tryParseJSON<PromoteSpec>((spec) => ({ type: 'promote', spec, raw: m![0] }));
    } else {
      out.push({ type: 'graph', kind: 'svg', svg: sanitizeSvg(body), raw: m[0] });
    }
    last = m.index + m[0].length;
  }
  if (last < text.length) out.push({ type: 'md', content: text.slice(last) });
  return out.length > 0 ? out : [{ type: 'md', content: text }];
}

// KaTeX rendering: process $...$ and $$...$$ in the rendered HTML after markdown.
// Loader/cache lives in `lib/mathish` so all graphic components share one
// KaTeX instance.
type KatexImpl = {
  // strict/errorColor 타입은 mathish 의 KatexOpts 와 정확히 일치시켜야 ensureKatex()
  // 가 돌려주는 Katex 인스턴스를 이 KatexImpl 로 받을 수 있다(더 넓게 잡으면 함수
  // 파라미터 contravariance 가 깨져 ts2345).
  renderToString: (tex: string, opts?: {
    displayMode?: boolean;
    throwOnError?: boolean;
    strict?: 'ignore' | 'warn' | 'error' | ((code: string) => 'ignore' | 'warn' | 'error');
    errorColor?: string;
  }) => string;
};

// Haiku 같은 작은 모델이 `$...$` 마커를 까먹고 부등식·절댓값·LaTeX 명령어를
// raw로 출력해도 화면이 깨지지 않도록 escape된 `&lt;`/`&gt;`/`&amp;le;` 등을
// 수학 문맥에서만 KaTeX로 복원. HTML 태그(예: `&lt;div&gt;`)와 헷갈리지
// 않도록 양옆에 수학 토큰이 있을 때만 적용.
//
// MATH_TOKEN: 단일 식별자/숫자/연산자, LaTeX 백슬래시 명령어(`\frac`, `\quad`),
// 절댓값 `|`, 괄호. 이 토큰들이 공백으로 이어진 run을 매칭.
const MATH_TOKEN = String.raw`(?:[A-Za-z0-9\-+*/^=,.]+|\\[A-Za-z]+(?:\{[^}]*\})*|\||\(|\)|\{|\})`;
const ENTITY_OP = String.raw`(?:&lt;|&gt;|&le;|&ge;|&amp;le;|&amp;ge;)=?`;
// 줄 안 부등호 chain: `a < b < c < ...` 모두 한 번에 변환.
// left → (op left)+ 구조로 chain 캡처. KaTeX가 chain 그대로 받아서 잘 렌더.
const INEQUALITY_RUN = new RegExp(
  `(${MATH_TOKEN}(?:\\s+${MATH_TOKEN})*)(\\s*${ENTITY_OP}\\s*${MATH_TOKEN}(?:\\s+${MATH_TOKEN})*)+`,
  'g',
);
const ENTITY_TO_LATEX: Record<string, string> = {
  '&lt;': '<', '&gt;': '>',
  '&lt;=': '\\le', '&gt;=': '\\ge',
  '&le;': '\\le', '&ge;': '\\ge',
  '&amp;le;': '\\le', '&amp;ge;': '\\ge',
};

// raw `\command` 단독 (또는 sequence)를 KaTeX로. 부등호 없이도 `\quad`, `\frac{a}{b}`
// 같이 명령어만 raw로 흘러 들어온 경우 처리. 한국어/일반 텍스트와 섞이면
// 명령어 토큰 직접 주변만 wrap.
// 꼬리 token run 이 `\cmd` 뒤의 영문 단어(and, the, where…)를 탐욕적으로 흡수해
// 영문이 수식 italic 으로 오렌더되지 않도록, 3+ 글자 순수 알파벳 단어(영단어)가
// 시작되는 지점에서 run 을 끊는다. 1~2글자 math 식별자(x, n, ab)는 그대로 둔다.
const LATEX_CMD_RUN = /(\\[A-Za-z]+(?:\{[^}]{0,80}\})*(?:\s+(?![A-Za-z]{3,}(?![A-Za-z]))[A-Za-z0-9\-+*/^=.,()|\\{}]+)*)/g;

function decodeEntities(s: string): string {
  return s
    .replace(/&amp;(le|ge)=?;/g, (_, k) => k === 'le' ? '\\le' : '\\ge')
    .replace(/&le;=?/g, '\\le')
    .replace(/&ge;=?/g, '\\ge')
    .replace(/&lt;=/g, '\\le')
    .replace(/&gt;=/g, '\\ge')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&');
}

function recoverBareMath(html: string, katex: KatexImpl): string {
  // ① 부등호 chain
  html = html.replace(INEQUALITY_RUN, (full) => {
    if (/[<>]/.test(full)) return full; // 실제 raw 태그 끼이면 건드리지 않음
    const tex = decodeEntities(full);
    try { return katex.renderToString(tex, { displayMode: false, throwOnError: true, strict: KATEX_STRICT }); }
    catch { return full; }
  });
  // ② raw `\command` 토큰 — 부등호 없이도 KaTeX로 시도. `\command` 가 KaTeX에
  // 모르는 명령어면 throw → 원본 반환.
  html = html.replace(LATEX_CMD_RUN, (full) => {
    // 이미 KaTeX SVG로 변환된 영역(<span class="katex">) 안은 건드리지 않음.
    // 단순 휴리스틱: full 안에 `<` 가 있으면 skip (HTML 태그 영역).
    if (/[<>]/.test(full)) return full;
    const tex = decodeEntities(full).trim();
    if (tex.length < 2) return full;
    try { return katex.renderToString(tex, { displayMode: false, throwOnError: true, strict: KATEX_STRICT }); }
    catch { return full; }
  });
  // ENTITY_TO_LATEX는 future-proof로 유지 (현재는 decodeEntities로 통합).
  void ENTITY_TO_LATEX;
  return html;
}

function applyKatex(html: string, katex: KatexImpl): string {
  // throwOnError: true 가 핵심 — false면 KaTeX가 파싱 실패 시 빨간색(#cc0000)
  // error HTML을 부분 출력해 DOM에 raw `<span style="color:#cc0000">5 &gt; 3</span>`
  // 같은 잔재가 들어간다 (실제 LLM이 그런 HTML을 출력한 게 아니라 KaTeX의 errorColor).
  // true로 두면 fail 시 throw → catch → 원본 `$...$` 텍스트가 그대로 보임 (안전).
  //
  // tex 안에 `&lt;`/`&gt;` 같은 escape된 entity가 들어오면 KaTeX는 이해 못함.
  // decode 후 KaTeX 호출.
  // `[^<>]` (← 옛 `[^$<>]`): 내부 `$` 를 허용해 `\text{$y$ 표기}` 처럼 \text{} 안에
  // 중첩된 `$` 가 들어간 display 수식도 통째로 잡는다(KaTeX 는 \text{} 안 `$...$` 를
  // 정상 처리). 짝 안 맞는 `$$` 의 폭주는 `<>` 가드(태그를 못 건넘) + KaTeX
  // throwOnError(유효 TeX 가 아니면 catch→원본 raw) 로 여전히 막힌다.
  // 멀티라인 $$…$$ : renderMarkdown 이 문단 내 개행을 전부 <br/> 로 바꾸므로(line 154)
  // `[^<>]` 만으론 <br/> 를 못 건너 닫는 $$ 까지 매칭 실패 → align 블록이 통째로 raw 노출.
  // <br/> 만 추가 허용(다른 태그는 여전히 차단=폭주 가드 유지)해 통째로 잡은 뒤, 매칭 본문의
  // <br/> 를 \n 으로 되돌린다(KaTeX aligned 는 \\ 로 행 구분, \n 은 무시 — 안전).
  html = html.replace(/\$\$((?:<br\s*\/?>|[^<>])+?)\$\$/g, (_, tex: string) => {
    try {
      const clean = tex.replace(/<br\s*\/?>/g, '\n');
      return katex.renderToString(normalizeKatex(decodeEntities(clean)), { displayMode: true, throwOnError: true, strict: KATEX_STRICT, errorColor: KATEX_ERROR_COLOR });
    } catch {
      return _;
    }
  });
  // `[^\n$<>]` 의 `<>` 가드가 핵심: 이 시점엔 renderMarkdown 이 문단 내 개행을
  // 전부 <br/> 로 바꾸고 문단을 구분자 없이 이어붙여(`\n` 가 하나도 안 남음) 정규식의
  // `\n` 폭주 방지턱이 무력화돼 있다. 그런데 실제 수학의 부등호는 이미 `&lt;`/`&gt;`
  // 엔티티 상태고, 남은 raw `<`/`>` 는 전부 HTML 태그(<code>·<br/>·</p>…)뿐이다.
  // 따라서 `<`/`>` 를 매칭에서 제외하면 — 짝 안 맞는 stray `$` 하나가 태그들을 가로질러
  // 메시지 전체를 삼키는 폭주를 막는다(태그를 만나면 매칭이 끊겨 그 `$` 는 그냥 literal).
  // 짝 맞는 `$...$` 는 태그를 안 건너므로 영향 없이 정상 렌더된다.
  // `\\text\{[^{}]*\}` 대안 추가: inline `$...$` 안에 `\text{$y$}` 처럼 중첩 `$` 가
  // 들어가도 \text{} 블록을 통째로 허용해 매칭한다(그 외 위치의 `$` 는 여전히 거부해
  // delimiter 짝을 유지).
  html = html.replace(/\$((?:\\text\{[^{}]*\}|[^\n$<>])+?)\$/g, (_, tex) => {
    try {
      return katex.renderToString(normalizeKatex(decodeEntities(tex)), { displayMode: false, throwOnError: true, strict: KATEX_STRICT, errorColor: KATEX_ERROR_COLOR });
    } catch {
      return _;
    }
  });
  // Fallback: LLM이 `$...$`를 까먹은 raw 부등식 복원.
  html = recoverBareMath(html, katex);
  return html;
}

// Visible fallback when an LLM-emitted fenced block has invalid JSON.
// Without this, parse failures silently render the raw fence as a code
// block and the user has no signal that they should re-prompt.
export function ErrorSegment({ kind, message, body }: { kind: string; message: string; body: string }) {
  return (
    <div className="my-2 rounded-lg border border-rose-500/40 bg-rose-500/10 p-2.5 text-xs">
      <div className="flex items-baseline gap-2 text-rose-300 font-medium">
        <span>⚠</span>
        <span>{`\`${kind}\` 블록 JSON 파싱 실패`}</span>
      </div>
      <pre className="mt-1 text-rose-200/80 whitespace-pre-wrap break-words">{message}</pre>
      <details className="mt-1">
        <summary className="cursor-pointer text-rose-400/70 hover:text-rose-300 text-[10px] uppercase tracking-wider">
          원문 보기
        </summary>
        <pre className="mt-1 p-1.5 rounded bg-zinc-950/80 text-zinc-400 whitespace-pre-wrap break-words font-mono text-[10px] max-h-40 overflow-auto">{body}</pre>
      </details>
    </div>
  );
}

// LLM 이 invalid spec 박아 graphic 컴포넌트 crash 해도 채팅창 전체 죽지 않게.
class GraphicErrorBoundary extends Component<{ children: ReactNode; kind: string }, { error: Error | null }> {
  constructor(props: { children: ReactNode; kind: string }) { super(props); this.state = { error: null }; }
  static getDerivedStateFromError(error: Error) { return { error }; }
  componentDidCatch(error: Error) { console.warn(`[ChatPanel] ${this.props.kind} crashed:`, error.message); }
  render() {
    if (this.state.error) {
      return (
        <div className="my-2 rounded-lg border border-rose-500/40 bg-rose-500/10 p-2.5 text-xs text-rose-300">
          <span>⚠ {this.props.kind} 렌더 실패: </span>
          <span className="font-mono">{this.state.error.message}</span>
        </div>
      );
    }
    return this.props.children;
  }
}

export function MdSegment({ content }: { content: string }) {
  // 동기 markdown 처리 (escape + inline + 표). 이걸 첫 paint 시점에 바로 표시해서
  // KaTeX 모듈 import 완료 전에 raw content가 DOM에 들어가는 사고를 막는다.
  // (이전: `html || content` 가 fallback이라 LLM이 raw `<span>` 같은 HTML을
  //  emit하면 그대로 해석되어 XSS 위험 + 화면 깨짐).
  const baseHtml = useMemo(() => renderMarkdown(content), [content]);
  const [html, setHtml] = useState<string>(baseHtml);
  useEffect(() => {
    // content 변경 시 stale KaTeX-적용본을 베이스로 즉시 교체.
    setHtml(baseHtml);
    let cancelled = false;
    (async () => {
      const k = await ensureKatex();
      if (k && !cancelled) setHtml(applyKatex(baseHtml, k));
    })();
    return () => { cancelled = true; };
  }, [baseHtml]);
  return <div className="prose-chat" dangerouslySetInnerHTML={{ __html: html }} />;
}

// Memoized so the message list doesn't re-render on every keystroke in the
// chat input. `onPromote` now receives the message index — passing a stable
// callback from the parent keeps prop identity steady, which lets `memo`
// actually skip rerenders.
const Message = memo(function Message({ msg, index, onPromote, onNoteFollowup, busy, slug, collection, isStreaming, isNoteResponse }: {
  msg: ChatMessage; index: number;
  onPromote?: (idx: number) => void;
  onNoteFollowup?: (kind: NoteFollowup) => void;
  busy?: boolean;
  slug: string; collection: 'concepts' | 'problems' | 'dashboard';
  isStreaming?: boolean;
  // True when the directly-preceding user message was a `[학습 노트 요청]`.
  // Shows an action row (저장 / 더 짧게 / 더 자세히 / 핵심만) under this reply.
  isNoteResponse?: boolean;
}) {
  // Hooks MUST run unconditionally so React's order-tracking holds even
  // when the message content shifts into one of the special-prefix branches
  // below (rare in practice, but easy to keep correct).
  const isUser = msg.role === 'user';
  const segments = useMemo(() => parseGraphSegments(msg.content), [msg.content]);
  const [modal, setModal] = useState<ChatModalState | null>(null);
  const canPromote = !!onPromote && !isUser && msg.content.trim().length > 0 && !busy;

  // 자동 계산 결과 inject 된 user message 는 내부 protocol — 사용자에겐 chip 만 표시.
  if (isUser && msg.content.startsWith('[자동 계산 결과 — 검증 실패]')) {
    return (
      <div className="flex flex-col items-end">
        <div className="text-[10px] px-2 py-1 rounded-full bg-amber-700/30 text-amber-300 border border-amber-700/50">
          ⚠ 검증 재계산
        </div>
      </div>
    );
  }
  if (isUser && msg.content.startsWith('[자동 계산 결과]')) {
    return (
      <div className="flex flex-col items-end">
        <div className="text-[10px] px-2 py-1 rounded-full bg-zinc-700/40 text-zinc-400 border border-zinc-600">
          ⚙ 정확한 좌표 계산 완료
        </div>
      </div>
    );
  }
  if (isUser && msg.content.startsWith('[시각 검증]')) {
    return (
      <div className="flex flex-col items-end">
        <div className="text-[10px] px-2 py-1 rounded-full bg-zinc-700/40 text-zinc-400 border border-zinc-600">
          🔍 도형 검증 중…
        </div>
      </div>
    );
  }
  if (!isUser && msg.content.trim() === '[검증 통과]') {
    return (
      <div className="flex flex-col items-start">
        <div className="text-[10px] px-2 py-1 rounded-full bg-emerald-700/30 text-emerald-300 border border-emerald-700/50">
          ✓ 도형 검증 완료
        </div>
      </div>
    );
  }
  return (
    <div data-mi={index} className={`flex flex-col ${isUser ? 'items-end' : 'items-start'}`}>
      <div
        className={`max-w-[92%] rounded-xl px-3.5 py-2 text-sm leading-relaxed space-y-2
          ${isUser
            ? 'bg-indigo-500/10 border border-indigo-500/30 text-zinc-100'
            : 'bg-[color:var(--color-surface-2)] border border-[color:var(--color-border)] text-zinc-100'}`}
      >
        {isUser && (msg.displayImage || (msg.images && msg.images.length > 0)) && (
          <div className="flex items-end gap-1.5 mb-1">
            <img src={msg.displayImage ?? msg.images![0]} alt="첨부 이미지" className="max-h-40 rounded border border-indigo-500/30" />
          </div>
        )}
        {segments.map((s, i) => {
          if (s.type === 'md') return <MdSegment key={i} content={s.content} />;
          // Streaming 중 partial JSON parse 실패는 silent — 완성되면 정상 segment 로 바뀜.
          // 사용자에게 "실패" 처럼 보이는 일시 오류를 숨김.
          if (s.type === 'error') {
            if (isStreaming) return null;
            return <ErrorSegment key={i} kind={s.kind} message={s.message} body={s.body} />;
          }
          if (s.type === 'geom') {
            return <GraphicErrorBoundary key={i} kind="geometry">
              <Geometry spec={s.spec}
                        onOpen={() => setModal({ kind: 'geom', geomSpec: s.spec })} />
            </GraphicErrorBoundary>;
          }
          if (s.type === 'geom3d') {
            return <GraphicErrorBoundary key={i} kind="geometry3d">
              <Geometry3D spec={s.spec}
                          onOpen={() => {
                            setModal({ kind: 'geom3d', geom3dSpec: s.spec });
                            window.dispatchEvent(new CustomEvent('math-study:geom3d-modal', { detail: { open: true } }));
                          }} />
            </GraphicErrorBoundary>;
          }
          if (s.type === 'numberline') {
            return <GraphicErrorBoundary key={i} kind="numberline">
              <Numberline spec={s.spec}
                          onOpen={() => setModal({ kind: 'numberline', numberlineSpec: s.spec })} />
            </GraphicErrorBoundary>;
          }
          if (s.type === 'chart') {
            return <GraphicErrorBoundary key={i} kind="chart">
              <StatsChart spec={s.spec}
                          onOpen={() => setModal({ kind: 'chart', chartSpec: s.spec })} />
            </GraphicErrorBoundary>;
          }
          if (s.type === 'interactive') {
            return <GraphicErrorBoundary key={i} kind="interactive">
              <Interactive spec={s.spec}
                           onOpen={() => setModal({ kind: 'interactive', interactiveSpec: s.spec })} />
            </GraphicErrorBoundary>;
          }
          if (s.type === 'promote') {
            // mastery 승급 카드는 concept 페이지에서만 의미 있음. 다른 collection에선
            // skip (ErrorSegment 안내).
            if (collection !== 'concepts') {
              return <ErrorSegment key={i} kind="promote"
                       message="mastery 승급은 concept 페이지에서만 적용 가능합니다."
                       body={s.raw} />;
            }
            return <PromotionCard key={i} slug={slug}
                                  to={s.spec.to} reason={s.spec.reason}
                                  evidence={s.spec.evidence} />;
          }
          return (
            <Graph
              key={i}
              kind={s.kind}
              spec={s.spec}
              svg={s.svg}
              onOpen={() => setModal({ kind: s.kind, spec: s.spec, svg: s.svg })}
            />
          );
        })}
      </div>
      {isNoteResponse && !isStreaming && msg.content.trim().length > 0 && !busy ? (
        // Action row under a 학습 노트 reply — save (= promote) plus three
        // followup rewrites. Clicking a followup re-fires the LLM call with
        // a `[학습 노트 요청]`-marked instruction, so the next reply also
        // gets this same row → 사용자가 마음에 들 때까지 iterate.
        <div className="mt-1.5 flex flex-wrap gap-1.5">
          <button
            type="button"
            onClick={() => onPromote?.(index)}
            disabled={!!msg.promoted}
            className={`text-[11px] px-2.5 py-1 rounded border transition ${
              msg.promoted
                ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300 cursor-default'
                : 'bg-indigo-500/15 border-indigo-500/40 text-indigo-200 hover:bg-indigo-500/25 cursor-pointer'
            }`}
            title={msg.promoted ? `저장됨: ${msg.promoted.path}` : '이 노트를 docs/syntheses/ 에 영구 저장'}
          >
            {msg.promoted ? '✓ 저장됨' : '💾 저장'}
          </button>
          <button
            type="button"
            onClick={() => onNoteFollowup?.('shorter')}
            className="text-[11px] px-2.5 py-1 rounded border border-[color:var(--color-border)] bg-[color:var(--color-surface-2)] text-zinc-300 hover:text-zinc-100 hover:border-zinc-500 transition"
          >📏 더 짧게</button>
          <button
            type="button"
            onClick={() => onNoteFollowup?.('longer')}
            className="text-[11px] px-2.5 py-1 rounded border border-[color:var(--color-border)] bg-[color:var(--color-surface-2)] text-zinc-300 hover:text-zinc-100 hover:border-zinc-500 transition"
          >📖 더 자세히</button>
          <button
            type="button"
            onClick={() => onNoteFollowup?.('coreOnly')}
            className="text-[11px] px-2.5 py-1 rounded border border-[color:var(--color-border)] bg-[color:var(--color-surface-2)] text-zinc-300 hover:text-zinc-100 hover:border-zinc-500 transition"
          >🎯 핵심만</button>
        </div>
      ) : canPromote && (
        <button
          onClick={() => onPromote?.(index)}
          disabled={busy || !!msg.promoted}
          className={`mt-1 text-[10px] uppercase tracking-wider transition ${
            msg.promoted
              ? 'text-emerald-400 cursor-default'
              : 'text-zinc-500 hover:text-zinc-100 cursor-pointer'
          }`}
        >
          {msg.promoted ? `✓ 노트에 저장됨 (${msg.promoted.path.split('/').pop()})` : '↑ 노트에 영구 저장'}
        </button>
      )}
      {modal && (
        <GraphModal
          open
          kind={modal.kind}
          spec={modal.kind === 'plot' || modal.kind === 'svg' ? modal.spec : undefined}
          svg={modal.kind === 'svg' ? modal.svg : undefined}
          geomSpec={modal.kind === 'geom' ? modal.geomSpec : undefined}
          geom3dSpec={modal.kind === 'geom3d' ? modal.geom3dSpec : undefined}
          numberlineSpec={modal.kind === 'numberline' ? modal.numberlineSpec : undefined}
          chartSpec={modal.kind === 'chart' ? modal.chartSpec : undefined}
          interactiveSpec={modal.kind === 'interactive' ? modal.interactiveSpec : undefined}
          onClose={() => {
            setModal(null);
            window.dispatchEvent(new CustomEvent('math-study:geom3d-modal', { detail: { open: false } }));
          }}
        />
      )}
    </div>
  );
});

export default function ChatPanel({ slug, unitTitle, collection = 'concepts', fill = false }: Props) {
  const placeholderHint =
    collection === 'dashboard' ? '예: 삼각함수가 헷갈리는데 어디부터 봐야 해?' :
    collection === 'problems'  ? '예: 이 문제 어떻게 풀어?' :
                                  '예: 근의 공식이 왜 저렇게 생겼어?';
  const subtitle =
    collection === 'dashboard' ? '학습 길잡이 — 무엇을 모르는지 말하면 어디로 가야 할지 알려드립니다.' :
    collection === 'problems'  ? `"${unitTitle}" 문제에 한정한 LLM 튜터.` :
                                  `"${unitTitle}" 단원에 한정한 LLM 튜터.`;
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [streaming, setStreaming] = useState(false);
  const [model, setModel] = useState<'haiku' | 'sonnet'>('haiku');
  const [error, setError] = useState<string | null>(null);
  const [mathOpen, setMathOpen] = useState(false);
  const [mathLatex, setMathLatex] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);
  const scrollRef = useRef<HTMLDivElement | null>(null);
  // 이미지 첨부 state
  const [pending, setPending] = useState<string[]>([]);          // 전송 대기 비전 타일들 (원해상도 PNG dataURL N장)
  const [pendingDisplay, setPendingDisplay] = useState<string | null>(null);  // 사용자 표시용 통이미지(타일과 분리)
  const [cropSrc, setCropSrc] = useState<string | null>(null);   // 크롭 모달 대상 (원본 dataURL)
  const [imgError, setImgError] = useState<string | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  // BYOK 설정 — 학생 본인 LLM (OpenRouter / Ollama local / 기타). localStorage 영구 보관.
  // baseURL 있으면 BYOK 사용, 없으면 dev fallback (claude CLI)
  const [byokOpen, setByokOpen] = useState(false);
  const [byokApiKey, setByokApiKey] = useState<string>('');
  const [byokModel, setByokModel] = useState<string>('openrouter/auto');
  const [byokBaseURL, setByokBaseURL] = useState<string>('https://openrouter.ai/api/v1');
  useEffect(() => {
    try {
      const k = localStorage.getItem('math-study:byok:apikey');
      const m = localStorage.getItem('math-study:byok:model');
      const b = localStorage.getItem('math-study:byok:baseurl');
      if (k) setByokApiKey(k);
      if (m) setByokModel(m);
      if (b) setByokBaseURL(b);
    } catch { /* localStorage 비활성 */ }
  }, []);
  // BYOK 활성 조건 — OpenRouter 면 apiKey 필수, Ollama (localhost/tailnet) 면 apiKey 없어도 OK
  // 호스트가 스킴(`//`) 직후에 오도록 앵커링 — 앵커 없으면 `https://10.example.com`
  // 같은 공인 도메인이나 경로에 박힌 `//100.` 이 로컬로 오판돼 무인증 더미키로 전송됨.
  const isOllamaLike = /^https?:\/\/(localhost|127\.0\.0\.1|0\.0\.0\.0|100\.\d|10\.\d|192\.168\.)/.test(byokBaseURL.trim());
  const byokActive = byokApiKey.length > 0 || (isOllamaLike && byokBaseURL.length > 0);
  const saveByok = useCallback((apiKey: string, modelId: string, baseURL: string) => {
    setByokApiKey(apiKey);
    setByokModel(modelId);
    setByokBaseURL(baseURL);
    try {
      if (apiKey) localStorage.setItem('math-study:byok:apikey', apiKey);
      else localStorage.removeItem('math-study:byok:apikey');
      localStorage.setItem('math-study:byok:model', modelId);
      localStorage.setItem('math-study:byok:baseurl', baseURL);
    } catch { /* ignore */ }
  }, []);

  // Insert "$...$" at the current cursor position in the textarea
  const insertMath = useCallback((latex: string) => {
    if (!latex.trim()) return;
    const ta = textareaRef.current;
    const wrapped = `$${latex}$`;
    if (!ta) { setInput((prev) => prev + (prev.endsWith(' ') ? '' : ' ') + wrapped); return; }
    const start = ta.selectionStart ?? input.length;
    const end = ta.selectionEnd ?? input.length;
    const before = input.slice(0, start);
    const after = input.slice(end);
    const sep = before && !before.endsWith(' ') ? ' ' : '';
    const next = before + sep + wrapped + after;
    setInput(next);
    setMathLatex('');
    setMathOpen(false);
    // restore focus + cursor after the inserted block
    setTimeout(() => {
      ta.focus();
      const pos = (before + sep + wrapped).length;
      ta.setSelectionRange(pos, pos);
    }, 0);
  }, [input]);

  const storageKey = `${collection}:${slug}`;

  // Interactive 컴포넌트가 '📋 현재 상태 채팅에 첨부' 버튼을 누르면
  // window CustomEvent로 한 줄 메타가 날아온다. textarea 앞에 prepend.
  // 같은 종류의 메타가 이미 있으면 교체 (누적되지 않게).
  useEffect(() => {
    const onInsert = (e: Event) => {
      const detail = (e as CustomEvent<{ text: string }>).detail;
      if (!detail?.text) return;
      setInput((prev) => {
        // 기존 [현재 상태] ... 라인이 맨 앞에 있으면 떼어내고 새 것으로 교체.
        const cleaned = prev.replace(/^\[현재 상태\][^\n]*\n?/, '');
        return `${detail.text}\n${cleaned}`;
      });
      // focus + cursor를 본문 끝으로
      setTimeout(() => {
        const ta = textareaRef.current;
        if (ta) {
          ta.focus();
          const len = ta.value.length;
          ta.setSelectionRange(len, len);
        }
      }, 0);
    };
    window.addEventListener('math-study:chat-insert', onInsert as EventListener);
    return () => window.removeEventListener('math-study:chat-insert', onInsert as EventListener);
  }, []);


  // Load history on mount — localStorage 즉시 표시 후 DB(계정·기기 넘어) 권위로 동기화.
  useEffect(() => {
    const local = loadHistory(storageKey);
    setMessages(local);
    // pyodide worker 선제 로드 — 첫 sympy 호출 시 대기 ↓
    prewarmPyodide();
    let cancelled = false;
    (async () => {
      const db = await loadDbHistory(collection, slug);
      if (cancelled) return;
      if (db && db.length > 0) setMessages(db);            // DB 권위(다른 기기 대화 포함)
      else if (local.length > 0) saveDbHistory(collection, slug, local); // 마이그레이션
    })();
    return () => { cancelled = true; };
  }, [storageKey]);

  // Persist on change — localStorage 캐시 + DB 둘 다 디바운스. 스트리밍 중엔 토큰마다
  // messages 가 바뀌는데, 그때마다 saveHistory(전체 JSON.stringify=O(n))를 동기 실행하면
  // 긴 히스토리에서 O(n²) 누적으로 스크롤이 버벅인다. 중간 토큰 상태 저장은 무의미(응답
  // 미완성)하므로 스트림이 잦아든 뒤(또는 단일 액션 후) 한 번만 저장한다.
  useEffect(() => {
    if (messages.length === 0) return;
    const t = setTimeout(() => {
      saveHistory(storageKey, messages);
      saveDbHistory(collection, slug, messages);
    }, 500);
    return () => clearTimeout(t);
  }, [storageKey, messages, collection, slug]);

  // 스크롤 정책 (ChatGPT 식):
  //  - 새 user 질문이 들어오면 그 질문을 스크롤 영역 '상단'으로 → 이어질 (긴) 답변이
  //    위에서부터 펼쳐져, 첫 줄이 자동 하단스크롤에 가려져 잘려 보이던 문제를 없앤다.
  //  - assistant 스트리밍/갱신은 사용자가 거의 바닥에 있을 때만 추종(near-bottom).
  //    위로 올려 읽는 중이면 끌어내리지 않는다.
  useEffect(() => {
    const el = scrollRef.current;
    if (!el) return;
    const last = messages[messages.length - 1];
    if (last && last.role === 'user') {
      const node = el.querySelector(`[data-mi="${messages.length - 1}"]`) as HTMLElement | null;
      if (node) {
        // 영역 내 상대 위치만큼 스크롤(페이지 전체 스크롤 부작용 없는 방식).
        el.scrollTop += node.getBoundingClientRect().top - el.getBoundingClientRect().top - 8;
        return;
      }
    }
    const nearBottom = el.scrollHeight - el.scrollTop - el.clientHeight < 200;
    if (nearBottom) el.scrollTop = el.scrollHeight;
  }, [messages]);

  // `override`: when called from the 학습 노트 buttons (right-side card or
  // action row), we pass the prompt directly instead of routing through the
  // input field. The textarea is left untouched so the user can keep typing
  // their own follow-up while the note request flies off.
  const send = useCallback(async (override?: string) => {
    const text = (override ?? input).trim();
    const attachedImgs = override === undefined ? pending : [];    // 합성/노트 호출엔 첨부 없음 (첫 user 메시지에만)
    const attachedDisplay = override === undefined ? pendingDisplay : null;  // 표시용 통이미지(타일과 분리)
    if ((!text && !attachedImgs.length) || streaming) return;      // 이미지만 있어도 전송 허용
    setError(null);
    if (override === undefined) { setInput(''); setPending([]); setPendingDisplay(null); setImgError(null); }

    const newUserMsg: ChatMessage = {
      role: 'user',
      content: text || '(첨부한 이미지를 봐주세요)',
      // images=비전 타일(LLM 전송), displayImage=통이미지(표시) — 사용자에겐 통이미지만 보임.
      ...(attachedImgs.length ? { images: attachedImgs, displayImage: attachedDisplay ?? attachedImgs[0] } : {}),
    };
    const placeholder: ChatMessage = { role: 'assistant', content: '' };
    setMessages([...messages, newUserMsg, placeholder]);
    setStreaming(true);

    // python block 을 채팅창에 노출하지 않기 위한 display sanitize.
    // python block 만 있는 응답은 chip 으로, geometry 등 다른 본문이 있으면 그대로.
    const sanitizeForDisplay = (s: string) => {
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

    // raw conversation (LLM 호출용, python/geometry 등 원본 보존)
    const rawHistory: ChatMessage[] = [...messages.slice(-MAX_HISTORY_TURNS), newUserMsg];
    // 표시 누적 — setMessages 인자로 직접 전달.
    let displayMessages: ChatMessage[] = [...messages, newUserMsg, placeholder];

    // 한 turn LLM 호출 + 마지막 placeholder 자리에 streaming 갱신. raw 텍스트 반환.
    // BYOK 모드 (apiKey 있음): /api/openrouter 로 학생 key 와 함께 relay.
    // dev fallback: /api/chat 의 claude CLI subprocess.
    const callLLM = async (history: ChatMessage[]): Promise<string> => {
      let assistantText = '';
      try {
        const endpoint = byokActive ? '/api/openrouter' : '/api/chat';
        const body = byokActive
          ? {
              slug, collection,
              messages: history.slice(-MAX_HISTORY_TURNS),
              model: byokModel,
              apiKey: byokApiKey || 'ollama', // ollama 등 인증 없는 endpoint 용 dummy
              baseURL: byokBaseURL,
            }
          : { slug, collection, messages: history.slice(-MAX_HISTORY_TURNS), model };
        const res = await fetch(endpoint, {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(body),
        });
        if (!res.ok || !res.body) throw new Error(`HTTP ${res.status}`);
        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let buf = '';
        while (true) {
          const { value, done } = await reader.read();
          if (done) break;
          buf += decoder.decode(value, { stream: true });
          let idx;
          while ((idx = buf.indexOf('\n\n')) !== -1) {
            const block = buf.slice(0, idx); buf = buf.slice(idx + 2);
            let event = 'message', data = '';
            for (const line of block.split('\n')) {
              if (line.startsWith('event: ')) event = line.slice(7).trim();
              else if (line.startsWith('data: ')) data = line.slice(6);
            }
            if (!data) continue;
            try {
              const parsed = JSON.parse(data);
              if (event === 'delta' && typeof parsed.text === 'string') {
                assistantText += parsed.text;
                const display = sanitizeForDisplay(assistantText);
                setMessages((curr) => {
                  const next = [...curr];
                  next[next.length - 1] = { role: 'assistant', content: display };
                  return next;
                });
              } else if (event === 'error') {
                setError(parsed.message ?? 'unknown error');
              }
            } catch { /* ignore */ }
          }
        }
      } catch (e) {
        setError((e as Error).message);
      }
      return assistantText;
    };

    // sympy 실행 (pyodide → server fallback)
    const runSympy = async (code: string): Promise<{ ok: boolean; stdout: string }> => {
      let sjson: { ok: boolean; stdout?: string; stderr?: string; error?: string; exit_code?: number };
      try { sjson = await runSympyLocal(code); }
      catch {
        const sres = await fetch('/api/sympy', {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ code }),
        });
        sjson = await sres.json();
      }
      const stdout = (sjson.ok ? (sjson.stdout || '(no output)') : (sjson.stderr || sjson.error || `exit ${sjson.exit_code}`)).trim();
      return { ok: !!sjson.ok, stdout };
    };

    // 새 user/assistant pair 를 displayMessages + setMessages 동시 갱신
    const appendTurn = (userMsg: ChatMessage) => {
      const ph: ChatMessage = { role: 'assistant', content: '' };
      displayMessages = [...displayMessages, userMsg, ph];
      setMessages(displayMessages);
      rawHistory.push(userMsg);
    };
    const finalizeAssistant = (rawText: string, display?: string) => {
      const shown = display ?? sanitizeForDisplay(rawText);
      displayMessages = [...displayMessages.slice(0, -1), { role: 'assistant', content: shown }];
      setMessages(displayMessages);
      rawHistory.push({ role: 'assistant', content: rawText });
    };

    try {
      // ===== Turn 1: 초기 응답 =====
      let assistantText = await callLLM(rawHistory);
      finalizeAssistant(assistantText);

      // ===== Sympy auto-exec + VERIFY FAIL retry (1회 cap) =====
      // 펜스 정규식을 sanitizeForDisplay(L817) 의 strip 형태와 일치시킨다.
      // 개행 강제(\s*\n)면 한 줄 펜스(```python x=1```)가 표시에선 제거되는데
      // 여기선 매칭 실패 → 실행 안 됨 → '계산 중…' chip 영구 고착. \n? 로 완화.
      const extractPy = (s: string) => s.match(/```(?:python|py|sympy)[ \t]*\n?([\s\S]*?)```/);
      const isFollowupInput = text.startsWith('[자동 계산 결과]') || text.startsWith('[시각 검증]');
      const MAX_SYMPY_ROUNDS = 3;
      let rounds = 0;
      const hasGeometry = (s: string) => /```geometry(3d)?\s*\n/.test(s);
      while (!isFollowupInput && rounds < MAX_SYMPY_ROUNDS) {
        if (hasGeometry(assistantText)) break; // 도형 emit 완료
        const m = extractPy(assistantText);
        if (!m) break; // python 도 도형도 없음 → 종료
        const sympyResult = await runSympy(m[1]);
        const failed = /\[VERIFY FAIL\]/.test(sympyResult.stdout);
        const prefix = failed ? '[자동 계산 결과 — 검증 실패]' : '[자동 계산 결과]';
        const tail = failed
          ? '\n\n위 출력에 `[VERIFY FAIL]` 항목이 있다. **이전 가정/수식이 어디서 틀렸는지** 찾아 단계 정의를 다시 읽고 sympy 코드를 다시 작성해 재계산하라. 추정 금지.'
          : '\n\n위 출력의 각 점 좌표를 **글자 그대로 ```geometry``` spec 의 `at: [x, y]` 에 옮겨 적어라**. 추정·반올림 금지. 이번 응답에서 바로 geometry block 작성, 대기 메시지 금지, 기술 용어 노출 금지.';
        const injected = `${prefix}\n\`\`\`\n${sympyResult.stdout}\n\`\`\`${tail}`;
        appendTurn({ role: 'user', content: injected });
        assistantText = await callLLM(rawHistory);
        finalizeAssistant(assistantText);
        rounds++;
      }

      // ===== Visual self-check (problems 페이지 + geometry emit 시 1회) =====
      const geomMatch = assistantText.match(/```geometry(3d)?\s*\n([\s\S]*?)```/);
      if (collection === 'problems' && geomMatch && !isFollowupInput) {
        const is3d = !!geomMatch[1];
        const specStr = geomMatch[2].trim();
        const checkMsg = [
          '[시각 검증]',
          '방금 emit 한 geometry spec:',
          '```json',
          specStr,
          '```',
          '',
          '원본 문제 도형 이미지를 Read 로 다시 본 뒤, **명백한 좌표 오류**만',
          '잡는다. 기본 응답은 `[검증 통과]`. 다시 그리는 비용이 크므로',
          '왠만하면 통과시킬 것.',
          '',
          '**다시 그릴 사유 — 다음 둘 중 하나만 해당하면 emit**:',
          '1. 점의 *사분면 부호*가 거꾸로 (이미지에선 P 가 왼쪽 위인데 spec',
          '   에선 오른쪽 위 같은 거울 대칭) → 좌표 derive 자체가 틀린 신호.',
          '   **3D 의 경우 정육면체 ABCD-EFGH 의 ABCD 가 위 면인지 / EFGH 가 위',
          '   인지 — 위/아래 면 거꾸로 박혔는지 반드시 확인.**',
          '2. 곡선 *종류*가 틀림 (이미지가 타원인데 spec 은 원, 쌍곡선인데 포물선)',
          ...(is3d ? [
            '3. **3D 한정: 문제에 없는 보조 segment 가 잔뜩 추가** (예: 정육면체의 모든 vertex 쌍 사이 대각선)',
            '   → 핵심 선분만 남기고 *불필요한 외곽선*만 제거. **단 학생 이해 돕는 보조 (정사영선, 회전축, 단면선) 는 통과.**',
            '4. **3D 한정: 명백한 over-emit** (정육면체 부피의 5배 이상의 거대 외접구 같이 핵심 도형을 가리는 경우) → 제거.',
            '   **그 외 (정사영면 plane, 회전체 parametricSurface, 보조 구체 sphere) 는 학습 시각화 도구로 통과.**',
          ] : []),
          '',
          '**무시할 차이 — 무조건 통과**:',
          '- 라벨 위치(NE/SW 등) 미세 차이',
          '- 색·선 두께·fill opacity 차이',
          '- **이미지가 반원(호)인데 spec 이 전체 원(circle)** — Geometry 컴포넌트가',
          '  호(arc)를 지원하지 않으므로 의도된 한계. 다시 안 그림.',
          '- 호를 polygon vertex 로 근사 (Geometry 컴포넌트 한계)',
          '- segment 가 여러 조각으로 나뉘어 그려진 경우 (시각적으로 같음)',
          '- 점의 상대 위치가 대략 비슷하면 (정확한 픽셀 위치 X)',
          '- 보조선·음영 일부 누락 (핵심 점·곡선만 맞으면 OK)',
          '- 점 라벨 1-2개 누락 또는 추가',
          '- **각도 호(∠θ 표시), 영역 label(S₁/S₂/f(θ)/g(θ)), 텍스트 주석 누락** — 보조 표시는 통과',
          '- 선이 연장선이 아닌 segment 로 표현되는 등 표현 방식 차이',
          '',
          '판정:',
          '- 다시 그릴 사유 없음 → 정확히 `[검증 통과]` 한 줄만 응답 (다른 텍스트 X)',
          '- 부호/종류 오류 있음 → 1줄로 어긋난 항목 짚고 수정된 ```geometry``` emit',
        ].join('\n');
        appendTurn({ role: 'user', content: checkMsg });
        const checkText = await callLLM(rawHistory);
        finalizeAssistant(checkText, checkText);

        // visual check 결과에 python 블록이 있으면 → 좌표 자체가 틀렸다는 신호.
        // 재계산 cycle 한 번 더 (sympy 실행 → [자동 계산 결과] inject → geometry 재emit)
        const recalcPy = checkText.match(/```(?:python|py|sympy)\s*\n([\s\S]*?)```/);
        if (recalcPy) {
          const sympyResult = await runSympy(recalcPy[1]);
          const failed = /\[VERIFY FAIL\]/.test(sympyResult.stdout);
          const prefix = failed ? '[자동 계산 결과 — 검증 실패]' : '[자동 계산 결과]';
          const tail = failed
            ? '\n\n위 [VERIFY FAIL] 항목을 확인하고 단계 정의를 다시 읽고 좌표를 재계산.'
            : '\n\n위 출력의 점 좌표를 글자 그대로 ```geometry``` spec 에 옮겨 재emit.';
          const injected = `${prefix}\n\`\`\`\n${sympyResult.stdout}\n\`\`\`${tail}`;
          appendTurn({ role: 'user', content: injected });
          const finalText = await callLLM(rawHistory);
          finalizeAssistant(finalText);
        }
      }
    } finally {
      setStreaming(false);
    }
  }, [input, pending, streaming, messages, slug, model, collection, byokActive, byokApiKey, byokModel, byokBaseURL]);

  // 이미지 첨부 — prepareImage 후 needsCrop 이면 크롭 모달, 아니면 바로 pending.
  const addFile = useCallback(async (files: File[]) => {
    if (!files.length) return;
    if (byokActive && isVisionDisabled(byokModel)) {
      setImgError('현재 모델은 이미지를 못 읽어요 — 비전 지원 모델(claude/gemini 등)로 바꾸거나 기본 모드를 쓰세요.');
      return;
    }
    if (pending.length) { setImgError('이미지는 한 번에 하나만 첨부할 수 있어요.'); return; }
    if (files.length > 1) setImgError('이미지는 한 장만 첨부돼요 (첫 장만 사용).');
    try {
      const p = await prepareImage(files[0]);
      if (p.kind === 'needsCrop') { setCropSrc(p.rawDataUrl); setImgError(null); }
      else { setPending(p.tiles); setPendingDisplay(p.display); setImgError(null); }   // 타일=전송, display=표시
    } catch (e) {
      setImgError(e instanceof Error ? e.message : '이미지 처리에 실패했어요.');
    }
  }, [byokActive, byokModel, pending]);

  // send() identity changes whenever messages/input/streaming change. The
  // window event handler below would otherwise capture a stale send.
  const sendRef = useRef(send);
  useEffect(() => { sendRef.current = send; }, [send]);

  // promote() 는 클릭 시점의 최신 messages 만 있으면 된다. messages 를 useCallback deps
  // 에 넣으면 스트리밍 토큰마다 promote 정체성이 바뀌고, 그게 모든 <Message> 의 onPromote
  // prop 을 흔들어 memo 를 전 메시지에서 깨뜨린다(긴 채팅 스크롤 버벅임의 회귀 원인 —
  // 3881d211 의 memo 최적화가 스트리밍 경로에서 무력화됨). ref 로 최신값을 읽어 promote 를
  // 안정화 → memo 유지.
  const messagesRef = useRef(messages);
  useEffect(() => { messagesRef.current = messages; }, [messages]);

  // LearningNoteButton (우측 카드) → 학습 노트 작성 요청. 입력창을 거치지 않고
  // 곧장 send() 로 user message 전송 (override 인자 — input 비우지 않음).
  useEffect(() => {
    const onNoteRequest = (e: Event) => {
      const detail = (e as CustomEvent<{ unitTitle?: string }>).detail;
      const title = detail?.unitTitle ?? unitTitle;
      void sendRef.current(buildNoteUserPrompt(title));
    };
    window.addEventListener('math-study:chat-note-request', onNoteRequest as EventListener);
    return () => window.removeEventListener('math-study:chat-note-request', onNoteRequest as EventListener);
  }, [unitTitle]);

  // Followup buttons (📏 더 짧게 등) under a 학습 노트 reply.
  const handleNoteFollowup = useCallback((kind: NoteFollowup) => {
    void sendRef.current(NOTE_FOLLOWUPS[kind]);
  }, []);

  const promote = useCallback(
    async (idx: number) => {
      const msgs = messagesRef.current;
      const assistant = msgs[idx];
      if (!assistant || assistant.role !== 'assistant') return;
      // Find the preceding user question — skip internal protocol messages
      // ([자동 계산 결과], [자동 계산 결과 — 검증 실패], [시각 검증]) that the
      // sympy/visual-verification loop pushes as user messages, so the real
      // student question is captured instead of an internal protocol string.
      let question = '';
      for (let i = idx - 1; i >= 0; i--) {
        if (msgs[i].role === 'user') {
          const c = msgs[i].content;
          if (c.startsWith('[자동 계산 결과') || c.startsWith('[시각 검증]')) continue;
          question = c;
          break;
        }
      }
      // 학습 노트 요청에서 비롯된 promote 면 파일명에 들어갈 title 을
      // 단원 이름 기반으로 깔끔하게 (`[학습 노트 요청] ...` 본문이
      // 그대로 들어가지 않게).
      const isNote = isNoteRequest(question);
      const titleOverride = isNote ? `학습 노트 - ${unitTitle}` : undefined;
      try {
        const res = await fetch('/api/promote', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ slug, question, answer: assistant.content, title: titleOverride }),
        });
        const json = await res.json();
        if (!res.ok) throw new Error(json.error ?? `HTTP ${res.status}`);
        setMessages((curr) => {
          const next = [...curr];
          next[idx] = { ...assistant, promoted: { path: json.path } };
          return next;
        });
        // 우측 LearningNoteButton 카드에 "최근 저장: …" 표시용.
        try {
          const recentKey = `math-study:note-last-saved:${collection}:${slug}`;
          const filename = String(json.path).split('/').pop() ?? '';
          window.localStorage.setItem(recentKey, filename);
        } catch { /* ignore */ }
      } catch (e) {
        setError(`저장 실패: ${(e as Error).message}`);
      }
    },
    [slug, unitTitle, collection], // messages 는 messagesRef 로 읽음 — deps 에서 제외해 promote 안정화
  );

  const clearChat = () => {
    if (!confirm('대화를 모두 지울까요?')) return;
    setMessages([]);
    try { window.localStorage.removeItem(STORAGE_PREFIX + storageKey); } catch {}
    saveDbHistory(collection, slug, []); // DB 도 비움
  };

  return (
    <section className={fill ? 'card h-full flex flex-col min-h-0' : 'card mt-6'}>
      <header className="flex items-center justify-between mb-3 shrink-0">
        <div>
          <h3 className="text-sm font-semibold">{collection === 'dashboard' ? '🧭 학습 길잡이' : '🤖 튜터 대화'}</h3>
          <p className="text-xs text-[color:var(--color-muted)]">
            {subtitle} 대화는 이 브라우저(localStorage)에 저장.
          </p>
        </div>
        <div className="flex items-center gap-2 text-xs">
          {/* BYOK 활성 시 학생 모델 표시, dev fallback 모드면 claude select */}
          {byokActive ? (
            <span className="bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 rounded px-2 py-1 text-[10px] font-mono"
                  title={byokBaseURL}>
              {isOllamaLike ? '🖥 ' : ''}{byokModel}
            </span>
          ) : (
            <select
              value={model}
              onChange={(e) => setModel(e.target.value as 'haiku' | 'sonnet')}
              className="bg-[color:var(--color-surface)] border border-[color:var(--color-border)] rounded px-2 py-1 text-xs text-zinc-300 focus:outline-none focus:border-indigo-400"
            >
              <option value="haiku">claude-haiku</option>
              <option value="sonnet">claude-sonnet</option>
            </select>
          )}
          <button
            onClick={() => setByokOpen((v) => !v)}
            title="내 API 키 설정"
            className={`text-[10px] tracking-wider px-2 py-1 rounded transition ${
              byokOpen ? 'bg-indigo-500/20 text-indigo-300' : 'text-zinc-500 hover:text-zinc-200'
            }`}
          >
            ⚙ {byokActive ? '내 키' : '설정'}
          </button>
          {messages.length > 0 && (
            <button
              onClick={clearChat}
              className="text-[10px] uppercase tracking-wider text-zinc-500 hover:text-rose-400 transition"
            >
              지우기
            </button>
          )}
        </div>
      </header>

      {byokOpen && (
        <div className="mb-3 rounded-lg border border-indigo-500/30 bg-indigo-500/5 p-3 space-y-2 text-xs">
          <div className="flex items-baseline justify-between">
            <p className="font-semibold text-zinc-200">🔑 내 API 키 설정</p>
            <span className="text-[10px] text-zinc-500">이 기기에만 저장</span>
          </div>

          {/* Provider preset 칩 */}
          <div className="flex flex-wrap gap-1">
            <button
              onClick={() => {
                setByokBaseURL('https://openrouter.ai/api/v1');
                setByokModel('anthropic/claude-haiku-4.5');
              }}
              className="text-[10px] px-2 py-1 rounded bg-zinc-800 text-zinc-300 hover:bg-indigo-500/20 hover:text-indigo-300"
            >☁ OpenRouter</button>
            <button
              onClick={() => {
                setByokBaseURL('http://localhost:11434/v1');
                setByokModel('gemma4:e4b-it-q4_K_M');
                setByokApiKey('ollama');
              }}
              className="text-[10px] px-2 py-1 rounded bg-zinc-800 text-zinc-300 hover:bg-emerald-500/20 hover:text-emerald-300"
            >🖥 Ollama (localhost)</button>
            <button
              onClick={() => {
                const cur = prompt('Tailscale 의 본인 맥북/PC IP 를 입력하세요 (예: 100.79.230.49)', '100.');
                if (cur && /^100\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$/.test(cur.trim())) {
                  setByokBaseURL(`http://${cur.trim()}:11434/v1`);
                  setByokModel('gemma4:e4b-it-q4_K_M');
                  setByokApiKey('ollama');
                }
              }}
              className="text-[10px] px-2 py-1 rounded bg-zinc-800 text-zinc-300 hover:bg-emerald-500/20 hover:text-emerald-300"
              title="Tailscale IP 입력 후 자동 설정"
            >🖥 Ollama (Tailscale)</button>
          </div>

          {/* base URL */}
          <div className="flex gap-2 items-center">
            <label className="text-[11px] text-zinc-400 shrink-0 w-14">URL</label>
            <input
              type="text"
              value={byokBaseURL}
              onChange={(e) => setByokBaseURL(e.target.value)}
              placeholder="https://openrouter.ai/api/v1"
              className="flex-1 bg-[color:var(--color-surface-2)] border border-[color:var(--color-border)] rounded px-2 py-1.5 text-xs font-mono text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-indigo-400"
            />
          </div>

          {/* API key */}
          <div className="flex gap-2 items-center">
            <label className="text-[11px] text-zinc-400 shrink-0 w-14">API key</label>
            <input
              type="password"
              value={byokApiKey}
              onChange={(e) => setByokApiKey(e.target.value)}
              placeholder={isOllamaLike ? '(Ollama 는 불필요)' : 'sk-or-v1-...'}
              className="flex-1 bg-[color:var(--color-surface-2)] border border-[color:var(--color-border)] rounded px-2 py-1.5 text-xs font-mono text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-indigo-400"
            />
          </div>

          {/* model */}
          <div className="flex gap-2 items-center">
            <label className="text-[11px] text-zinc-400 shrink-0 w-14">모델</label>
            <input
              type="text"
              value={byokModel}
              onChange={(e) => setByokModel(e.target.value)}
              placeholder="anthropic/claude-haiku-4.5"
              className="flex-1 bg-[color:var(--color-surface-2)] border border-[color:var(--color-border)] rounded px-2 py-1.5 text-xs font-mono text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-indigo-400"
            />
          </div>
          <div className="flex flex-wrap gap-1 pt-1">
            <span className="text-[10px] text-zinc-500 self-center mr-1">모델 빠른 선택:</span>
            {(isOllamaLike
              ? ['gemma4:e4b-it-q4_K_M', 'gemma4:e2b', 'gemma4:26b', 'gemma3:4b', 'llama3.2-vision:11b', 'qwen2.5-vl:7b']
              : ['anthropic/claude-haiku-4.5', 'google/gemini-2.5-flash', 'openai/gpt-5-mini', 'openrouter/auto']
            ).map((id) => (
              <button key={id} onClick={() => setByokModel(id)}
                      className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-zinc-800 text-zinc-400 hover:bg-zinc-700 hover:text-zinc-200">
                {id}
              </button>
            ))}
          </div>

          {!isOllamaLike && (
            <p className="text-[10px] text-zinc-500 leading-relaxed pt-1">
              💡 OpenRouter key 는 <a href="https://openrouter.ai/keys" target="_blank" rel="noreferrer"
                                       className="text-indigo-400 hover:text-indigo-300 underline">openrouter.ai/keys</a> 에서 발급
            </p>
          )}
          {isOllamaLike && (
            <p className="text-[10px] text-zinc-500 leading-relaxed pt-1">
              💡 Ollama 사용: 맥북·PC 에 <code className="text-zinc-300">ollama serve</code> 띄우고 모델 pull (예: <code className="text-zinc-300">ollama pull gemma4:e4b-it-q4_K_M</code>).
              Tailscale 로 원격 접속 시 <code className="text-zinc-300">OLLAMA_HOST=0.0.0.0 ollama serve</code> 후 본인 tailnet IP 입력.
            </p>
          )}

          <div className="flex justify-end gap-2 pt-1">
            <button
              onClick={() => { saveByok('', byokModel, 'https://openrouter.ai/api/v1'); setByokOpen(false); }}
              className="text-[11px] text-zinc-500 hover:text-rose-400 px-2"
            >리셋 (dev fallback)</button>
            <button
              onClick={() => { saveByok(byokApiKey, byokModel, byokBaseURL); setByokOpen(false); }}
              disabled={!byokBaseURL.trim() || (!isOllamaLike && !byokApiKey.trim())}
              className="text-[11px] px-3 py-1 rounded bg-indigo-500/20 border border-indigo-500/40 text-indigo-300 hover:bg-indigo-500/30 disabled:opacity-40"
            >저장</button>
          </div>
        </div>
      )}

      <div
        ref={scrollRef}
        className={`chat-scroll ${fill ? 'flex-1 min-h-0' : 'max-h-[420px]'} space-y-3 overflow-y-auto py-2 px-1 -mx-1 mb-3 scroll-smooth`}
      >
        {messages.length === 0 ? (
          <p className="text-sm text-[color:var(--color-subtle)] py-8 text-center">
            {collection === 'dashboard'
              ? '무엇이 헷갈리는지 / 어디서 막혔는지 알려주세요.'
              : `"${unitTitle}"에 대해 무엇이든 물어보세요.`}
            <br />
            <span className="text-[color:var(--color-accent)]">{placeholderHint}</span>
          </p>
        ) : (
          messages.map((m, i) => (
            <Message
              key={i}
              msg={m}
              index={i}
              busy={streaming}
              isStreaming={streaming && i === messages.length - 1}
              isNoteResponse={
                m.role === 'assistant'
                && i > 0
                && messages[i - 1].role === 'user'
                && isNoteRequest(messages[i - 1].content)
              }
              slug={slug}
              collection={collection}
              onPromote={promote}
              onNoteFollowup={handleNoteFollowup}
            />
          ))
        )}
        {streaming && messages[messages.length - 1]?.content === '' && (
          <div className="flex items-center gap-2 text-xs text-[color:var(--color-muted)] pl-2">
            <span className="inline-block size-1.5 rounded-full bg-[color:var(--color-accent)] animate-pulse"></span>
            <span>답변 생성 중…</span>
          </div>
        )}
      </div>

      {error && (
        <p className="text-xs text-rose-400 mb-2">⚠ {error}</p>
      )}

      {(pending.length > 0 || imgError) && (
        <div className="flex items-center gap-2 mb-2 shrink-0">
          {pending.length > 0 && (
            <div className="relative">
              <img src={pendingDisplay ?? pending[0]} alt="첨부 이미지" className="h-14 w-14 object-cover rounded border border-[color:var(--color-border)]" />
              <button
                type="button"
                onClick={() => { setPending([]); setPendingDisplay(null); setImgError(null); }}
                className="absolute -top-1.5 -right-1.5 size-5 rounded-full bg-zinc-900 border border-zinc-600 text-zinc-300 text-xs grid place-items-center hover:text-white"
                aria-label="첨부 제거"
              >×</button>
            </div>
          )}
          {imgError && <p className="text-xs text-rose-400">⚠ {imgError}</p>}
        </div>
      )}

      <div
        className={`flex gap-2 items-stretch shrink-0 rounded-lg transition ${dragOver ? 'ring-2 ring-indigo-400/60' : ''}`}
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={(e) => { e.preventDefault(); setDragOver(false); void addFile(imagesFromDataTransfer(e.dataTransfer)); }}
      >
        <textarea
          ref={textareaRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onPaste={(e) => {
            const imgs = imagesFromDataTransfer(e.clipboardData);
            if (imgs.length) { e.preventDefault(); void addFile(imgs); }
          }}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
              e.preventDefault();
              send();
            }
          }}
          placeholder="질문을 입력하세요. (⌘/Ctrl+Enter로 전송 · 이미지 붙여넣기/드래그)"
          rows={2}
          disabled={streaming}
          className="flex-1 min-h-[3.5rem] bg-[color:var(--color-surface-2)] border border-[color:var(--color-border)] rounded-lg px-3 py-2 text-sm text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-indigo-400 resize-y"
        />
        <input
          ref={fileInputRef}
          type="file"
          accept="image/png,image/jpeg,image/webp,image/heic,image/heif"
          className="hidden"
          onChange={(e) => { void addFile(Array.from(e.target.files ?? [])); e.target.value = ''; }}
        />
        <div className="flex flex-col gap-1.5 self-start">
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            disabled={streaming}
            title="이미지 첨부 (그래프·수식 캡처)"
            className="px-2.5 py-1.5 rounded border text-xs transition bg-[color:var(--color-surface-2)] border-[color:var(--color-border)] text-zinc-400 hover:text-zinc-100"
          >🖼 이미지</button>
          <button
            type="button"
            onClick={() => setMathOpen((v) => !v)}
            disabled={streaming}
            title="수식 입력 (LaTeX)"
            className={`px-2.5 py-1.5 rounded border text-xs transition ${
              mathOpen
                ? 'bg-indigo-500/30 border-indigo-500/50 text-indigo-200'
                : 'bg-[color:var(--color-surface-2)] border-[color:var(--color-border)] text-zinc-400 hover:text-zinc-100'
            }`}
          >∑ 수식</button>
          <button
            type="button"
            onClick={() => send()}
            disabled={streaming || (!input.trim() && !pending.length)}
            className="px-4 py-2 rounded-lg bg-indigo-500/20 hover:bg-indigo-500/30 border border-indigo-500/40 text-indigo-300 text-sm font-medium transition disabled:opacity-40 disabled:cursor-not-allowed"
          >
            {streaming ? '전송 중…' : '전송'}
          </button>
        </div>
      </div>

      {cropSrc && (
        <ImageCropper
          src={cropSrc}
          onCrop={(dataUrl) => { setPending([dataUrl]); setPendingDisplay(dataUrl); setCropSrc(null); setImgError(null); }}
          onCancel={() => setCropSrc(null)}
        />
      )}

      {mathOpen && (
        <div className="mt-2 rounded-lg border border-indigo-500/30 bg-indigo-500/5 p-2 space-y-2">
          <p className="text-[11px] text-zinc-400 px-1">
            수식 입력 후 <kbd className="px-1 py-0.5 rounded bg-zinc-800 text-zinc-300 text-[10px]">Enter</kbd>로 메시지에 삽입 ($수식$ 형식). 가상 키보드는 우측 하단 아이콘에서.
          </p>
          <MathField
            value={mathLatex}
            onChange={setMathLatex}
            onSubmit={() => insertMath(mathLatex)}
            placeholder="예: \\frac{1}{2} 또는 \\int_0^1 x^2 dx"
            autoFocus
            rows={2}
          />
          <div className="flex justify-end gap-2">
            <button
              onClick={() => { setMathLatex(''); setMathOpen(false); }}
              className="text-[11px] text-zinc-500 hover:text-zinc-200 px-2 py-1"
            >취소</button>
            <button
              onClick={() => insertMath(mathLatex)}
              disabled={!mathLatex.trim()}
              className="text-[11px] px-2.5 py-1 rounded bg-indigo-500/20 border border-indigo-500/40 text-indigo-300 hover:bg-indigo-500/30 disabled:opacity-40"
            >메시지에 삽입</button>
          </div>
        </div>
      )}

      <style>{`
        /* 대화 스크롤 영역 — 스크롤바를 항상 또렷이(manila 에서 기본 thumb 가 배경과 동색이라
           안 보였음). gutter 예약으로 스크롤 생겨도 레이아웃 안 흔들림 + 스크롤 가능함을 명시. */
        .chat-scroll { scrollbar-gutter: stable; scrollbar-width: thin; scrollbar-color: var(--color-border-strong) transparent; overscroll-behavior: contain; }
        .chat-scroll::-webkit-scrollbar { width: 10px; }
        .chat-scroll::-webkit-scrollbar-track { background: transparent; }
        .chat-scroll::-webkit-scrollbar-thumb {
          background: var(--color-border-strong);
          border-radius: 6px;
          border: 2px solid var(--color-surface);
        }
        .chat-scroll::-webkit-scrollbar-thumb:hover { background: var(--color-subtle); }
        .prose-chat p { margin: 0.25rem 0; }
        .prose-chat p:first-child { margin-top: 0; }
        .prose-chat p:last-child { margin-bottom: 0; }
        .prose-chat .chat-md-heading {
          font-weight: 700;
          line-height: 1.3;
          margin: 0.7rem 0 0.3rem;
          color: var(--color-text);
        }
        .prose-chat h4.chat-md-heading { font-size: 1.02em; }
        .prose-chat h5.chat-md-heading { font-size: 0.95em; color: var(--color-muted); }
        .prose-chat .chat-md-heading:first-child { margin-top: 0; }
        .prose-chat code {
          background: rgba(255,255,255,0.08);
          padding: 1px 5px;
          border-radius: 3px;
          font-size: 0.9em;
          font-family: var(--font-mono);
        }
        .prose-chat pre {
          background: rgba(0,0,0,0.4);
          border: 1px solid #27272a;
          border-radius: 6px;
          padding: 0.5rem 0.75rem;
          margin: 0.5rem 0;
          overflow-x: auto;
          font-size: 0.8em;
        }
        .prose-chat pre code { background: none; padding: 0; }
        .prose-chat .katex { color: inherit; }
        /* 좁은 채팅 폭에서 긴 display 수식이 깨지지 않고 가로 스크롤 */
        /* padding 0.35em: 한글 글리프 잉크가 KaTeX 메트릭 박스 위아래로 솟는데
           overflow-y:hidden 이 패딩 경계에서 클립 → 패딩으로 흡수(글자 상단 잘림 방지). */
        .prose-chat .katex-display { margin: 0.5rem 0; overflow-x: auto; overflow-y: hidden; max-width: 100%; padding: 0.35em 0; }
        .prose-chat table {
          border-collapse: collapse;
          margin: 0.6em 0;
          font-size: 0.92em;
          width: auto;
        }
        .prose-chat th, .prose-chat td {
          border: 1px solid var(--color-border);
          padding: 0.3em 0.6em;
          text-align: left;
          vertical-align: top;
        }
        .prose-chat th {
          background: var(--color-surface-2);
          font-weight: 600;
        }
      `}</style>
    </section>
  );
}
