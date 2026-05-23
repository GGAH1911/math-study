import { useState } from 'react';

// Detail-page-only delete control. The /syntheses/[slug] page embeds
// this as a `client:load` island in its right sidebar — the rest of the
// page stays static. After a successful delete we navigate back to the
// /syntheses index so the user isn't staring at a now-404 detail page.

type Props = {
  slug: string;
};

export default function SynthesisDeleteButton({ slug }: Props) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onClick = async () => {
    if (busy) return;
    const ok = window.confirm(
      `이 학습 노트를 삭제할까요?\n\n${slug}\n\ndocs/syntheses/ 에서 파일이 영구히 제거됩니다.`
    );
    if (!ok) return;
    setBusy(true);
    setError(null);
    try {
      const res = await fetch('/api/synthesis-delete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ slug }),
      });
      const json = await res.json();
      if (!res.ok) throw new Error(json.error ?? `HTTP ${res.status}`);
      // 삭제된 페이지에 머무를 이유가 없으니 목록으로.
      window.location.href = '/syntheses';
    } catch (e) {
      setError((e as Error).message);
      setBusy(false);
    }
  };

  return (
    <>
      <button
        type="button"
        onClick={onClick}
        disabled={busy}
        className="w-full px-3 py-1.5 rounded-md border border-rose-500/40 bg-rose-500/10 hover:bg-rose-500/20 text-rose-300 text-xs font-medium transition disabled:opacity-50 disabled:cursor-wait"
      >
        {busy ? '삭제 중…' : '🗑 이 노트 삭제'}
      </button>
      {error && (
        <p className="mt-2 text-[11px] text-rose-400">⚠ {error}</p>
      )}
    </>
  );
}
