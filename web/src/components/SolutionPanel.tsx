// 검증된 풀이 캐시(frontmatter `solution:`)를 문제 페이지에 표시.
// scripts/build_solution_cache.py 가 채운 단계별 풀이를 "풀이 보기" 토글로 노출 —
// 기본은 접힘(스포일러 방지, 사이드바 '정답 보기' blur 버튼과 동일 철학).
// KaTeX 는 mathish 의 MathishText 재사용 (앱 전역과 동일 렌더).
import { useState } from 'react';
import { MathishText } from '../lib/mathish';

type Solution = {
  answer_value?: string;
  verified?: boolean;
  generated_by?: string;
  steps?: string[];
};

export default function SolutionPanel({ solution }: { solution?: Solution }) {
  const [open, setOpen] = useState(false);
  if (!solution?.steps?.length) return null;

  // steps 의 `**bold**` 마커는 제거(텍스트만), `\n` 으로 줄 분리. KaTeX `$...$` 는 MathishText 가 처리.
  const lines = (s: string) => s.replace(/\*\*(.+?)\*\*/g, '$1').split('\n').filter((l) => l.trim());

  return (
    <section className="card my-6">
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        className="w-full flex items-center justify-between text-left group"
        aria-expanded={open}
      >
        <span className="text-xs uppercase tracking-[0.15em] text-[color:var(--color-subtle)] group-hover:text-[color:var(--color-accent)] transition">
          {open ? '▼' : '▶'} 검증된 풀이 보기
        </span>
        <span className="text-[10px] text-zinc-500">
          {solution.verified ? '✓ 검증됨' : ''}{solution.generated_by ? ` · ${solution.generated_by}` : ''} · 스포일러
        </span>
      </button>

      {open && (
        <ol className="mt-4 space-y-3 text-sm list-none">
          {solution.steps.map((s, i) => (
            <li key={i} className="flex gap-3">
              <span className="shrink-0 w-5 h-5 mt-0.5 rounded-full bg-indigo-500/20 border border-indigo-500/30 text-indigo-300 text-[11px] flex items-center justify-center">
                {i + 1}
              </span>
              {/* overflow 는 안쪽 .katex-display(max-width:100% + 자체 overflow-x:auto)에 맡긴다.
                  바깥에 overflow-x-auto 를 또 두면 수식이 폭에 거의 맞을 때 1~2px 넘쳐
                  불필요한 스크롤바가 생긴다(우측 스크롤바 버그). min-w-0 만 유지(flex 축소 허용). */}
              <div className="flex-1 leading-relaxed space-y-1 min-w-0">
                {lines(s).map((line, j) => (
                  <MathishText key={j} text={line} display className="block" />
                ))}
              </div>
            </li>
          ))}
          {solution.answer_value && (
            <li className="flex gap-3 pt-3 mt-1 border-t border-zinc-800 items-center">
              <span className="shrink-0 text-emerald-400 text-xs">정답</span>
              <MathishText text={solution.answer_value} auto className="text-emerald-300 font-mono" />
            </li>
          )}
        </ol>
      )}
    </section>
  );
}
