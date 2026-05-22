// NotesPanel — concept/problem 페이지 우측 aside에 마운트.
// 학생이 그 페이지에서 LLM과 나눈 대화를 바탕으로 LLM 튜터가 정리된 학습
// 노트를 만들어 주고, localStorage에 즉시 영속 + 선택적으로 docs/notes/
// 파일로도 영구 저장 (다기기/git 추적).
//
// 노트는 매 생성마다 timestamp 헤더와 함께 누적(append) — 학생이 시간순
// 학습 흔적을 따라가도록.

import { useEffect, useState } from 'react';
import { ensureKatex } from '../lib/mathish';
import { parseTableBlock } from '../lib/markdown';

type Collection = 'concepts' | 'problems';
type Props = {
  slug: string;
  collection?: Collection;
};

type ChatMessage = { role: 'user' | 'assistant'; content: string };

const CHAT_PREFIX = 'math-study:chat:';
const NOTE_PREFIX = 'math-study:note:';

function loadChat(storageKey: string): ChatMessage[] {
  if (typeof window === 'undefined') return [];
  try {
    const raw = window.localStorage.getItem(CHAT_PREFIX + storageKey);
    return raw ? (JSON.parse(raw) as ChatMessage[]) : [];
  } catch { return []; }
}

function loadNoteLS(storageKey: string): string {
  if (typeof window === 'undefined') return '';
  try {
    const newKey = NOTE_PREFIX + storageKey;
    const direct = window.localStorage.getItem(newKey);
    if (direct) return direct;
    // sub-dir 진입 후 lazy migration — 'concepts:algebra/근의_공식' 가 비면
    // 기존 'concepts:근의_공식' 의 노트를 복사 후 삭제.
    if (storageKey.includes('/')) {
      const leaf = storageKey.split('/').pop() ?? storageKey;
      const colon = storageKey.indexOf(':');
      const legacyKey = NOTE_PREFIX + (colon >= 0 ? storageKey.slice(0, colon + 1) + leaf : leaf);
      const legacy = window.localStorage.getItem(legacyKey);
      if (legacy) {
        window.localStorage.setItem(newKey, legacy);
        window.localStorage.removeItem(legacyKey);
        return legacy;
      }
    }
    return '';
  }
  catch { return ''; }
}

function saveNoteLS(storageKey: string, content: string): void {
  try { window.localStorage.setItem(NOTE_PREFIX + storageKey, content); }
  catch { /* quota — surface elsewhere */ }
}

function tsHeader(): string {
  const d = new Date();
  const pad = (n: number) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

// 간단한 markdown 렌더 (KaTeX 포함 X — 일단 raw markdown 표시. KaTeX는 추후
// MathishText 적용 가능). 1차로 백틱·헤딩 등 기본만.
function renderMarkdown(text: string): string {
  const escape = (s: string) =>
    s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const lines = text.split('\n');
  const out: string[] = [];
  let inList = false;
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    // 표 detect — 현재 줄이 `|...|` 이고 다음 줄이 alignment row면 표 블록 수집.
    if (/^\s*\|.+\|\s*$/.test(line) && i + 1 < lines.length &&
        /^\s*\|[\s\-:|]+\|\s*$/.test(lines[i + 1])) {
      const tblLines = [line, lines[i + 1]];
      let j = i + 2;
      while (j < lines.length && /^\s*\|.+\|\s*$/.test(lines[j])) {
        tblLines.push(lines[j]);
        j++;
      }
      const html = parseTableBlock(tblLines, (c) => inline(escape(c)));
      if (html) {
        if (inList) { out.push('</ul>'); inList = false; }
        out.push(html);
        i = j;
        continue;
      }
    }
    const heading = line.match(/^(#{1,4})\s+(.*)$/);
    if (heading) {
      if (inList) { out.push('</ul>'); inList = false; }
      const level = heading[1].length;
      out.push(`<h${level} class="font-semibold text-zinc-100 mt-3 mb-1">${escape(heading[2])}</h${level}>`);
      i++; continue;
    }
    const bullet = line.match(/^[-*]\s+(.*)$/);
    if (bullet) {
      if (!inList) { out.push('<ul class="list-disc pl-4 space-y-0.5">'); inList = true; }
      out.push(`<li>${inline(escape(bullet[1]))}</li>`);
      i++; continue;
    }
    if (line.trim() === '---') {
      if (inList) { out.push('</ul>'); inList = false; }
      out.push('<hr class="my-2 border-zinc-800" />');
      i++; continue;
    }
    if (line.trim() === '') {
      if (inList) { out.push('</ul>'); inList = false; }
      i++; continue;
    }
    if (inList) { out.push('</ul>'); inList = false; }
    out.push(`<p class="my-1">${inline(escape(line))}</p>`);
    i++;
  }
  if (inList) out.push('</ul>');
  return out.join('');
}

function inline(s: string): string {
  return s
    .replace(/\*\*([^\n*]+?)\*\*/g, '<strong>$1</strong>')
    .replace(/`([^`\n]+?)`/g, '<code class="text-[color:var(--color-accent)] bg-zinc-900 px-1 rounded">$1</code>')
    // markdown links — keep as plain anchors
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="text-[color:var(--color-accent)] hover:underline">$1</a>');
}

export default function NotesPanel({ slug, collection = 'concepts' }: Props) {
  const storageKey = `${collection}:${slug}`;
  const [note, setNote] = useState<string>('');
  const [busy, setBusy] = useState<'idle' | 'generating' | 'saving'>('idle');
  const [error, setError] = useState<string | null>(null);
  const [toast, setToast] = useState<string | null>(null);

  // localStorage 우선, 없으면 파일에서 GET. 1회만.
  useEffect(() => {
    const ls = loadNoteLS(storageKey);
    if (ls) { setNote(ls); return; }
    (async () => {
      try {
        const r = await fetch(`/api/save-note?slug=${encodeURIComponent(slug)}`);
        const j = await r.json();
        if (j.content) {
          setNote(j.content);
          saveNoteLS(storageKey, j.content);
        }
      } catch { /* 처음 사용자, 파일 없음 — 무시 */ }
    })();
  }, [storageKey, slug]);

  // localStorage에 즉시 영속 — note state가 바뀔 때마다.
  useEffect(() => {
    if (note) saveNoteLS(storageKey, note);
  }, [storageKey, note]);

  // toast 자동 사라짐
  useEffect(() => {
    if (!toast) return;
    const t = setTimeout(() => setToast(null), 3000);
    return () => clearTimeout(t);
  }, [toast]);

  // messageCount는 SSR 시점엔 localStorage 미접근 → 0, client mount 후 실제값.
  // 직접 계산하면 SSR/client hydration mismatch. useState로 분리.
  const [messageCount, setMessageCount] = useState(0);
  useEffect(() => {
    setMessageCount(loadChat(storageKey).length);
    const onStorage = () => setMessageCount(loadChat(storageKey).length);
    window.addEventListener('storage', onStorage);
    return () => window.removeEventListener('storage', onStorage);
  }, [storageKey]);

  const generate = async () => {
    setError(null);
    const messages = loadChat(storageKey);
    if (messages.length < 2) {
      setError('대화가 너무 짧아요. LLM과 좀 더 이야기 한 뒤 다시 시도하세요.');
      return;
    }
    setBusy('generating');
    try {
      const res = await fetch('/api/generate-note', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ slug, collection, messages, model: 'haiku' }),
      });
      const j = await res.json();
      if (!res.ok) throw new Error(j.error ?? `HTTP ${res.status}`);
      const newSection = (note.trim() ? `${note.trim()}\n\n---\n\n` : '')
        + `## 📅 ${tsHeader()} 학습\n\n${(j.note as string).trim()}`;
      setNote(newSection);
      setToast('노트 생성 완료');
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy('idle');
    }
  };

  const saveToFile = async () => {
    if (!note.trim()) return;
    setBusy('saving');
    setError(null);
    try {
      const res = await fetch('/api/save-note', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ slug, content: note, collection }),
      });
      const j = await res.json();
      if (!res.ok) throw new Error(j.error ?? `HTTP ${res.status}`);
      setToast(`저장됨: ${j.path}`);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy('idle');
    }
  };

  const download = () => {
    if (!note.trim()) return;
    const blob = new Blob([`# ${slug} 학습 노트\n\n${note}\n`], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${slug}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const clearNote = () => {
    if (!confirm('이 페이지의 학습 노트를 모두 지울까요? (파일에 저장한 사본은 유지됩니다.)')) return;
    setNote('');
    try { window.localStorage.removeItem(NOTE_PREFIX + storageKey); } catch { /* ignore */ }
    setToast('노트 지움');
  };

  // markdown → KaTeX 두 단계. KaTeX는 비동기 import 후 처리.
  const [noteHtml, setNoteHtml] = useState<string>('');
  useEffect(() => {
    if (!note) { setNoteHtml(''); return; }
    let cancelled = false;
    (async () => {
      let html = renderMarkdown(note);
      const k = await ensureKatex();
      if (k) {
        // $$...$$ (display)
        html = html.replace(/\$\$([^$]+?)\$\$/g, (_, tex) => {
          try { return k.renderToString(tex, { displayMode: true, throwOnError: false }); }
          catch { return _; }
        });
        // $...$  (inline). 단, HTML escape된 형태(&lt; etc)를 KaTeX가 못 다루므로 복원.
        html = html.replace(/\$([^\n$]+?)\$/g, (_, tex) => {
          try {
            const decoded = tex.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>');
            return k.renderToString(decoded, { displayMode: false, throwOnError: false });
          } catch { return _; }
        });
      }
      if (!cancelled) setNoteHtml(html);
    })();
    return () => { cancelled = true; };
  }, [note]);

  return (
    <section className="card">
      <header className="flex items-baseline justify-between mb-2">
        <h3 className="text-xs uppercase tracking-[0.15em] text-[color:var(--color-subtle)]">📝 학습 노트</h3>
        <span className="text-[10px] text-zinc-600">{messageCount}개 메시지</span>
      </header>

      {note ? (
        <div className="notes-md text-sm text-zinc-300 max-h-[400px] overflow-y-auto pr-1"
             dangerouslySetInnerHTML={{ __html: noteHtml }} />
      ) : (
        <p className="text-xs text-zinc-500 py-2">
          이 페이지의 학습 노트가 아직 없어요. LLM과 대화한 뒤 아래 버튼으로 정리 노트를 만들어보세요.
        </p>
      )}

      {error && <p className="text-xs text-rose-400 mt-2">⚠ {error}</p>}
      {toast && <p className="text-xs text-emerald-400 mt-2">✓ {toast}</p>}

      <div className="mt-3 flex flex-wrap gap-1.5">
        <button
          onClick={generate}
          disabled={busy !== 'idle'}
          className="text-[11px] px-2.5 py-1 rounded bg-indigo-500/20 border border-indigo-500/40 text-indigo-300 hover:bg-indigo-500/30 disabled:opacity-40"
        >
          {busy === 'generating' ? '⏳ 정리 중…' : (note ? '➕ 노트 추가' : '✨ 노트 생성')}
        </button>
        {note && (
          <>
            <button
              onClick={saveToFile}
              disabled={busy !== 'idle'}
              title="docs/notes/ 파일로 영구 저장 (git 추적)"
              className="text-[11px] px-2.5 py-1 rounded border border-zinc-700 text-zinc-300 hover:bg-zinc-800 disabled:opacity-40"
            >
              💾 영구 저장
            </button>
            <button
              onClick={download}
              title=".md 파일 다운로드"
              className="text-[11px] px-2.5 py-1 rounded border border-zinc-700 text-zinc-300 hover:bg-zinc-800"
            >
              📤 내보내기
            </button>
            <button
              onClick={clearNote}
              title="localStorage 노트 비우기 (파일은 유지)"
              className="text-[11px] px-2.5 py-1 rounded border border-zinc-700 text-zinc-500 hover:bg-rose-500/20 hover:text-rose-300 ml-auto"
            >
              지우기
            </button>
          </>
        )}
      </div>
      <style>{`
        .notes-md table {
          border-collapse: collapse;
          margin: 0.6em 0;
          font-size: 0.92em;
        }
        .notes-md th, .notes-md td {
          border: 1px solid var(--color-border);
          padding: 0.3em 0.6em;
          text-align: left;
          vertical-align: top;
        }
        .notes-md th {
          background: var(--color-surface-2);
          font-weight: 600;
        }
      `}</style>
    </section>
  );
}
