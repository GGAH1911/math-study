import { useEffect, useState } from 'react';

// 우측 사이드바의 작은 카드. "학습 노트 작성"이 가능하다는 발견 통로 +
// 클릭 시 chat 흐름에 노트 작성 user message를 주입한다 (window CustomEvent
// `math-study:chat-note-request`). 결과 답변 아래에는 ChatPanel 의 Message
// 컴포넌트가 자동으로 액션 행 (저장 / 더 짧게 / 더 자세히 / 핵심만) 을
// 노출한다.
//
// 본인은 LLM 호출이나 파일 IO를 하지 않는다 — 그건 전부 chat 쪽에서 처리.

type Props = {
  slug: string;
  unitTitle: string;
  collection?: 'concepts' | 'problems' | 'dashboard';
};

export default function LearningNoteButton({ slug, unitTitle, collection = 'concepts' }: Props) {
  const [lastSaved, setLastSaved] = useState<string | null>(null);

  // ChatPanel이 promote 성공 시 같은 storageKey로 신호 보내면 카드 하단에
  // "최근 저장: …" 표시. 별도 통신 채널이 없으니 localStorage로 가볍게.
  const recentKey = `math-study:note-last-saved:${collection}:${slug}`;
  useEffect(() => {
    try { setLastSaved(localStorage.getItem(recentKey)); } catch { /* ignore */ }
    const onStorage = (e: StorageEvent) => {
      if (e.key === recentKey) setLastSaved(e.newValue);
    };
    window.addEventListener('storage', onStorage);
    return () => window.removeEventListener('storage', onStorage);
  }, [recentKey]);

  const requestNote = () => {
    window.dispatchEvent(new CustomEvent('math-study:chat-note-request', {
      detail: { unitTitle },
    }));
  };

  return (
    <section className="card">
      <h3 className="text-xs uppercase tracking-[0.15em] text-[color:var(--color-subtle)] mb-2 flex items-center gap-1.5">
        <span aria-hidden>📝</span>
        <span>학습 노트</span>
      </h3>
      <p className="text-[11px] text-[color:var(--color-muted)] leading-relaxed mb-2.5">
        지금까지의 대화를 LLM에 보내 학습 노트를 받아봅니다. 답변 아래
        버튼으로 길이 조정·저장.
      </p>
      <button
        type="button"
        onClick={requestNote}
        className="w-full px-3 py-2 rounded-lg bg-indigo-500/15 hover:bg-indigo-500/25 border border-indigo-500/40 text-indigo-200 text-sm font-medium transition"
      >
        ✨ 학습 노트 작성 요청
      </button>
      {lastSaved && (
        <p className="mt-2 text-[10px] text-[color:var(--color-subtle)]">
          최근 저장: <span className="text-emerald-400">{lastSaved}</span>
        </p>
      )}
    </section>
  );
}
