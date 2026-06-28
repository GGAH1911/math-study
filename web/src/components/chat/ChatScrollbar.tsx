// 튜터 채팅 커스텀 스크롤바 — ChatPanel 에서 분리(동작 무변). 네이티브 스크롤바는 숨기고 JS 로
// thumb/track 을 그려 스트리밍 중에도 정확히 추종.
import React, { useState, useRef, useEffect, useCallback } from 'react';

export function clampNum(v: number, lo: number, hi: number): number {
  return v < lo ? lo : v > hi ? hi : v;
}
export default function ChatScrollbar({ targetRef }: { targetRef: React.RefObject<HTMLDivElement | null> }) {
  const trackRef = useRef<HTMLDivElement | null>(null);
  const thumbRef = useRef<HTMLDivElement | null>(null);
  const dragRef = useRef<{ startY: number; startScroll: number; maxTop: number; scrollable: number } | null>(null);
  const [overflow, setOverflow] = useState(false);

  // scroll 상태 → thumb 기하 동기화. 스트리밍으로 내용이 늘어도 항상 정확히 추종.
  const sync = useCallback(() => {
    const el = targetRef.current;
    const track = trackRef.current;
    const thumb = thumbRef.current;
    if (!el || !track || !thumb) return;
    const scrollable = el.scrollHeight - el.clientHeight;
    if (scrollable <= 2) { setOverflow(false); return; }
    setOverflow(true);
    const trackH = track.clientHeight;
    const thumbH = Math.max(40, (el.clientHeight / el.scrollHeight) * trackH); // 최소 40px — 손으로 잡기 쉽게
    const maxTop = Math.max(0, trackH - thumbH);
    const top = clampNum((el.scrollTop / scrollable) * maxTop, 0, maxTop);
    thumb.style.height = `${thumbH}px`;
    thumb.style.transform = `translateY(${top}px)`;
  }, [targetRef]);

  useEffect(() => {
    const el = targetRef.current;
    if (!el) return;
    sync();
    el.addEventListener('scroll', sync, { passive: true });
    const ro = new ResizeObserver(sync);
    ro.observe(el);
    const mo = new MutationObserver(sync);
    mo.observe(el, { childList: true, subtree: true, characterData: true });
    window.addEventListener('resize', sync);
    return () => {
      el.removeEventListener('scroll', sync);
      ro.disconnect();
      mo.disconnect();
      window.removeEventListener('resize', sync);
    };
  }, [targetRef, sync]);

  // 드래그 시작 — fromTrack 이면 클릭 위치로 thumb 중심을 점프시킨 뒤 그 지점부터 드래그.
  const beginDrag = useCallback((clientY: number, fromTrack: boolean) => {
    const el = targetRef.current;
    const track = trackRef.current;
    const thumb = thumbRef.current;
    if (!el || !track || !thumb) return;
    const trackH = track.clientHeight;
    const thumbH = thumb.offsetHeight;
    const maxTop = Math.max(1, trackH - thumbH);
    const scrollable = el.scrollHeight - el.clientHeight;
    if (fromTrack) {
      const rect = track.getBoundingClientRect();
      const desiredTop = clampNum(clientY - rect.top - thumbH / 2, 0, maxTop);
      // behavior:'instant' — 컨테이너의 scroll-behavior:smooth 가 직접 scrollTop 쓰기를
      // 애니메이션해 드래그가 기어가는 버그(관측)를 우회. 드래그는 항상 즉시 반영.
      el.scrollTo({ top: (desiredTop / maxTop) * scrollable, behavior: 'instant' as ScrollBehavior });
    }
    dragRef.current = { startY: clientY, startScroll: el.scrollTop, maxTop, scrollable };
  }, [targetRef]);

  // 전역 pointermove/up — thumb 밖으로 손가락이 벗어나도 계속 추종(setPointerCapture 대신 window).
  useEffect(() => {
    const onMove = (e: PointerEvent) => {
      const drag = dragRef.current;
      const el = targetRef.current;
      if (!drag || !el) return;
      e.preventDefault();
      const dy = e.clientY - drag.startY;
      const top = clampNum(drag.startScroll + (dy / drag.maxTop) * drag.scrollable, 0, drag.scrollable);
      // instant — scroll-behavior:smooth 가 드래그 중 매 쓰기를 애니메이션해 멈칫대는 것 방지.
      el.scrollTo({ top, behavior: 'instant' as ScrollBehavior });
    };
    const onUp = () => { dragRef.current = null; };
    window.addEventListener('pointermove', onMove, { passive: false });
    window.addEventListener('pointerup', onUp);
    window.addEventListener('pointercancel', onUp);
    return () => {
      window.removeEventListener('pointermove', onMove);
      window.removeEventListener('pointerup', onUp);
      window.removeEventListener('pointercancel', onUp);
    };
  }, [targetRef]);

  return (
    <div
      ref={trackRef}
      className="chat-scrollbar-track"
      data-visible={overflow ? '1' : '0'}
      aria-hidden="true"
      onPointerDown={(e) => {
        if (e.target === thumbRef.current) return; // thumb 가 자체 처리
        e.preventDefault();
        beginDrag(e.clientY, true);
      }}
    >
      <div
        ref={thumbRef}
        className="chat-scrollbar-thumb"
        onPointerDown={(e) => {
          e.preventDefault();
          e.stopPropagation();
          beginDrag(e.clientY, false);
        }}
      />
    </div>
  );
}
