import { useEffect, useState } from 'react';
import { Doughnut } from 'react-chartjs-2';
import { Chart, ArcElement, Tooltip, Legend } from 'chart.js';
import type { ChartOptions } from 'chart.js';

Chart.register(ArcElement, Tooltip, Legend);

type Props = {
  unknown: number;
  learning: number;
  proficient: number;
  mastered: number;
};

/* §14-C 패턴: chart.js 는 색 문자열만 소비하므로 마운트 시 getComputedStyle 로
   --color-mastery-* 토큰 실측값을 캐싱하고, html class MutationObserver 로
   테마 토글을 감지해 재렌더한다 — 도넛이 바로 옆 범례 점·헤더 칩과
   같은 4색을 공유하고, 세그먼트 보더·툴팁도 양 테마를 추종. */
type ThemeColors = {
  unknown: string;
  learning: string;
  proficient: string;
  mastered: string;
  surface: string;
  tipBg: string;
  tipBorder: string;
  text: string;
  muted: string;
};

/* SSR·실측 실패 fallback — 라이트 토큰 리터럴(global.css @theme 와 동일 값) */
const LIGHT_FALLBACK: ThemeColors = {
  unknown: '#C13D38',
  learning: '#9F600C',
  proficient: '#2E7B4F',
  mastered: '#166E8E',
  surface: '#F5F0E4',
  tipBg: 'rgba(245, 240, 228, 0.95)',
  tipBorder: '#D7CDB5',
  text: '#2A261E',
  muted: '#6B6350',
};

function readThemeColors(): ThemeColors {
  const cs = getComputedStyle(document.documentElement);
  const v = (name: string, fallback: string) => cs.getPropertyValue(name).trim() || fallback;
  return {
    unknown: v('--color-mastery-unknown', LIGHT_FALLBACK.unknown),
    learning: v('--color-mastery-learning', LIGHT_FALLBACK.learning),
    proficient: v('--color-mastery-proficient', LIGHT_FALLBACK.proficient),
    mastered: v('--color-mastery-mastered', LIGHT_FALLBACK.mastered),
    surface: v('--color-surface', LIGHT_FALLBACK.surface),
    tipBg: v('--plot-tip-bg', LIGHT_FALLBACK.tipBg),
    tipBorder: v('--plot-tip-border', LIGHT_FALLBACK.tipBorder),
    text: v('--color-text', LIGHT_FALLBACK.text),
    muted: v('--color-muted', LIGHT_FALLBACK.muted),
  };
}

export default function MasteryDonut({ unknown, learning, proficient, mastered }: Props) {
  // lazy 초기화: 하이드레이션 첫 렌더부터 현재 테마 실측값 사용(플래시 방지)
  const [colors, setColors] = useState<ThemeColors>(() =>
    typeof document === 'undefined' ? LIGHT_FALLBACK : readThemeColors(),
  );

  useEffect(() => {
    // 테마 토글(html.dark) 추종 — 색 재캐싱 → 새 data/options 로 chart.update
    const obs = new MutationObserver(() => setColors(readThemeColors()));
    obs.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
    return () => obs.disconnect();
  }, []);

  const total = unknown + learning + proficient + mastered;
  const data = {
    labels: ['미습득', '학습중', '능숙', '마스터'],
    datasets: [
      {
        data: [unknown, learning, proficient, mastered],
        backgroundColor: [colors.unknown, colors.learning, colors.proficient, colors.mastered],
        borderColor: colors.surface, // 세그먼트 간 보더 = 카드 표면색(검은 링 제거)
        borderWidth: 3,
        hoverOffset: 6,
      },
    ],
  };

  const options: ChartOptions<'doughnut'> = {
    cutout: '70%',
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: colors.tipBg,
        titleColor: colors.text,
        bodyColor: colors.muted,
        borderColor: colors.tipBorder,
        borderWidth: 1,
        padding: 10,
        callbacks: {
          label: (ctx) => {
            const v = ctx.parsed;
            const pct = total > 0 ? Math.round((v / total) * 100) : 0;
            return `${ctx.label}: ${v} (${pct}%)`;
          },
        },
      },
    },
  };

  return (
    <div className="relative aspect-square w-full max-w-[180px] mx-auto">
      <Doughnut data={data} options={options} />
      <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
        <div className="text-center">
          <div className="stat-num text-2xl">{total}</div>
          <div className="text-[10px] tracking-[0.1em] text-[color:var(--color-subtle)]">단원</div>
        </div>
      </div>
    </div>
  );
}
