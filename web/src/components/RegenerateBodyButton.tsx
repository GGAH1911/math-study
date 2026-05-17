import { useState } from 'react';

type Props = {
  slug: string;
};

export default function RegenerateBodyButton({ slug }: Props) {
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState<string | null>(null);

  const run = async (model: 'haiku' | 'sonnet') => {
    if (busy) return;
    if (!confirm(`'${slug}' 페이지 본문을 ${model}로 다시 작성합니다. 기존 본문은 덮어쓰여집니다. 계속할까요?`)) return;
    setBusy(true);
    setMsg(null);
    try {
      const res = await fetch('/api/regenerate-body', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ slug, model }),
      });
      const json = await res.json();
      if (!res.ok) throw new Error(json.error ?? `HTTP ${res.status}`);
      setMsg(`✓ 본문 갱신 (${json.length} chars). 새로고침으로 반영.`);
      setTimeout(() => location.reload(), 1500);
    } catch (e) {
      setMsg(`✗ 실패: ${(e as Error).message}`);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="space-y-2">
      <div className="flex gap-2">
        <button
          onClick={() => run('haiku')}
          disabled={busy}
          className="flex-1 px-3 py-1.5 rounded-md text-xs font-medium bg-indigo-500/10 hover:bg-indigo-500/20 border border-indigo-500/30 text-indigo-300 transition disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {busy ? '생성 중…' : '↻ haiku로 작성'}
        </button>
        <button
          onClick={() => run('sonnet')}
          disabled={busy}
          className="flex-1 px-3 py-1.5 rounded-md text-xs font-medium bg-violet-500/10 hover:bg-violet-500/20 border border-violet-500/30 text-violet-300 transition disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {busy ? '생성 중…' : '↻ sonnet로 작성'}
        </button>
      </div>
      {msg && (
        <p className={`text-xs ${msg.startsWith('✓') ? 'text-emerald-400' : 'text-rose-400'}`}>
          {msg}
        </p>
      )}
      <p className="text-[10px] text-[color:var(--color-subtle)] leading-relaxed">
        본문이 빈약하거나 더 깊은 설명이 필요할 때. 기존 본문은 덮어쓰여집니다 (Git에 commit 안 한 변경은 사라짐).
      </p>
    </div>
  );
}
