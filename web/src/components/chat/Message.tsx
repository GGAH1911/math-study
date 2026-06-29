// 튜터 메시지 렌더링 클러스터 — ChatPanel 에서 분리(동작 무변). 메시지 1건의 표시(마크다운·수식·
// 그래프/도형/3D/수직선/차트/인터랙티브 세그먼트·인용칩·드래그인용 버튼·에러바운더리·모달).
import { Component, memo, type ReactNode, useState, useRef, useEffect, useCallback, useMemo } from 'react';
import Graph, { GraphModal, type PlotSpec } from '../Graph.tsx';
import Geometry, { type GeomSpec } from '../Geometry.tsx';
import Geometry3D, { type Geom3DSpec } from '../Geometry3D.tsx';
import Numberline, { type NumberlineSpec } from '../Numberline.tsx';
import StatsChart, { type ChartSpec } from '../StatsChart.tsx';
import Interactive from '../Interactive.tsx';
import PromotionCard from '../PromotionCard.tsx';
import type { InteractiveSpec } from '../../data/interactive-samples';
import { renderMarkdown, latexFromSelection } from '../../lib/chat/markdown';
import { ensureKatex, renderMathSegments } from '../../lib/mathish';
import type { NoteFollowup } from '../../lib/note-prompts';
import type { ChatMessage } from '../../lib/chat/types';

type ChatModalState =
  | { kind: 'plot' | 'svg'; spec?: PlotSpec; svg?: string }
  | { kind: 'geom'; geomSpec: GeomSpec }
  | { kind: 'geom3d'; geom3dSpec: Geom3DSpec }
  | { kind: 'numberline'; numberlineSpec: NumberlineSpec }
  | { kind: 'chart'; chartSpec: ChartSpec }
  | { kind: 'interactive'; interactiveSpec: InteractiveSpec };

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

// KaTeX 렌더는 lib/katex-normalize 의 공유 renderMathSegments 로 일원화(SSOT).
// (구) 로컬 applyKatex/recoverBareMath/decodeEntities/상수는 그쪽으로 이전 — 챗은
// renderMathSegments(html, k, {htmlInput:true, recoverBare:true}) 호출로 동일 동작.

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



// 인용 칩 — 렌더 수식 채팅을 복붙해 삽입한 내용을 마스킹 표시(탭하면 펼쳐 미리보기, 수식 렌더).
export function QuotedChip({ text, onRemove }: { text: string; onRemove?: () => void }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="mb-1.5 w-full">
      <div className="flex items-center gap-1.5 text-[11px] text-zinc-400 bg-zinc-700/30 border border-zinc-600/60 rounded-lg px-2 py-1">
        <button type="button" onClick={() => setOpen((v) => !v)} className="flex items-center gap-1.5 flex-1 min-w-0 text-left hover:text-zinc-200">
          <span aria-hidden="true">📋</span>
          <span className="truncate">채팅 내용 삽입됨</span>
          <span className="text-zinc-500" aria-hidden="true">{open ? '접기 ▴' : '미리보기 ▾'}</span>
        </button>
        {onRemove && (
          <button type="button" onClick={onRemove} title="삭제" className="text-zinc-500 hover:text-rose-300 shrink-0">✕</button>
        )}
      </div>
      {open && (
        <div className="mt-1 max-h-48 overflow-y-auto rounded-lg border border-zinc-700/60 bg-zinc-800/40 px-2.5 py-2">
          <MdSegment content={text} />
        </div>
      )}
    </div>
  );
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
      if (k && !cancelled) setHtml(renderMathSegments(baseHtml, k, { htmlInput: true, recoverBare: true }));
    })();
    return () => { cancelled = true; };
  }, [baseHtml]);
  return <div className="prose-chat" dangerouslySetInnerHTML={{ __html: html }} />;
}

// Memoized so the message list doesn't re-render on every keystroke in the
// chat input. `onPromote` now receives the message index — passing a stable
// callback from the parent keeps prop identity steady, which lets `memo`
// actually skip rerenders.
const Message = memo(function Message({ msg, index, onPromote, onNoteFollowup, onQuote, busy, slug, collection, isStreaming, isNoteResponse }: {
  msg: ChatMessage; index: number;
  onPromote?: (idx: number) => void;
  onNoteFollowup?: (kind: NoteFollowup) => void;
  onQuote?: (latex: string) => void;
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
  // 드래그 선택 → "인용" 버튼 + 직접 그린 하이라이트(네이티브 ::selection 은 iPad touchend 시 OS 가
  //   지우고, 데스크탑은 포커스 이탈 시 비활성렌더돼 신뢰 불가 → 선택 rects 를 오버레이로 직접 그린다).
  const bodyRef = useRef<HTMLDivElement | null>(null);
  const [quoteBtn, setQuoteBtn] = useState<{ x: number; y: number; below: boolean; latex: string; hl: { left: number; top: number; w: number; h: number }[] } | null>(null);
  const updateQuoteBtn = useCallback(() => {
    if (!onQuote || isUser) return;
    const sel = window.getSelection();
    const body = bodyRef.current;
    if (!sel || sel.isCollapsed || !body) { setQuoteBtn(null); return; }
    const range = sel.getRangeAt(0);
    if (!body.contains(range.commonAncestorContainer)) { setQuoteBtn(null); return; }
    const latex = latexFromSelection(range, body);
    if (!latex.trim()) { setQuoteBtn(null); return; }
    // 버튼·하이라이트는 data-mi 래퍼(position:relative) 안에 있으므로 좌표도 그 래퍼 기준.
    const wrap = body.closest('[data-mi]') as HTMLElement | null;
    const wrapRect = (wrap ?? body).getBoundingClientRect();
    const rects = Array.from(range.getClientRects());
    const hl = rects.map((r) => ({ left: r.left - wrapRect.left, top: r.top - wrapRect.top, w: r.width, h: r.height }));
    const last = rects.length ? rects[rects.length - 1] : range.getBoundingClientRect();
    // ★터치기기(coarse): 네이티브 선택 툴바가 선택 위를 가리므로 버튼을 선택 *아래*에 둔다.
    //   데스크탑: 선택 끝 위쪽(기존). below 플래그로 버튼 transform 분기.
    const coarse = typeof window !== 'undefined' && window.matchMedia?.('(pointer: coarse)')?.matches === true;
    setQuoteBtn({
      x: Math.max(28, Math.min(last.right - wrapRect.left, wrapRect.width - 28)),
      y: coarse ? last.bottom - wrapRect.top + 8 : last.top - wrapRect.top - 6,
      below: coarse,
      latex,
      hl,
    });
  }, [onQuote, isUser]);
  // 모바일/태블릿: 롱프레스 선택은 touchend *후* 네이티브 핸들로 이뤄져 onTouchEnd 핸들러는 빈 선택만
  //   본다. selectionchange 로 실제 선택 완료·핸들 조정 시 버튼을 띄운다. (★닫기는 안 함 — 선택 해제/
  //   collapse 시엔 return 만. iPad 가 touchend 후 선택을 자동으로 지우는 순간 같이 닫히는 사고 방지.
  //   닫기는 기존 pointerdown 경로가 담당.)
  useEffect(() => {
    if (!onQuote || isUser) return;
    let t = 0;
    // ★디바운스 필수: 드래그로 선택 범위를 넓히는 동안 selectionchange 가 매 프레임 발화한다.
    //   거기서 곧장 updateQuoteBtn 하면 버튼·오버레이 DOM 이 매 프레임 재생성(churn)돼 네이티브
    //   선택 드래그 제스처가 끊긴다("드래그 선택 안됨"). → 선택이 멈춘 뒤(마지막 변경 후 300ms)에만
    //   버튼을 띄워 드래그 중엔 DOM 을 안 건드린다.
    const onSelChange = () => {
      window.clearTimeout(t);
      t = window.setTimeout(() => {
        const sel = window.getSelection();
        const body = bodyRef.current;
        if (!sel || sel.isCollapsed || sel.rangeCount === 0 || !body) return;
        if (!body.contains(sel.getRangeAt(0).commonAncestorContainer)) return; // 이 메시지 밖 선택 무시
        updateQuoteBtn();
      }, 300);
    };
    document.addEventListener('selectionchange', onSelChange);
    return () => { document.removeEventListener('selectionchange', onSelChange); window.clearTimeout(t); };
  }, [onQuote, isUser, updateQuoteBtn]);
  // 새 포인터 down(다른 곳 클릭/새 드래그 시작) 때 인용 버튼·하이라이트 닫기. ★selectionchange 로 닫으면
  //   iPad 가 touchend 후 선택을 자동으로 지우는 순간 같이 닫혀버리므로(우리 오버레이의 존재 이유와 충돌)
  //   포인터 down 으로만 dismiss — 버튼 자신을 누른 경우는 onClick 이 먼저 처리하므로 제외.
  useEffect(() => {
    if (!quoteBtn) return;
    const onDown = (e: Event) => {
      const t = e.target as HTMLElement;
      if (t?.closest?.('[data-quote-btn]')) return;   // 인용 버튼 클릭은 onClick 이 처리
      setQuoteBtn(null);
    };
    // 캡처 단계 + 약간 지연(현재 mouseup/touchend 와 같은 틱에 닫히지 않게).
    const id = window.setTimeout(() => {
      document.addEventListener('pointerdown', onDown, true);
    }, 0);
    return () => { clearTimeout(id); document.removeEventListener('pointerdown', onDown, true); };
  }, [quoteBtn]);
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
    <div data-mi={index} className={`relative flex flex-col ${isUser ? 'items-end' : 'items-start'}`}>
      {quoteBtn && (<>
        {/* 직접 그린 선택 하이라이트 — 네이티브 선택이 지워져도 무엇을 골랐는지 보인다. */}
        {quoteBtn.hl.map((r, i) => (
          <div key={i} aria-hidden="true" style={{ position: 'absolute', left: r.left, top: r.top, width: r.w, height: r.h, background: 'rgba(79,70,229,0.32)', borderRadius: 2, pointerEvents: 'none', zIndex: 20 }} />
        ))}
        <button
          type="button"
          data-quote-btn
          onMouseDown={(e) => { e.preventDefault(); }}
          onClick={() => { onQuote?.(quoteBtn.latex); setQuoteBtn(null); window.getSelection()?.removeAllRanges(); }}
          style={quoteBtn.below
            // ★모바일(coarse): 선택 위엔 네이티브 툴바, 아래엔 선택 핸들(물방울)이 떠 둘 다 덮으면
            //   드래그-확장이 막힌다. 그래서 선택과 무관한 고정 위치(입력창 위 중앙)에 띄운다.
            ? { position: 'fixed', left: '50%', bottom: '88px', transform: 'translateX(-50%)', zIndex: 70 }
            : { position: 'absolute', left: quoteBtn.x, top: Math.max(0, quoteBtn.y), transform: 'translate(-100%, -100%)', zIndex: 30 }}
          className={`rounded-full bg-indigo-500 border border-indigo-400 font-medium text-white shadow-lg whitespace-nowrap hover:bg-indigo-400 ${quoteBtn.below ? 'px-4 py-2 text-[13px]' : 'px-2.5 py-1 text-[12px]'}`}
        >💬 선택 인용</button>
      </>)}
      <div
        ref={bodyRef}
        onMouseUp={updateQuoteBtn}
        onTouchEnd={updateQuoteBtn}
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
        {isUser && msg.quoted && (
          <QuotedChip text={msg.quoted} />
        )}
        {/* quoted 동반 user 메시지는 content 에 인용블록이 들어있으므로(LLM용), 표시는 칩 + 사용자 실제 질문만. */}
        {isUser && msg.quoted
          ? <MdSegment content={msg.displayText ?? ''} />
          : segments.map((s, i) => {
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
        {/* (삼항 끝) */}
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

export default Message;
