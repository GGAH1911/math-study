import { useState, useRef, useEffect, useCallback } from 'react';

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
        const escaped = escape(para);
        // Re-instate inline markdown after escape — but escape made angle brackets safe;
        // inline regex only touches *, _, ` so it's still safe.
        parts.push(`<p>${inline(escaped).replace(/\n/g, '<br/>')}</p>`);
      }
    }
  }
  return parts.join('');
}

// KaTeX rendering: process $...$ and $$...$$ in the rendered HTML after markdown.
// Returns HTML with KaTeX spans inserted. Loads katex from CDN on demand.
declare global {
  interface Window {
    katex?: {
      renderToString: (tex: string, opts?: { displayMode?: boolean; throwOnError?: boolean }) => string;
    };
  }
}

async function ensureKatex(): Promise<typeof window.katex | null> {
  if (typeof window === 'undefined') return null;
  if (window.katex) return window.katex;
  // Try dynamic import from same JS bundle — KaTeX is already a dep
  try {
    const mod = await import('katex');
    window.katex = mod.default ?? mod;
    return window.katex;
  } catch {
    return null;
  }
}

function applyKatex(html: string, katex: NonNullable<typeof window.katex>): string {
  // Display $$...$$
  html = html.replace(/\$\$([^$]+?)\$\$/g, (_, tex) => {
    try {
      return katex.renderToString(tex, { displayMode: true, throwOnError: false });
    } catch {
      return _;
    }
  });
  // Inline $...$
  html = html.replace(/\$([^\n$]+?)\$/g, (_, tex) => {
    try {
      return katex.renderToString(tex, { displayMode: false, throwOnError: false });
    } catch {
      return _;
    }
  });
  return html;
}

function Message({ msg, onPromote, busy }: { msg: ChatMessage; onPromote?: () => void; busy?: boolean }) {
  const [html, setHtml] = useState<string>('');
  useEffect(() => {
    let cancelled = false;
    (async () => {
      const k = await ensureKatex();
      let rendered = renderMarkdown(msg.content);
      if (k) rendered = applyKatex(rendered, k);
      if (!cancelled) setHtml(rendered);
    })();
    return () => { cancelled = true; };
  }, [msg.content]);

  const isUser = msg.role === 'user';
  return (
    <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'}`}>
      <div
        className={`max-w-[92%] rounded-xl px-3.5 py-2 text-sm leading-relaxed
          ${isUser
            ? 'bg-indigo-500/10 border border-indigo-500/30 text-zinc-100'
            : 'bg-[color:var(--color-surface-2)] border border-[color:var(--color-border)] text-zinc-100'}`}
      >
        <div
          className="prose-chat"
          dangerouslySetInnerHTML={{ __html: html || msg.content }}
        />
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
  const scrollRef = useRef<HTMLDivElement | null>(null);

  const storageKey = `${collection}:${slug}`;

  // Load history on mount
  useEffect(() => {
    setMessages(loadHistory(storageKey));
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
    const all = [...messages.slice(-MAX_HISTORY_TURNS), newUserMsg];
    setMessages([...messages, newUserMsg, placeholder]);
    setStreaming(true);

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ slug, collection, messages: all, model }),
      });
      if (!res.ok || !res.body) {
        throw new Error(`HTTP ${res.status}`);
      }
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buf = '';
      let assistantText = '';
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        buf += decoder.decode(value, { stream: true });
        // SSE: events separated by blank lines
        let idx;
        while ((idx = buf.indexOf('\n\n')) !== -1) {
          const block = buf.slice(0, idx);
          buf = buf.slice(idx + 2);
          let event = 'message';
          let data = '';
          for (const line of block.split('\n')) {
            if (line.startsWith('event: ')) event = line.slice(7).trim();
            else if (line.startsWith('data: ')) data = line.slice(6);
          }
          if (!data) continue;
          try {
            const parsed = JSON.parse(data);
            if (event === 'delta' && typeof parsed.text === 'string') {
              assistantText += parsed.text;
              setMessages((curr) => {
                const next = [...curr];
                next[next.length - 1] = { role: 'assistant', content: assistantText };
                return next;
              });
            } else if (event === 'error') {
              setError(parsed.message ?? 'unknown error');
            }
          } catch {
            // ignore bad chunk
          }
        }
      }
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setStreaming(false);
    }
  }, [input, streaming, messages, slug, model]);

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
          <select
            value={model}
            onChange={(e) => setModel(e.target.value as 'haiku' | 'sonnet')}
            className="bg-[color:var(--color-surface)] border border-[color:var(--color-border)] rounded px-2 py-1 text-xs text-zinc-300 focus:outline-none focus:border-indigo-400"
          >
            <option value="haiku">claude-haiku</option>
            <option value="sonnet">claude-sonnet</option>
          </select>
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
        <button
          onClick={send}
          disabled={streaming || !input.trim()}
          className="px-4 py-2 rounded-lg bg-indigo-500/20 hover:bg-indigo-500/30 border border-indigo-500/40 text-indigo-300 text-sm font-medium transition disabled:opacity-40 disabled:cursor-not-allowed"
        >
          {streaming ? '전송 중…' : '전송'}
        </button>
      </div>

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
      `}</style>
    </section>
  );
}
