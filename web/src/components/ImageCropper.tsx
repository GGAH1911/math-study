import { useEffect, useRef, useState } from 'react';
import { loadImage, cropRegion, downscaleFull, VISION_LONG_EDGE } from '../lib/image-utils';

type Props = { src: string; onCrop: (dataUrl: string) => void; onCancel: () => void };
type Rect = { x: number; y: number; w: number; h: number };

// 큰 이미지(긴 변>2200 또는 면적>2.4MP)를 첨부할 때 학생이 문제 영역만 잘라
// 1568 안으로 보내도록 하는 자체 크롭 모달. 라이브러리 없이 <img>+canvas.
export default function ImageCropper({ src, onCrop, onCancel }: Props) {
  const [img, setImg] = useState<HTMLImageElement | null>(null);
  const [sel, setSel] = useState<Rect | null>(null);
  const imgRef = useRef<HTMLImageElement | null>(null);     // 화면에 표시되는 <img>
  const dragStart = useRef<{ x: number; y: number } | null>(null);

  useEffect(() => { loadImage(src).then(setImg).catch(() => onCancel()); }, [src]);

  // 표시 좌표 → 원본 픽셀 좌표 (표시 img의 렌더 크기 기준 스케일).
  const toOrig = (r: Rect): Rect => {
    const el = imgRef.current!;
    const sx = img!.naturalWidth / el.clientWidth;
    const sy = img!.naturalHeight / el.clientHeight;
    return { x: r.x * sx, y: r.y * sy, w: r.w * sx, h: r.h * sy };
  };

  const onPointerDown = (e: React.PointerEvent) => {
    const el = imgRef.current!;
    const rect = el.getBoundingClientRect();
    const x = e.clientX - rect.left, y = e.clientY - rect.top;
    dragStart.current = { x, y };
    setSel({ x, y, w: 0, h: 0 });
    el.setPointerCapture(e.pointerId);
  };
  const onPointerMove = (e: React.PointerEvent) => {
    if (!dragStart.current) return;
    const el = imgRef.current!;
    const rect = el.getBoundingClientRect();
    const cx = Math.max(0, Math.min(e.clientX - rect.left, el.clientWidth));
    const cy = Math.max(0, Math.min(e.clientY - rect.top, el.clientHeight));
    const s = dragStart.current;
    setSel({ x: Math.min(s.x, cx), y: Math.min(s.y, cy), w: Math.abs(cx - s.x), h: Math.abs(cy - s.y) });
  };
  const onPointerUp = () => { dragStart.current = null; };

  const hasSelection = !!sel && sel.w > 8 && sel.h > 8;
  // 1568 가이드: 선택 영역을 원본 픽셀로 환산한 긴 변이 1568을 넘으면 축소됨.
  const willDownscale = hasSelection && img
    ? (() => { const o = toOrig(sel!); return Math.max(o.w, o.h) > VISION_LONG_EDGE; })()
    : false;

  const useSelection = () => {
    if (!img || !hasSelection) return;
    const o = toOrig(sel!);
    onCrop(cropRegion(img, o.x, o.y, o.w, o.h));
  };
  const useFull = () => { if (img) onCrop(downscaleFull(img)); };

  return (
    <div className="fixed inset-0 z-50 bg-black/70 flex items-center justify-center p-4" onClick={onCancel}>
      <div
        className="bg-[color:var(--color-bg)] border border-[color:var(--color-border)] rounded-lg p-4 max-w-[90vw] flex flex-col gap-3"
        onClick={(e) => e.stopPropagation()}
      >
        <p className="text-sm text-[color:var(--color-muted)]">
          큰 이미지예요 — 문제 영역을 드래그해 선택하거나 <b className="text-[color:var(--color-fg)]">전체 사용</b>을 누르세요.
        </p>
        <div className="relative overflow-auto" style={{ maxHeight: '70vh' }}>
          <img
            ref={imgRef}
            src={src}
            alt="크롭 대상"
            className="max-w-full select-none touch-none block"
            style={{ maxHeight: '70vh' }}
            draggable={false}
            onPointerDown={onPointerDown}
            onPointerMove={onPointerMove}
            onPointerUp={onPointerUp}
          />
          {sel && (
            <div
              className="absolute border-2 pointer-events-none"
              style={{
                left: sel.x, top: sel.y, width: sel.w, height: sel.h,
                borderColor: willDownscale ? '#eab308' : '#3b82f6',
                background: 'rgba(59,130,246,0.12)',
              }}
            />
          )}
        </div>
        {willDownscale && (
          <p className="text-xs text-amber-400">⚠ 선택 영역이 1568px보다 커서 축소돼요 — 글자가 작아질 수 있어요.</p>
        )}
        <div className="flex gap-2 justify-end">
          <button type="button" onClick={onCancel} className="chip opacity-70 hover:opacity-100">취소</button>
          <button type="button" onClick={useFull} className="chip hover:opacity-100">전체 사용</button>
          <button type="button" onClick={useSelection} disabled={!hasSelection}
            className="chip border-[color:var(--color-accent)] hover:opacity-100 disabled:opacity-40 disabled:cursor-not-allowed">
            선택 영역 사용
          </button>
        </div>
      </div>
    </div>
  );
}
