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

const MASTERY_COLORS = {
  unknown: '#f43f5e',
  learning: '#f59e0b',
  proficient: '#10b981',
  mastered: '#0ea5e9',
};

export default function MasteryDonut({ unknown, learning, proficient, mastered }: Props) {
  const total = unknown + learning + proficient + mastered;
  const data = {
    labels: ['unknown', 'learning', 'proficient', 'mastered'],
    datasets: [
      {
        data: [unknown, learning, proficient, mastered],
        backgroundColor: [
          MASTERY_COLORS.unknown,
          MASTERY_COLORS.learning,
          MASTERY_COLORS.proficient,
          MASTERY_COLORS.mastered,
        ],
        borderColor: '#18181b',
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
        backgroundColor: '#1f1f23',
        titleColor: '#fafafa',
        bodyColor: '#a1a1aa',
        borderColor: '#27272a',
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
          <div className="text-[10px] uppercase tracking-[0.15em] text-[color:var(--color-subtle)]">concepts</div>
        </div>
      </div>
    </div>
  );
}
