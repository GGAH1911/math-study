// Dev-only verification page for the LLM-emitted graphic block components.
// Mounted by web/src/pages/dev/graphics-test.astro.
//
// Each section renders one component type with a hand-picked sample spec so
// regressions (broken labels, missing modals, sticky-panel drift, JSON
// errors) can be eyeballed in one place without round-tripping the LLM.

import Graph, { GraphModal, type PlotSpec } from './Graph.tsx';
import Geometry, { type GeomSpec } from './Geometry.tsx';
import Numberline, { type NumberlineSpec } from './Numberline.tsx';
import StatsChart, { type ChartSpec } from './StatsChart.tsx';
import Interactive from './Interactive.tsx';
import { INTERACTIVE_SAMPLES } from '../data/interactive-samples';
import type { InteractiveSpec } from '../data/interactive-samples';
import { ErrorSegment, parseGraphSegments } from './chat/Message';
import { useEffect, useState } from 'react';

// Render a string that may contain `$...$` LaTeX segments. Used for section
// titles so $-3 \le x < 2$ shows pretty math instead of raw source.
function MaybeMath({ text }: { text: string }) {
  const [html, setHtml] = useState<string>(text);
  useEffect(() => {
    if (!text.includes('$')) { setHtml(text); return; }
    let cancelled = false;
    (async () => {
      try {
        const mod = await import('katex');
        const katex = (mod.default ?? mod) as { renderToString: (t: string, o?: object) => string };
        const escape = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        const out = escape(text).replace(/\$([^\n$]+?)\$/g, (_, tex) =>
          katex.renderToString(tex.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>'),
                              { displayMode: false, throwOnError: false }));
        if (!cancelled) setHtml(out);
      } catch { /* leave plain */ }
    })();
    return () => { cancelled = true; };
  }, [text]);
  return <span dangerouslySetInnerHTML={{ __html: html }} />;
}

type ModalState =
  | { kind: 'plot' | 'svg'; spec?: PlotSpec; svg?: string }
  | { kind: 'geom'; geomSpec: GeomSpec }
  | { kind: 'numberline'; numberlineSpec: NumberlineSpec }
  | { kind: 'chart'; chartSpec: ChartSpec }
  | { kind: 'interactive'; interactiveSpec: InteractiveSpec }
  | null;

// f(x) = x² − 3x + 2 와 점 x=a 에서의 접선 y = f'(a)(x − a) + f(a)
// f'(x) = 2x − 3, f(a) = a² − 3a + 2
// 접선: y = (2a − 3)(x − a) + (a² − 3a + 2) = (2a − 3)x − a² + 2
//      → mathjs scope 로 a 를 슬라이더에 묶음.
const SAMPLE_PLOT: PlotSpec = {
  title: '$f(x) = x^2 - 3x + 2$의 점 $x = a$ 접선',
  fns: [
    { fn: 'x^2 - 3*x + 2', label: '$f(x)$' },
    { fn: '(2*a - 3)*x - a^2 + 2', label: '점 $a$의 접선', scope: { a: 2 } },
  ],
  range: [-2, 5],
  yRange: [-3, 8],
  points: [[1, 0], [2, 0]],
  pointsLabel: '$f$의 근',
  sliders: [{ name: 'a', min: -1, max: 4, init: 2, step: 0.1 }],
};

// 평행사변형 ABCD + 대각선 + 한 내각 θ. Vector 테스트는 별도 도형(SAMPLE_GEOM_VEC)으로 분리.
const SAMPLE_GEOM: GeomSpec = {
  title: '평행사변형 $ABCD$',
  shapes: [
    {
      type: 'polygon',
      vertices: [[0, 0], [4, 0], [5, 2.5], [1, 2.5]],
      labels: ['A', 'B', 'C', 'D'],
    },
    { type: 'segment', from: [0, 0], to: [5, 2.5], dashed: true },
    { type: 'segment', from: [4, 0], to: [1, 2.5], dashed: true },
    // 대각선 라벨은 별도 text 도형으로 분산 배치. AC와 BD는 중심 (2.5, 1.25)
    // 에서 교차해서 segment 자동 midpoint label은 겹침. 각 대각선 위의 70%
    // 지점(끝 쪽)에 두면 (a) 라벨이 실제로 해당 대각선 위에 있고 (b) 서로
    // 멀리 떨어져서 안 겹친다.
    //   AC: 70% from A → (3.5, 1.75). 살짝 위로 offset해서 라인 안 가리게.
    //   BD: 70% from B → (1.75, 1.875). 동일.
    { type: 'text', at: [3.55, 1.85], text: '$\\overline{AC}$' },
    { type: 'text', at: [1.4, 1.95], text: '$\\overline{BD}$' },
    { type: 'angle', at: [0, 0], from: [4, 0], to: [1, 2.5], radius: 0.6, label: '$\\theta$' },
  ],
  range: [-1, 6.5],
  yRange: [-1, 3.5],
  showAxes: false,
  showGrid: false,
};

// vector + point + circle 타입 단독 검증용.
const SAMPLE_GEOM_VEC: GeomSpec = {
  title: '벡터·점·원 ($O$ 중심, 반지름 2)',
  shapes: [
    // circle 자체에는 라벨을 두지 않고 (중심 라벨은 point가 담당), point만 'O' 라벨.
    { type: 'circle', center: [0, 0], radius: 2 },
    { type: 'point', at: [0, 0], label: '$O$' },
    { type: 'vector', from: [0, 0], to: [2, 1.5], label: '$\\vec{u}$' },
    { type: 'vector', from: [0, 0], to: [-1.5, 1], label: '$\\vec{v}$', color: '#fb7185' },
    { type: 'text', at: [-2.5, -2], text: '벡터·점·원 동시 렌더 검증' },
  ],
  range: [-3, 3],
  yRange: [-2.5, 2.5],
  showAxes: true,
  showGrid: true,
};

// 합집합 형태의 해 집합: (-3 ≤ x < 2) ∪ (x ≥ 5)
// — 두 interval 동시 표시 + offset (위/아래 row 분리) + +∞ 화살표 검증 겸함.
const SAMPLE_NUMBERLINE: NumberlineSpec = {
  title: '$x$의 범위: $-3 \\le x < 2$ 또는 $x \\ge 5$',
  range: [-6, 8],
  marks: [
    { at: -3, label: '$-3$', closed: true },
    { at: 2, label: '$2$', closed: false },
    { at: 5, label: '$5$', closed: true },
  ],
  intervals: [
    { from: -3, to: 2, closed: [true, false], color: '#a5b4fc', label: '$-3 \\le x < 2$' },
    { from: 5, to: Infinity, closed: [true, false], color: '#34d399', label: '$x \\ge 5$', offset: 1 },
  ],
};

const SAMPLE_CHARTS: Array<{ key: string; spec: ChartSpec }> = [
  {
    key: 'histogram',
    spec: {
      kind: 'histogram',
      bins: [[0, 20, 5], [20, 40, 12], [40, 60, 28], [60, 80, 35], [80, 100, 18]],
      xLabel: '점수', yLabel: '학생 수', title: '수학 점수 분포',
    },
  },
  {
    key: 'bar',
    spec: {
      kind: 'bar',
      data: [{ x: '확통', y: 7 }, { x: '기하', y: 5 }, { x: '미적', y: 9 }, { x: '대수', y: 4 }],
      title: '단원별 오답 수', xLabel: '단원', yLabel: '오답',
    },
  },
  {
    key: 'line',
    spec: {
      kind: 'line',
      data: [{ x: 1, y: 60 }, { x: 2, y: 65 }, { x: 3, y: 72 }, { x: 4, y: 78 }, { x: 5, y: 83 }],
      title: '주차별 평균점수', xLabel: '주', yLabel: '점수',
    },
  },
  {
    key: 'normal',
    spec: {
      kind: 'normal',
      mean: 0, std: 1, shaded: [-1, 1],
      title: '표준정규분포 ($\\mu \\pm \\sigma$)',
    },
  },
  {
    key: 'box',
    spec: {
      kind: 'box',
      stats: { min: 32, q1: 58, median: 71, q3: 84, max: 96 },
      outliers: [15],
      title: '반 점수 박스플롯',
    },
  },
];

const SAMPLE_SVG = `<svg viewBox="0 0 340 160" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="10" width="320" height="140" fill="#1e1b4b" stroke="#a5b4fc" stroke-width="2" rx="12"/>
  <circle cx="80" cy="75" r="38" fill="#a5b4fc33" stroke="#a5b4fc" stroke-width="2"/>
  <polygon points="200,40 260,40 280,115 220,115 180,80" fill="#fb718533" stroke="#fb7185" stroke-width="2"/>
  <text x="170" y="142" text-anchor="middle" fill="#fafafa" font-size="12" font-family="sans-serif">raw SVG · sanitize + auto size</text>
</svg>`;

const EDGE_GEOM_EMPTY: GeomSpec = { shapes: [], title: '빈 shapes' };

function Section({
  num, title, expected, children,
}: { num: number; title: string; expected: string; children: React.ReactNode }) {
  return (
    <section className="card my-5 p-4">
      <header className="mb-3 pb-2 border-b border-[color:var(--color-border)]">
        <h2 className="text-sm font-semibold">
          <span className="text-[color:var(--color-accent)] mr-2">§{num}</span>
          <MaybeMath text={title} />
        </h2>
        <p className="text-[11px] text-[color:var(--color-muted)] mt-1 font-mono">{expected}</p>
      </header>
      {children}
    </section>
  );
}

export default function GraphicsTest() {
  const [modal, setModal] = useState<ModalState>(null);

  return (
    <div>
      <Section
        num={1}
        title="Plot — function-plot"
        expected="✓ 인라인 · ✓ 클릭→모달 (sliders) · ✓ sticky 미러링"
      >
        <Graph
          kind="plot"
          spec={SAMPLE_PLOT}
          onOpen={() => setModal({ kind: 'plot', spec: SAMPLE_PLOT })}
        />
      </Section>

      <Section
        num={2}
        title="Geometry — 평행사변형 ABCD"
        expected="✓ 꼭지점 라벨 A/B/C/D가 정확한 위치 · ✓ 각 θ · ✓ 클릭→모달 · ✓ sticky 미러링"
      >
        <Geometry
          spec={SAMPLE_GEOM}
          onOpen={() => setModal({ kind: 'geom', geomSpec: SAMPLE_GEOM })}
        />
        <div className="mt-3">
          <div className="text-[10px] uppercase tracking-wider text-[color:var(--color-muted)] mb-1">
            vector / point / circle 추가 검증
          </div>
          <Geometry
            spec={SAMPLE_GEOM_VEC}
            onOpen={() => setModal({ kind: 'geom', geomSpec: SAMPLE_GEOM_VEC })}
          />
        </div>
      </Section>

      <Section
        num={3}
        title="Numberline — $-3 \le x < 2$ 또는 $x \ge 5$"
        expected="✓ 인라인 · ✓ closed/open · ✓ 클릭→모달 · ✓ sticky 미러링"
      >
        <Numberline spec={SAMPLE_NUMBERLINE}
                    onOpen={() => setModal({ kind: 'numberline', numberlineSpec: SAMPLE_NUMBERLINE })} />
      </Section>

      <Section
        num={4}
        title="StatsChart — 5종 (histogram/bar/line/normal/box)"
        expected="✓ 5개 모두 렌더 · ✓ 각자 클릭→모달 · ✓ sticky 미러링 (마지막 본 것)"
      >
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {SAMPLE_CHARTS.map((c) => (
            <div key={c.key}>
              <div className="text-[10px] uppercase tracking-wider text-[color:var(--color-muted)] mb-1">
                {c.key}
              </div>
              <StatsChart spec={c.spec}
                          onOpen={() => setModal({ kind: 'chart', chartSpec: c.spec })} />
            </div>
          ))}
        </div>
      </Section>

      <Section
        num={5}
        title="SVG — raw + DOMPurify"
        expected="✓ 인라인 · ✓ 클릭→모달"
      >
        <Graph
          kind="svg"
          svg={SAMPLE_SVG}
          onOpen={() => setModal({ kind: 'svg', svg: SAMPLE_SVG })}
        />
      </Section>

      <Section
        num={6}
        title="에지 케이스 — 빈 spec"
        expected="✓ 깨지지 않음 (에러 메시지 또는 빈 캔버스)"
      >
        <div className="space-y-3">
          <div>
            <div className="text-[10px] uppercase tracking-wider text-[color:var(--color-muted)] mb-1">
              Geometry shapes=[]
            </div>
            <Geometry spec={EDGE_GEOM_EMPTY} />
          </div>
          <div>
            <div className="text-[10px] uppercase tracking-wider text-[color:var(--color-muted)] mb-1">
              Plot fn 없음
            </div>
            <Graph kind="plot" spec={{ range: [-3, 3] } as PlotSpec} />
          </div>
          <div>
            <div className="text-[10px] uppercase tracking-wider text-[color:var(--color-muted)] mb-1">
              Interactive 잘못된 표현식 (mu 슬라이더만 있는데 식이 nu 참조)
            </div>
            <Interactive spec={{
              title: '잘못된 표현식 테스트',
              params: [{ name: 'mu', label: 'μ', type: 'slider', min: 0, max: 5, init: 1, step: 0.1 }],
              scope: 'k = mu * nu',   // nu is undefined
              geometry: {
                shapes: [{ type: 'point', at: ['=mu', '=k'] as unknown as [number, number], label: 'P' }],
                range: [-1, 5], yRange: [-1, 5],
              },
              readout: [{ label: 'k', expr: 'k' }],
            }} />
          </div>
        </div>
      </Section>

      <Section
        num={8}
        title="Interactive — 동적 탐구 (6개 시드)"
        expected="✓ 각자 슬라이더로 즉시 갱신 · ✓ 클릭→모달 · ✓ sticky 미러링 · LLM이 학습 상황에 맞춰 골라 쓸 reference"
      >
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {INTERACTIVE_SAMPLES.map(({ key, spec }) => (
            <div key={key}>
              <div className="text-[10px] uppercase tracking-wider text-[color:var(--color-muted)] mb-1">{key}</div>
              <Interactive
                spec={spec}
                width={420}
                height={280}
                onOpen={() => setModal({ kind: 'interactive', interactiveSpec: spec })}
              />
            </div>
          ))}
        </div>
      </Section>

      <Section
        num={7}
        title="JSON 파싱 에러 — 사용자 친화 에러 표시"
        expected="✓ 깨진 fence는 빨간 에러 박스 · 메시지 + '원문 보기' 토글로 디버깅 가능"
      >
        {/* Actually pipes broken fences through the real ChatPanel parser
            so the verification matches production behavior. */}
        {parseGraphSegments([
          '아래는 일부러 깨진 chart spec입니다:',
          '```chart',
          '{ kind: "bar", data: [ {x:"A", y:5} ',  // missing closing brace + unquoted keys
          '```',
          '',
          '그리고 잘못된 geometry:',
          '```geometry',
          '{"shapes": [{"type":"polygon" "vertices":[[0,0]]}]}',  // missing comma
          '```',
        ].join('\n')).map((s, i) => {
          if (s.type === 'error') return <ErrorSegment key={i} kind={s.kind} message={s.message} body={s.body} />;
          if (s.type === 'md') return <p key={i} className="text-xs text-[color:var(--color-muted)] my-1">{s.content}</p>;
          return null;
        })}
      </Section>

      {modal && (
        <GraphModal
          open
          kind={modal.kind}
          spec={modal.kind === 'plot' || modal.kind === 'svg' ? modal.spec : undefined}
          svg={modal.kind === 'svg' ? modal.svg : undefined}
          geomSpec={modal.kind === 'geom' ? modal.geomSpec : undefined}
          numberlineSpec={modal.kind === 'numberline' ? modal.numberlineSpec : undefined}
          chartSpec={modal.kind === 'chart' ? modal.chartSpec : undefined}
          interactiveSpec={modal.kind === 'interactive' ? modal.interactiveSpec : undefined}
          onClose={() => setModal(null)}
        />
      )}
    </div>
  );
}
