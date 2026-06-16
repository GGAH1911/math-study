// PaperHero — 홈 히어로 「오늘의 작도」 (디자인 계약 §9-B).
// '오늘의 개념'을 나타내는 도형/곡선이 컴퍼스 보조선과 함께 캔버스에 스스로 작도된다.
// 그림 데이터(stroke 좌표)는 개념별로 LLM이 미리 생성해 캐시한 figure spec 을 props 로 받는다
// (없으면 일반 곡선 폴백). 의존성 0(React 훅만) · rAF 핸들 1개 · 재생 완료 즉시 rAF 해제.
// 테마 추종은 getComputedStyle 1회 캐싱 + html class MutationObserver — §14-C 계약의 1호 구현.
import { useEffect, useRef } from 'react';

// 결정적 PRNG (계약 리터럴 mulberry32) — wobble 질감 시드용.
function mulberry32(a: number) {
  return function () {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
// 라벨 → 안정 시드(개념마다 wobble 질감 고정).
function hashStr(s: string): number {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
  return h >>> 0;
}

const N = 240; // 폴백 곡선 샘플 수

type Stroke = { pts: number[]; dash: boolean; hover: boolean }; // pts = [x0,y0,x1,y1,...] (월드 좌표)
type Scene = { strokes: Stroke[]; label: string; guideCircle: number | null; equalScale: boolean; wob: Float32Array };
// 개념별 LLM 생성 figure spec(캐시) — scripts/gen_daily_illustration.mjs 가 만든 스키마.
export type FigureSpec = {
  strokes: Array<{ pts: number[]; dash?: boolean; hover?: boolean }>;
  guideCircle?: number | null;
  equalScale?: boolean;
};

// figure spec(개념별 LLM 생성·캐시) → Scene. spec 없거나 부실하면 일반 곡선으로 폴백.
// 좌표는 그대로 두고 fit() 이 데이터 bbox 에 맞춰 프레이밍한다. seed 는 wobble 질감 전용.
function sceneFromSpec(spec: FigureSpec | null | undefined, label: string, seed: number): Scene {
  const rnd = mulberry32(seed);
  let strokes: Stroke[] = [];
  let guideCircle: number | null = null;
  let equalScale = false;

  if (spec && Array.isArray(spec.strokes)) {
    for (const s of spec.strokes) {
      if (!s || !Array.isArray(s.pts) || s.pts.length < 4) continue;
      // 유한·범위 검증(±6 안). 이상치 stroke 는 버린다.
      const ok = s.pts.every((v) => Number.isFinite(v) && Math.abs(v) <= 6) && s.pts.length % 2 === 0;
      if (!ok) continue;
      strokes.push({ pts: s.pts.slice(), dash: !!s.dash, hover: !!s.hover });
    }
    if (typeof spec.guideCircle === 'number' && Number.isFinite(spec.guideCircle)) guideCircle = spec.guideCircle;
    equalScale = !!spec.equalScale;
  }

  // 폴백 — 부드러운 일반 곡선(특정 개념 안 뜻함, 안정적).
  if (!strokes.length) {
    const a: number[] = [];
    for (let i = 0; i < N; i++) {
      const x = -3 + (6 * i) / (N - 1);
      a.push(x, Math.sin((Math.PI * x) / 2));
    }
    strokes = [{ pts: a, dash: false, hover: true }];
    guideCircle = null;
    equalScale = false;
  }

  // 연필 wobble 테이블 — 점당 (dx,dy) 사전계산, 매 프레임 rnd 호출 금지(손그림 질감).
  let total = 0;
  for (const s of strokes) total += s.pts.length / 2;
  const wob = new Float32Array(total * 2);
  for (let i = 0; i < wob.length; i++) wob[i] = (rnd() * 2 - 1) * 0.7;
  return { strokes, label, guideCircle, equalScale, wob };
}

export default function PaperHero({ spec = null, label = '' }: { spec?: FigureSpec | null; label?: string }) {
  const wrapRef = useRef<HTMLDivElement>(null);
  const cvRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const wrap = wrapRef.current;
    const cv = cvRef.current;
    if (!wrap || !cv) return;
    const ctx = cv.getContext('2d');
    if (!ctx) return;

    // 개념별 figure spec(props)으로 장면 구성. spec 없으면 일반 곡선 폴백. seed=라벨 해시(질감 고정).
    const scene = sceneFromSpec(spec, label, hashStr(label || 'paper-hero'));

    // 데이터 bbox 로 프레이밍(x·y 둘 다) — 도형이든 곡선이든 캔버스에 알맞게 채운다.
    let xMin = Infinity, xMax = -Infinity, yMin = Infinity, yMax = -Infinity;
    for (const s of scene.strokes)
      for (let i = 0; i + 1 < s.pts.length; i += 2) {
        const x = s.pts[i], y = s.pts[i + 1];
        if (Number.isFinite(x) && Number.isFinite(y) && Math.abs(y) <= 5 && Math.abs(x) <= 5) {
          if (x < xMin) xMin = x; if (x > xMax) xMax = x;
          if (y < yMin) yMin = y; if (y > yMax) yMax = y;
        }
      }
    if (!Number.isFinite(xMin) || xMax - xMin < 0.3) { xMin = -3; xMax = 3; }
    if (!Number.isFinite(yMin) || yMax - yMin < 0.3) { yMin = -1.5; yMax = 1.5; }
    const padX = (xMax - xMin) * 0.08, padY = (yMax - yMin) * 0.12;
    xMin -= padX; xMax += padX; yMin -= padY; yMax += padY;

    // 뷰 변환(월드→스크린) — 리사이즈 때만 갱신
    const view = { w: 0, h: 0, sx: 1, sy: 1, ox: 0, oy: 0 };
    const X = (x: number) => view.ox + x * view.sx;
    const Y = (y: number) => view.oy - y * view.sy;
    function fit() {
      const w = wrap!.clientWidth || 1;
      const h = wrap!.clientHeight || 1;
      const dpr = Math.min(window.devicePixelRatio || 1, 2); // DPR ≤ 2
      cv!.width = Math.max(1, Math.round(w * dpr));
      cv!.height = Math.max(1, Math.round(h * dpr));
      ctx!.setTransform(dpr, 0, 0, dpr, 0, 0);
      let sx = (w - 40) / (xMax - xMin);
      let sy = (h - 32) / (yMax - yMin);
      if (scene.equalScale || scene.guideCircle != null) sx = sy = Math.min(sx, sy); // 도형은 안 찌그러뜨림
      view.w = w;
      view.h = h;
      view.sx = sx;
      view.sy = sy;
      view.ox = w / 2 - ((xMin + xMax) / 2) * sx;
      view.oy = h / 2 + ((yMin + yMax) / 2) * sy;
    }

    // 테마 색 — 마운트·html.dark 토글 시 1회 캐싱 (§14-C)
    const col = { main: '#39487D', guide: '#D7CDB5', label: '#6B6350' };
    function cacheColors() {
      const cs = getComputedStyle(document.documentElement);
      col.main = cs.getPropertyValue('--color-accent').trim() || col.main;
      col.guide = cs.getPropertyValue('--color-border-strong').trim() || col.guide;
      col.label = cs.getPropertyValue('--ink-muted').trim() || col.label;
    }

    // 한 획(연필 2겹 중 1겹) — frac 만큼 좌→우 진행, 사전계산 wobble 적용
    function trace(s: Stroke, wo: number, frac: number, dx: number, dy: number) {
      const n = s.pts.length / 2;
      const fi = Math.max(0.02, (n - 1) * frac); // 진행 float 인덱스 — 2점 직선도 점진 진행
      const li = Math.min(n - 1, Math.floor(fi));
      ctx!.beginPath();
      for (let i = 0; i <= li; i++) {
        const px = X(s.pts[i * 2]) + scene.wob[(wo + i) * 2] + dx;
        const py = Y(s.pts[i * 2 + 1]) + scene.wob[(wo + i) * 2 + 1] + dy;
        if (i === 0) ctx!.moveTo(px, py);
        else ctx!.lineTo(px, py);
      }
      if (li < n - 1) {
        const t = fi - li;
        const x = s.pts[li * 2] + (s.pts[(li + 1) * 2] - s.pts[li * 2]) * t;
        const y = s.pts[li * 2 + 1] + (s.pts[(li + 1) * 2 + 1] - s.pts[li * 2 + 1]) * t;
        ctx!.lineTo(X(x) + dx, Y(y) + dy);
      }
      ctx!.stroke();
    }

    // 3단계 합성 렌더: p1 보조선 페이드 / p2 본 곡선 진행 / p3 라벨 페이드
    function render(p1: number, p2: number, p3: number) {
      ctx!.clearRect(0, 0, view.w, view.h);
      if (p1 > 0 && scene.guideCircle != null) {
        // ① 컴퍼스 보조원만(원 관련 개념일 때). x/y 좌표축·중심점은 폐지 —
        //    도형 그래픽(삼각형·벡터 등)엔 무의미한 노이즈라 어떤 그래픽에도 안 그린다(사용자 지침).
        ctx!.globalAlpha = p1;
        ctx!.strokeStyle = col.guide;
        ctx!.lineWidth = 1;
        ctx!.setLineDash([5, 6]);
        ctx!.beginPath();
        ctx!.arc(X(0), Y(0), scene.guideCircle * view.sx, 0, Math.PI * 2);
        ctx!.stroke();
        ctx!.setLineDash([]);
        ctx!.globalAlpha = 1;
      }
      if (p2 > 0) {
        // ② 본 곡선 — 같은 path 를 0.55 알파 × 2겹(흑연 질감)
        ctx!.strokeStyle = col.main;
        ctx!.lineWidth = 1.6;
        ctx!.lineJoin = 'round';
        ctx!.lineCap = 'round';
        let wo = 0;
        for (const s of scene.strokes) {
          ctx!.setLineDash(s.dash ? [6, 5] : []);
          ctx!.globalAlpha = 0.55;
          trace(s, wo, p2, 0, 0);
          trace(s, wo, p2, 0.5, -0.4);
          ctx!.globalAlpha = 1;
          wo += s.pts.length / 2;
        }
        ctx!.setLineDash([]);
      }
      if (p3 > 0) {
        // ③ 끝점 라벨 — 마지널리아(Nanum Pen)
        const e = scene.strokes[0].pts;
        const ex = X(e[e.length - 2]);
        const ey = Y(e[e.length - 1]);
        ctx!.globalAlpha = p3;
        ctx!.font = '18px "Nanum Pen Script", "Gowun Batang", cursive';
        ctx!.fillStyle = col.label;
        const tw = ctx!.measureText(scene.label).width;
        ctx!.fillText(
          scene.label,
          Math.min(Math.max(ex - tw - 10, 6), view.w - tw - 6),
          Math.min(Math.max(ey - 10, 20), view.h - 8),
        );
        ctx!.globalAlpha = 1;
      }
    }
    const drawStatic = () => render(1, 1, 1); // 완성 정지 화면

    // ── 재생 제어: rAF 핸들은 raf 하나뿐 ─────────────────────────
    let raf = 0;
    let playing = false;
    let idleBlank = false; // 데스크톱: IO 발화 전까지는 빈 캔버스 유지(완성본 선노출 방지)
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const desktop = window.matchMedia('(min-width: 640px)').matches;
    const DUR = 2300;

    function play() {
      if (playing) return;
      if (reduced) {
        drawStatic(); // 모션 감수성: 애니메이션 전부 생략, 완성 정지 화면만
        return;
      }
      if (raf) cancelAnimationFrame(raf); // 잔여 호버 rAF 회수
      idleBlank = false;
      playing = true;
      const t0 = performance.now();
      const step = (now: number) => {
        const t = now - t0;
        const p1 = Math.min(t / 400, 1);
        const r = Math.min(Math.max((t - 400) / 1600, 0), 1);
        const p2 = r < 0.5 ? 2 * r * r : 1 - Math.pow(-2 * r + 2, 2) / 2; // ease-in-out
        const p3 = Math.min(Math.max((t - 2000) / 300, 0), 1);
        render(p1, p2, p3);
        if (t < DUR) {
          raf = requestAnimationFrame(step);
        } else {
          raf = 0; // 재생 완료 즉시 해제 — idle CPU 0
          playing = false;
        }
      };
      raf = requestAnimationFrame(step);
    }

    // 호버: 최근접 샘플점 + 접선 세그먼트 + 좌표 — 이벤트당 단발 rAF(상시 루프 없음)
    function drawHover(px: number, py: number) {
      let bi = -1;
      let bs = -1;
      let bd = 3600; // 60px 이내만 반응
      for (let si = 0; si < scene.strokes.length; si++) {
        const s = scene.strokes[si];
        if (!s.hover) continue;
        const n = s.pts.length / 2;
        for (let i = 0; i < n; i++) {
          const dx = X(s.pts[i * 2]) - px;
          const dy = Y(s.pts[i * 2 + 1]) - py;
          const d = dx * dx + dy * dy;
          if (d < bd) {
            bd = d;
            bi = i;
            bs = si;
          }
        }
      }
      drawStatic();
      if (bs < 0) return;
      const s = scene.strokes[bs];
      const n = s.pts.length / 2;
      const x = s.pts[bi * 2];
      const y = s.pts[bi * 2 + 1];
      const i0 = Math.max(0, bi - 1);
      const i1 = Math.min(n - 1, bi + 1);
      // 접선 방향 = 이웃 샘플 차분(스크린 좌표)
      let tx = X(s.pts[i1 * 2]) - X(s.pts[i0 * 2]);
      let ty = Y(s.pts[i1 * 2 + 1]) - Y(s.pts[i0 * 2 + 1]);
      const L = Math.hypot(tx, ty) || 1;
      tx /= L;
      ty /= L;
      const cx = X(x);
      const cy = Y(y);
      ctx!.strokeStyle = col.main;
      ctx!.lineWidth = 1;
      ctx!.beginPath();
      ctx!.moveTo(cx - tx * 26, cy - ty * 26);
      ctx!.lineTo(cx + tx * 26, cy + ty * 26);
      ctx!.stroke();
      ctx!.fillStyle = col.main;
      ctx!.beginPath();
      ctx!.arc(cx, cy, 3, 0, Math.PI * 2);
      ctx!.fill();
      ctx!.font = '12px "IBM Plex Sans KR", sans-serif';
      ctx!.fillStyle = col.label;
      const txt = `(${x.toFixed(2)}, ${y.toFixed(2)})`;
      const tw = ctx!.measureText(txt).width;
      ctx!.fillText(txt, Math.min(Math.max(cx + 8, 4), view.w - tw - 4), Math.max(cy - 8, 14));
    }

    let pend: { x: number; y: number } | null = null;
    const onMove = (e: PointerEvent) => {
      if (playing || idleBlank || e.pointerType === 'touch') return;
      const r = cv.getBoundingClientRect();
      pend = { x: e.clientX - r.left, y: e.clientY - r.top };
      if (!raf)
        raf = requestAnimationFrame(() => {
          raf = 0;
          if (!playing && pend) drawHover(pend.x, pend.y);
        });
    };
    const onLeave = () => {
      pend = null;
      if (!playing && !idleBlank) {
        if (raf) {
          cancelAnimationFrame(raf);
          raf = 0;
        }
        drawStatic();
      }
    };
    const onDown = () => {
      if (!desktop) play(); // 모바일: 탭 시 1회 재생(reduced 면 play 가 정지 화면만)
    };
    const onVis = () => {
      if (document.hidden) {
        if (raf) cancelAnimationFrame(raf);
        raf = 0;
        playing = false; // 숨김 → 즉시 정지
      } else if (!idleBlank) {
        drawStatic(); // 다음 가시화엔 정지 화면(재생 아님)
      }
    };

    cacheColors();
    fit();

    // 재생 트리거: 데스크톱 = IO 1회 / 모바일·reduced = 정지 화면 즉시
    let io: IntersectionObserver | null = null;
    if (reduced || !desktop) {
      drawStatic();
    } else {
      idleBlank = true;
      io = new IntersectionObserver(
        (es) => {
          if (es.some((en) => en.isIntersecting)) {
            io?.disconnect();
            io = null;
            play();
          }
        },
        { threshold: 0.35 },
      );
      io.observe(wrap);
    }

    // 리사이즈 → 정지 화면만 재그리기(재생 금지)
    const ro = new ResizeObserver(() => {
      fit();
      if (!playing && !idleBlank) drawStatic();
    });
    ro.observe(wrap);

    // 테마 토글 → 색 재캐싱 + 정지 화면 재그리기(§14-C)
    const mo = new MutationObserver(() => {
      cacheColors();
      if (!playing && !idleBlank) drawStatic();
    });
    mo.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });

    cv.addEventListener('pointermove', onMove);
    cv.addEventListener('pointerleave', onLeave);
    cv.addEventListener('pointerdown', onDown);
    document.addEventListener('visibilitychange', onVis);

    return () => {
      if (raf) cancelAnimationFrame(raf);
      io?.disconnect();
      ro.disconnect();
      mo.disconnect();
      cv.removeEventListener('pointermove', onMove);
      cv.removeEventListener('pointerleave', onLeave);
      cv.removeEventListener('pointerdown', onDown);
      document.removeEventListener('visibilitychange', onVis);
    };
  }, []);

  return (
    <div id="paper-hero" ref={wrapRef} className="relative mt-4 h-[140px] sm:h-[200px] md:h-[220px]">
      <canvas ref={cvRef} className="absolute inset-0 w-full h-full" aria-hidden="true" />
      <span className="sr-only">오늘의 작도</span>
    </div>
  );
}
