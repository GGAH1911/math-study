import { useState } from 'react';

type Props = {
  slug: string;
  // Concept-detail page passes this from syntheses-by-concept.json. When
  // > 0 we show an extra "노트 반영" button that injects the student's
  // saved notes into the regenerate prompt (always uses sonnet for that
  // path — personalization warrants the better model).
  noteCount?: number;
};

export default function RegenerateBodyButton({ slug, noteCount = 0 }: Props) {
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState<string | null>(null);

  const run = async (model: 'haiku' | 'sonnet', useNotes = false) => {
    if (busy) return;
    const label = useNotes
      ? `'${slug}' 본문을 저장된 노트 ${noteCount}개를 반영해서 다시 작성합니다. 기존 본문은 덮어쓰여집니다. 계속할까요?`
      : `'${slug}' 페이지 본문을 ${model}로 다시 작성합니다. 기존 본문은 덮어쓰여집니다. 계속할까요?`;
    if (!confirm(label)) return;
    setBusy(true);
    setMsg(null);
    try {
      const res = await fetch('/api/regenerate-body', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ slug, model, useNotes }),
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
      {noteCount > 0 && (
        <button
          onClick={() => run('sonnet', true)}
          disabled={busy}
          className="w-full px-3 py-1.5 rounded-md text-xs font-medium bg-amber-500/10 hover:bg-amber-500/20 border border-amber-500/30 text-amber-300 transition disabled:opacity-50 disabled:cursor-not-allowed"
          title={`이 페이지의 학습 노트 ${noteCount}개를 컨텍스트로 사용해 본문 개인화 (sonnet)`}
        >
          {busy ? '생성 중…' : `📝 노트 ${noteCount}개 반영해서 작성 (sonnet)`}
        </button>
      )}
      {msg && (
        <p className={`text-xs ${msg.startsWith('✓') ? 'text-emerald-400' : 'text-rose-400'}`}>
          {msg}
        </p>
      )}
      <p className="text-[10px] text-[color:var(--color-subtle)] leading-relaxed">
        본문이 빈약하거나 더 깊은 설명이 필요할 때. 기존 본문은 덮어쓰여집니다 (Git에 commit 안 한 변경은 사라짐).
        {noteCount > 0 && ' "노트 반영"은 LLM에 학생의 promote 노트를 함께 전달.'}
      </p>
    </div>
  );
}
