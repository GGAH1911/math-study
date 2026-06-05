// 유사문제 생성 PoC — 검증기 자산을 씨앗+채점기로 써서 만든 변형 3종을
// 도형 복잡도(비도형/일반도형/복잡도형)별로 렌더. dev/variants-test.astro 가 마운트.
// 도형은 기존 Graph(plot)/Geometry(2D) 컴포넌트를 그대로 재사용 — sympy로 좌표 계산한 spec.
// 사이트 다크테마(--color-surface/border/text) 색변수 사용.
import Graph, { type PlotSpec } from './Graph.tsx';
import Geometry, { type GeomSpec } from './Geometry.tsx';
import { useEffect, useState, type ReactNode } from 'react';

// $...$ 인라인 LaTeX 렌더 (GraphicsTest 의 MaybeMath 패턴)
function MathText({ text }: { text: string }) {
  const [html, setHtml] = useState<string>(text);
  useEffect(() => {
    if (!text.includes('$')) { setHtml(text); return; }
    let cancelled = false;
    (async () => {
      try {
        const mod = await import('katex');
        const katex = (mod.default ?? mod) as { renderToString: (t: string, o?: object) => string };
        const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        const out = esc(text).replace(/\$([^\n$]+?)\$/g, (_, tex) =>
          katex.renderToString(tex.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>'),
                              { displayMode: false, throwOnError: false }));
        if (!cancelled) setHtml(out);
      } catch { /* leave plain */ }
    })();
    return () => { cancelled = true; };
  }, [text]);
  return <span dangerouslySetInnerHTML={{ __html: html }} />;
}

// 변형2 도형: 포물선 y=x²−6x+8 + x축 교점 A,B
const PARABOLA: PlotSpec = {
  title: '$y = x^2 - 6x + 8$',
  fns: [{ fn: 'x^2 - 6*x + 8', label: '$y$' }],
  range: [-1, 7],
  yRange: [-2, 10],
  points: [[2, 0], [4, 0]],
  pointsLabel: '$A,\\ B$',
};

// 변형3 도형: 반지름5 원 O + 내접 직각삼각형 ABC (BC=지름, A=(−1.4,4.8) sympy 계산)
const CIRCLE_TRI: GeomSpec = {
  title: '원 $O$(반지름 5) 내접 직각삼각형 $ABC$',
  shapes: [
    { type: 'circle', center: [0, 0], radius: 5 },
    { type: 'point', at: [0, 0], label: '$O$' },
    { type: 'polygon', vertices: [[-1.4, 4.8], [-5, 0], [5, 0]], labels: ['A', 'B', 'C'] },
    { type: 'angle', at: [-1.4, 4.8], from: [-5, 0], to: [5, 0], radius: 0.5, label: '$90°$' },
    { type: 'text', at: [-3.95, 2.7], text: '$6$' },
    { type: 'text', at: [2.35, 2.75], text: '$8$' },
  ],
  range: [-6, 6],
  yRange: [-1.2, 6],
  showAxes: false,
  showGrid: false,
};

// 변형4 도형: 킬러#30 장르 — 포물선 f + 직선 g + 접선 y=x−9 + 접점 (3곡선 복잡 그래프)
const KILLER_GRAPH: PlotSpec = {
  title: '$f=x^2-5x$ · $g=-\\tfrac{1}{2}x+\\tfrac{5}{2}$ · 접선 $y=x-9$',
  fns: [
    { fn: 'x^2 - 5*x', label: '$f$' },
    { fn: '-0.5*x + 2.5', label: '$g$' },
    { fn: 'x - 9', label: '접선' },
  ],
  range: [-2, 8],
  yRange: [-10, 8],
  points: [[3, -6]],
  pointsLabel: '접점 $(3,-6)$',
};

// 변형5 도형: 실제 기출(2026 고2 3월 #12) 재현 — parametric 곡선 2개 + 음영 삼각형 + 라벨점 5개.
// f=2√x → x=t²,y=2t / g=x²/4 → x=t,y=t²/4 / 선 OA → x=4t,y=4t. 좌표는 sympy 계산.
const REAL_FIG: GeomSpec = {
  title: '$f=2\\sqrt{x}$, $g=\\tfrac{1}{4}x^2$ 와 삼각형 $ABC$',
  shapes: [
    { type: 'parametric', x: 't^2', y: '2*t', tRange: [0, 2.15], label: '$f$', color: '#60a5fa' },
    { type: 'parametric', x: 't', y: 't^2/4', tRange: [0, 4.5], label: '$g$', color: '#34d399' },
    { type: 'parametric', x: '4*t', y: '4*t', tRange: [0, 1], color: '#a1a1aa' },
    { type: 'polygon', vertices: [[4, 4], [0.25, 1], [2, 1]], fill: '#fbbf24', fillOpacity: 0.22 },
    { type: 'point', at: [0, 0], label: '$O$' },
    { type: 'point', at: [4, 4], label: '$A$' },
    { type: 'point', at: [0.25, 1], label: '$B$' },
    { type: 'point', at: [1, 1], label: '$P$' },
    { type: 'point', at: [2, 1], label: '$C$' },
  ],
  range: [-0.6, 5],
  yRange: [-0.6, 5],
  showAxes: true,
  showGrid: false,
};

// 변형6 도형: 실제 기출(2026 고2 6월 #18) 재현 — 두 원 교차 + 공통접선 + 접선-현 각(빈칸추론형).
// 두 원이 ℓ(y=0)에 동시에 접하면서 P,Q 두 점에서 교차하도록 수치로 좌표 풀이.
// ω₁(작은,왼쪽) 중심(0.8,1.5)r1.5 / ω₂(큰,오른쪽) 중심(3.3,2.3)r2.3 → 교점 P(1.10,2.97)·Q(1.90,0.48).
const TWO_CIRCLES: GeomSpec = {
  title: '두 원 $\\omega_1,\\omega_2$ (교점 $P,Q$) · 공통접선 $\\ell$ (접점 $A,B$)',
  shapes: [
    { type: 'circle', center: [0.8, 1.5], radius: 1.5, stroke: '#60a5fa' },          // ω₁
    { type: 'circle', center: [3.3, 2.3], radius: 2.3, stroke: '#f472b6' },          // ω₂
    { type: 'line', from: [-0.7, 0], to: [4.9, 0], color: '#a1a1aa' },               // 공통접선 ℓ
    { type: 'line', from: [1.10, 2.97], to: [1.90, 0.48], dashed: true, color: '#71717a' }, // 공통현 PQ
    { type: 'polygon', vertices: [[0.8, 0], [1.10, 2.97], [3.3, 0]], stroke: '#e4e4e7' },    // △PAB
    { type: 'polygon', vertices: [[0.8, 0], [1.90, 0.48], [3.3, 0]], stroke: '#fbbf24' },    // △QAB
    { type: 'angle', at: [0.8, 0], from: [1.90, 0.48], to: [3.3, 0], radius: 0.55, label: '$\\theta_1$' },
    { type: 'angle', at: [3.3, 0], from: [1.90, 0.48], to: [0.8, 0], radius: 0.55, label: '$\\theta_2$' },
    { type: 'point', at: [0.8, 0], label: '$A$', labelDir: 'SW' },
    { type: 'point', at: [3.3, 0], label: '$B$', labelDir: 'SE' },
    { type: 'point', at: [1.10, 2.97], label: '$P$', labelDir: 'N' },
    { type: 'point', at: [1.90, 0.48], label: '$Q$', labelDir: 'E' },
    { type: 'text', at: [-1.0, 2.6], text: '$\\omega_1$', color: '#60a5fa' },
    { type: 'text', at: [4.95, 3.9], text: '$\\omega_2$', color: '#f472b6' },
    { type: 'text', at: [-0.45, 0.26], text: '$\\ell$' },
  ],
  range: [-1.3, 6.2],
  yRange: [-0.7, 5],
  showAxes: false,
  showGrid: false,
};

type Variant = {
  cat: string; tone: string; concept: string; source: string;
  statement: string; answer: string; verifier: string; figure?: ReactNode;
};

const VARIANTS: Variant[] = [
  {
    cat: '비도형', tone: 'text-emerald-300 bg-emerald-500/15 border-emerald-500/40',
    concept: '이차방정식의 허근 · 복소수 절댓값',
    source: '원본형: "$x^2 - bx + c=0$의 두 허근, 조건 만족하는 상수 구하기"',
    statement: '이차방정식 $x^2 - 8x + k = 0$이 서로 다른 두 허근 $\\alpha,\\ \\beta$를 가진다. $|\\alpha|^2 + |\\beta|^2 = 50$일 때, 상수 $k$의 값을 구하시오.',
    answer: '25',
    verifier: 'x²−8x+25=0 근 → 두 허근 확인 → |α|²+|β|²=50 만족',
  },
  {
    cat: '일반도형', tone: 'text-sky-300 bg-sky-500/15 border-sky-500/40',
    concept: '이차함수 그래프와 $x$축 교점',
    source: '원본형: "포물선과 $x$축 교점/길이"',
    statement: '포물선 $y = x^2 - 6x + 8$이 $x$축과 만나는 두 점을 $A,\\ B$라 하자. 선분 $AB$의 길이를 구하시오.',
    answer: '2',
    verifier: 'x²−6x+8=0 두 근 2,4 → |4−2| = 2',
    figure: <Graph kind="plot" spec={PARABOLA} onOpen={() => { /* inline only */ }} />,
  },
  {
    cat: '복잡도형', tone: 'text-rose-300 bg-rose-500/15 border-rose-500/40',
    concept: '반원에 내접하는 직각삼각형 (원주각)',
    source: '원본형: "원 내접 삼각형 + 길이/넓이"',
    statement: '반지름이 $5$인 원 $O$에 직각삼각형 $ABC$가 내접하고, 빗변 $\\overline{BC}$는 원의 지름이다. $\\overline{AB} = 6$일 때, 삼각형 $ABC$의 넓이를 구하시오.',
    answer: '24',
    verifier: 'BC=10(지름)·∠A=90°·AB=6 → AC=8 → 넓이 ½·6·8 = 24',
    figure: <Geometry spec={CIRCLE_TRI} />,
  },
  {
    cat: '복잡 그래프 (킬러)', tone: 'text-amber-300 bg-amber-500/15 border-amber-500/40',
    concept: '이차·일차함수와 매개변수 직선의 접선 (도함수 활용 킬러)',
    source: '원본: 2026 고1 6월 #30 (killer, 세로 2.7) — 원본은 도형 없는 텍스트형(has_figure 오라벨). 그래프를 spec으로 새로 그림.',
    statement: '두 함수 $f(x)=x^2-5x$, $g(x)=-\\frac{1}{2}x+\\frac{5}{2}$가 있다. 직선 $y=x+k$가 곡선 $y=f(x)$에 접할 때, 그 접점의 $x$좌표를 구하시오.',
    answer: '3',
    verifier: 'x²−5x=x+k → x²−6x−k=0 중근(판별식 0) → k=−9, 접점 x=3',
    figure: <Graph kind="plot" spec={KILLER_GRAPH} onOpen={() => { /* inline only */ }} />,
  },
  {
    cat: '실제 기출 도형 재현', tone: 'text-violet-300 bg-violet-500/15 border-violet-500/40',
    concept: '두 함수($\\sqrt{x}$·이차)의 그래프와 삼각형 넓이',
    source: '원본: 2026 고2 3월 #12 — 실제 그림 있는 객관식. PNG를 spec(parametric 곡선 2개 + 음영 polygon + 라벨점)으로 재현.',
    statement: '그림과 같이 $f(x)=2\\sqrt{x}$와 $g(x)=\\frac{1}{4}x^2$의 그래프가 만나는 두 점 중 원점 $O$가 아닌 점을 $A$라 하고, $\\overline{OA}$를 $1:3$으로 내분하는 점 $P$를 지나 $x$축에 평행한 직선이 두 곡선과 만나는 점을 각각 $B,\\ C$라 할 때, 삼각형 $ABC$의 넓이는?',
    answer: '21/8 (②)',
    verifier: 'A=(4,4)·P=(1,1)·B=(¼,1)·C=(2,1) → ½·BC·높이 = ½·(7/4)·3 = 21/8',
    figure: <Geometry spec={REAL_FIG} />,
  },
  {
    cat: '실제 기출 재현 (두 원·공통접선)', tone: 'text-cyan-300 bg-cyan-500/15 border-cyan-500/40',
    concept: '두 원의 교점·공통접선 + 접선-현 각 + 사인·코사인법칙 (빈칸추론형)',
    source: '원본: 2026 고2 6월 #18 (4점·killer mid) — 두 원 교차+공통접선 도형. PNG를 spec(circle×2 + line + polygon + angle + point)으로 재현.',
    statement: '그림과 같이 두 원 $\\omega_1,\\ \\omega_2$가 서로 다른 두 점 $P,\\ Q$에서 만나고, 직선 $\\ell$이 두 원과 동시에 접한다. 접점을 각각 $A,\\ B$라 하고 $\\angle QAB=\\theta_1$, $\\angle QBA=\\theta_2$라 하자. $\\overline{AB}=2$, $\\sin\\theta_1:\\sin\\theta_2=\\sqrt3:\\sqrt2$, 삼각형 $PAB$의 외접원 반지름이 $\\frac{3\\sqrt3}{5}$일 때, $\\overline{QA}$를 구하는 과정의 (가)(나)(다) 값 $p,q,r$에 대해 $p\\times q\\times r^2$의 값은? (단, $\\angle APB<\\angle AQB$)',
    answer: '20√2/19 (①)',
    verifier: '사인법칙 $\\sin(\\theta_1{+}\\theta_2)=\\frac{5\\sqrt3}{9}{=}p$ · $\\overline{QB}{=}q\\overline{QA},\\ q{=}\\frac{\\sqrt6}{2}$ · 코사인법칙 $\\overline{QA}^2{=}\\frac{24}{19}{=}r^2$ → $p\\,q\\,r^2{=}\\frac{20\\sqrt2}{19}$',
    figure: <Geometry spec={TWO_CIRCLES} />,
  },
];

export default function VariantsDemo() {
  const [reveal, setReveal] = useState<Record<number, boolean>>({});
  return (
    <div className="space-y-6 text-[color:var(--color-text)]">
      <div className="rounded-lg bg-[color:var(--color-surface)] border border-[color:var(--color-border)] p-4 text-sm text-[color:var(--color-muted)]">
        검증기(원본 문제의 수학 구조를 코드로 인코딩)를 <b className="text-zinc-100">씨앗 + 자동채점기</b>로 써서 만든 변형 3종입니다.
        각 변형은 <b className="text-zinc-100">새 검증기로 정답이 자동 검증됨</b>(VERIFY_PASS). 도형은 PNG가 아니라 <code className="text-zinc-300">Graph</code>/<code className="text-zinc-300">Geometry</code>
        spec(좌표는 sympy 계산)으로 렌더 — 숫자만 바꿔 무한 생성·렌더 가능.
      </div>
      {VARIANTS.map((v, i) => (
        <section key={i} className="rounded-xl border border-[color:var(--color-border)] bg-[color:var(--color-surface)] shadow-sm overflow-hidden">
          <div className="flex items-center gap-3 px-5 py-3 border-b border-[color:var(--color-border)] bg-[color:var(--color-surface-2)]">
            <span className={`text-xs font-semibold px-2.5 py-1 rounded-full border ${v.tone}`}>{v.cat}</span>
            <span className="text-sm text-[color:var(--color-muted)]">개념: <b className="text-zinc-200"><MathText text={v.concept} /></b></span>
          </div>
          <div className="px-5 py-4">
            <p className="text-[11px] text-[color:var(--color-subtle)] mb-2"><MathText text={v.source} /></p>
            <p className="text-[15px] leading-relaxed text-zinc-100"><MathText text={v.statement} /></p>
            {v.figure && (
              <div className="mt-4 flex justify-center rounded-lg bg-[color:var(--color-surface-2)] border border-[color:var(--color-border)] py-3">
                {v.figure}
              </div>
            )}
            <div className="mt-4 flex items-center gap-3 flex-wrap">
              <button
                onClick={() => setReveal((r) => ({ ...r, [i]: !r[i] }))}
                className="text-sm px-3 py-1.5 rounded-md bg-indigo-600 text-white hover:bg-indigo-500 transition">
                {reveal[i] ? '정답 숨기기' : '정답·검증 보기'}
              </button>
              {reveal[i] && (
                <div className="text-sm text-zinc-300">
                  정답 <b className="text-lg text-zinc-50">{v.answer}</b>
                  <span className="ml-3 inline-flex items-center gap-1 text-emerald-400 font-medium">✓ 검증기 통과</span>
                  <div className="mt-1 text-xs text-[color:var(--color-subtle)] font-mono">{v.verifier}</div>
                </div>
              )}
            </div>
          </div>
        </section>
      ))}
    </div>
  );
}
