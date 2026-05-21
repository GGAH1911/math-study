import { Component, type ReactNode, useState, useRef, useEffect, useCallback, useMemo } from 'react';
import MathField from './MathField.tsx';
import Graph, { GraphModal, type PlotSpec } from './Graph.tsx';
import Geometry, { type GeomSpec } from './Geometry.tsx';
import Geometry3D, { type Geom3DSpec } from './Geometry3D.tsx';
import Numberline, { type NumberlineSpec } from './Numberline.tsx';
import StatsChart, { type ChartSpec } from './StatsChart.tsx';
import Interactive from './Interactive.tsx';
import PromotionCard from './PromotionCard.tsx';
import type { InteractiveSpec } from '../data/interactive-samples';
import { ensureKatex } from '../lib/mathish';
import { tryParseTable } from '../lib/markdown';
import { runSympyLocal, prewarmPyodide } from '../lib/pyodide-client';

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
};

type Props = {
  slug: string;
  unitTitle: string;
  collection?: 'concepts' | 'problems' | 'dashboard';
};

const STORAGE_PREFIX = 'math-study:chat:';
const MAX_HISTORY_TURNS = 12; // include up to last N messages in API request

function loadHistory(slug: string): ChatMessage[] {
  if (typeof window === 'undefined') return [];
  try {
    const raw = window.localStorage.getItem(STORAGE_PREFIX + slug);
    return raw ? (JSON.parse(raw) as ChatMessage[]) : [];
  } catch {
    return [];
  }
}

function saveHistory(slug: string, msgs: ChatMessage[]): void {
  try {
    window.localStorage.setItem(STORAGE_PREFIX + slug, JSON.stringify(msgs));
  } catch {
    /* quota or disabled — ignore */
  }
}

// Lightweight markdown rendering: bold, italic, code spans, code blocks, paragraphs, KaTeX-aware passthrough.
// Strategy: split paragraphs, wrap code fences as <pre><code>, render inline.
function renderMarkdown(text: string): string {
  const escape = (s: string) =>
    s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const inline = (s: string) =>
    s
      // bold
      .replace(/\*\*([^\n*]+?)\*\*/g, '<strong>$1</strong>')
      // italic (single * or _)
      .replace(/(^|[^*])\*([^\n*]+?)\*(?!\*)/g, '$1<em>$2</em>')
      // inline code
      .replace(/`([^`\n]+?)`/g, '<code>$1</code>');

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
      // (2) string 안 LaTeX backslash (\frac, \alpha, \sqrt 등) — JSON 표준 외 escape → \\
      // JSON 표준 escape: \" \\ \/ \b \f \n \r \t \uXXXX. 그 외 \X 는 invalid.
      out = out.replace(/"((?:[^"\\]|\\.)*)"/g, (_m, inner: string) => {
        const fixed = inner.replace(/\\([^"\\/bfnrtu])/g, '\\\\$1');
        return `"${fixed}"`;
      });
      // (3) JSON value 자리의 raw 수식 (예: 2*1.732, 3*sqrt(2)) → 평가 결과
      // pattern: : <number/expr>[,}\]]  안전한 평가만 (sqrt, *, /, +, -, 괄호, 숫자).
      out = out.replace(/:\s*([0-9][0-9eE.+\-*/\s()]*(?:sqrt|sin|cos|tan|pi)[a-zA-Z0-9_.+\-*/\s()]*)\s*([,}\]])/g,
        (_m, expr: string, tail: string) => {
          try {
            // mathjs 없이 간단 safe-eval — Function 생성. 매우 제한된 패턴만.
            const safe = expr.replace(/sqrt/g, 'Math.sqrt')
              .replace(/sin/g, 'Math.sin').replace(/cos/g, 'Math.cos')
              .replace(/tan/g, 'Math.tan').replace(/pi/g, 'Math.PI');
            const v = Function(`"use strict"; return (${safe});`)();
            if (typeof v === 'number' && Number.isFinite(v)) return `: ${v}${tail}`;
          } catch { /* 평가 실패 — 그대로 (parse 실패 유도) */ }
          return _m;
        });
      // (4) 단순 number * number 같은 raw expression (sqrt 등 함수 없음)
      out = out.replace(/:\s*(-?\d+(?:\.\d+)?\s*[*/]\s*-?\d+(?:\.\d+)?(?:\s*[*/]\s*-?\d+(?:\.\d+)?)*)\s*([,}\]])/g,
        (_m, expr: string, tail: string) => {
          try {
            const v = Function(`"use strict"; return (${expr});`)();
            if (typeof v === 'number' && Number.isFinite(v)) return `: ${v}${tail}`;
          } catch { /* */ }
          return _m;
        });
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
      out.push({ type: 'graph', kind: 'svg', svg: body, raw: m[0] });
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
  renderToString: (tex: string, opts?: { displayMode?: boolean; throwOnError?: boolean }) => string;
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
const LATEX_CMD_RUN = /(\\[A-Za-z]+(?:\{[^}]{0,80}\})*(?:\s+[A-Za-z0-9\-+*/^=.,()|\\{}]+)*)/g;

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
    try { return katex.renderToString(tex, { displayMode: false, throwOnError: true }); }
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
    try { return katex.renderToString(tex, { displayMode: false, throwOnError: true }); }
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
  html = html.replace(/\$\$([^$]+?)\$\$/g, (_, tex) => {
    try {
      return katex.renderToString(decodeEntities(tex), { displayMode: true, throwOnError: true });
    } catch {
      return _;
    }
  });
  html = html.replace(/\$([^\n$]+?)\$/g, (_, tex) => {
    try {
      return katex.renderToString(decodeEntities(tex), { displayMode: false, throwOnError: true });
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

function MdSegment({ content }: { content: string }) {
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

function Message({ msg, onPromote, busy, slug, collection, isStreaming }: {
  msg: ChatMessage; onPromote?: () => void; busy?: boolean;
  slug: string; collection: 'concepts' | 'problems' | 'dashboard';
  isStreaming?: boolean;
}) {
  // 자동 계산 결과 inject 된 user message 는 내부 protocol — 사용자에겐 chip 만 표시.
  const isUser = msg.role === 'user';
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
  const segments = parseGraphSegments(msg.content);
  const [modal, setModal] = useState<ChatModalState | null>(null);
  return (
    <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'}`}>
      <div
        className={`max-w-[92%] rounded-xl px-3.5 py-2 text-sm leading-relaxed space-y-2
          ${isUser
            ? 'bg-indigo-500/10 border border-indigo-500/30 text-zinc-100'
            : 'bg-[color:var(--color-surface-2)] border border-[color:var(--color-border)] text-zinc-100'}`}
      >
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
      {!isUser && onPromote && (
        <button
          onClick={onPromote}
          disabled={busy || !!msg.promoted}
          className={`mt-1 text-[10px] uppercase tracking-wider transition ${
            msg.promoted
              ? 'text-emerald-400 cursor-default'
              : 'text-zinc-500 hover:text-zinc-100 cursor-pointer'
          }`}
        >
          {msg.promoted ? `✓ wiki에 저장됨 (${msg.promoted.path.split('/').pop()})` : '↑ wiki에 영구화 (Promote)'}
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
}

export default function ChatPanel({ slug, unitTitle, collection = 'concepts' }: Props) {
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
  const isOllamaLike = /\/\/(localhost|127\.0\.0\.1|100\.|0\.0\.0\.0|192\.168\.|10\.)/.test(byokBaseURL);
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

  // Load history on mount
  useEffect(() => {
    setMessages(loadHistory(storageKey));
    // pyodide worker 선제 로드 — 첫 sympy 호출 시 대기 ↓
    prewarmPyodide();
  }, [storageKey]);

  // Persist on every change
  useEffect(() => {
    if (messages.length > 0) saveHistory(storageKey, messages);
  }, [storageKey, messages]);

  // Auto-scroll to bottom on new content
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const send = useCallback(async () => {
    const text = input.trim();
    if (!text || streaming) return;
    setError(null);
    setInput('');

    const newUserMsg: ChatMessage = { role: 'user', content: text };
    const placeholder: ChatMessage = { role: 'assistant', content: '' };
    setMessages([...messages, newUserMsg, placeholder]);
    setStreaming(true);

    // python block 을 채팅창에 노출하지 않기 위한 display sanitize.
    // python block 만 있는 응답은 chip 으로, geometry 등 다른 본문이 있으면 그대로.
    const sanitizeForDisplay = (s: string) => {
      const stripped = s.replace(/```(?:python|py|sympy)[\s\S]*?```/g, '').trim();
      const hadPy = stripped !== s.trim();
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
      const extractPy = (s: string) => s.match(/```(?:python|py|sympy)\s*\n([\s\S]*?)```/);
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
  }, [input, streaming, messages, slug, model, collection, byokActive, byokApiKey, byokModel, byokBaseURL]);

  const promote = useCallback(
    async (idx: number) => {
      const assistant = messages[idx];
      if (!assistant || assistant.role !== 'assistant') return;
      // Find the preceding user question
      let question = '';
      for (let i = idx - 1; i >= 0; i--) {
        if (messages[i].role === 'user') {
          question = messages[i].content;
          break;
        }
      }
      try {
        const res = await fetch('/api/promote', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ slug, question, answer: assistant.content }),
        });
        const json = await res.json();
        if (!res.ok) throw new Error(json.error ?? `HTTP ${res.status}`);
        setMessages((curr) => {
          const next = [...curr];
          next[idx] = { ...assistant, promoted: { path: json.path } };
          return next;
        });
      } catch (e) {
        setError(`Promote 실패: ${(e as Error).message}`);
      }
    },
    [messages, slug],
  );

  const clearChat = () => {
    if (!confirm('대화를 모두 지울까요?')) return;
    setMessages([]);
    try { window.localStorage.removeItem(STORAGE_PREFIX + storageKey); } catch {}
  };

  return (
    <section className="card mt-6">
      <header className="flex items-center justify-between mb-3">
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
            title="API key 설정 (BYOK)"
            className={`text-[10px] uppercase tracking-wider px-2 py-1 rounded transition ${
              byokOpen ? 'bg-indigo-500/20 text-indigo-300' : 'text-zinc-500 hover:text-zinc-200'
            }`}
          >
            ⚙ {byokActive ? 'BYOK' : '설정'}
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
            <p className="font-semibold text-zinc-200">🔑 BYOK — LLM provider 설정</p>
            <span className="text-[10px] text-zinc-500">localStorage 에만 저장</span>
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
        className="space-y-3 max-h-[420px] overflow-y-auto py-2 px-1 -mx-1 mb-3 scroll-smooth"
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
              busy={streaming}
              isStreaming={streaming && i === messages.length - 1}
              slug={slug}
              collection={collection}
              onPromote={m.role === 'assistant' && m.content.trim().length > 0 && !streaming ? () => promote(i) : undefined}
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

      <div className="flex gap-2 items-end">
        <textarea
          ref={textareaRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
              e.preventDefault();
              send();
            }
          }}
          placeholder="질문을 입력하세요. (⌘/Ctrl+Enter로 전송)"
          rows={2}
          disabled={streaming}
          className="flex-1 bg-[color:var(--color-surface-2)] border border-[color:var(--color-border)] rounded-lg px-3 py-2 text-sm text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-indigo-400 resize-none"
        />
        <div className="flex flex-col gap-1.5">
          <button
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
            onClick={send}
            disabled={streaming || !input.trim()}
            className="px-4 py-2 rounded-lg bg-indigo-500/20 hover:bg-indigo-500/30 border border-indigo-500/40 text-indigo-300 text-sm font-medium transition disabled:opacity-40 disabled:cursor-not-allowed"
          >
            {streaming ? '전송 중…' : '전송'}
          </button>
        </div>
      </div>

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
        .prose-chat p { margin: 0.25rem 0; }
        .prose-chat p:first-child { margin-top: 0; }
        .prose-chat p:last-child { margin-bottom: 0; }
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
        .prose-chat .katex-display { margin: 0.5rem 0; }
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
