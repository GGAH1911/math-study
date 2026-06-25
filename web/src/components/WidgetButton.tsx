import { useState, useEffect } from 'react';
import Interactive from './Interactive';
import type { InteractiveSpec } from '../data/interactive-samples';

// 본문 버튼 → 모달 팝업으로 InteractiveSpec 위젯을 띄운다.
//   설계(사장님): 본문 내용을 가리지 않게 버튼만 두고, 클릭 시 모달에서 슬라이더 조작.
//   캔버스 인라인이 아니라 모달이라 모바일 스크롤 터치와 겹치지 않음.
export default function WidgetButton({ spec, label }: { spec: InteractiveSpec; label?: string }) {
  const [open, setOpen] = useState(false);
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') setOpen(false); };
    document.addEventListener('keydown', onKey);
    const prev = document.body.style.overflow;
    document.body.style.overflow = 'hidden'; // 모달 열린 동안 배경 스크롤 잠금
    return () => { document.removeEventListener('keydown', onKey); document.body.style.overflow = prev; };
  }, [open]);

  return (
    <div style={{ margin: '20px 0' }}>
      <button
        type="button"
        onClick={() => setOpen(true)}
        style={{
          display: 'inline-flex', alignItems: 'center', gap: 8,
          padding: '10px 16px', borderRadius: 12, cursor: 'pointer',
          background: 'var(--color-accent)', color: '#fff', fontWeight: 600, fontSize: 14,
          border: '1px solid var(--color-accent)', boxShadow: '0 1px 2px rgba(0,0,0,0.08)',
        }}
      >
        🔭 인터랙티브로 탐구하기{label ? ` — ${label}` : ''}
      </button>

      {open && (
        <div
          onClick={() => setOpen(false)}
          style={{
            position: 'fixed', inset: 0, zIndex: 1000, background: 'rgba(0,0,0,0.5)',
            display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 16,
          }}
        >
          <div
            onClick={(e) => e.stopPropagation()}
            style={{
              background: 'var(--color-surface)', borderRadius: 16, padding: '18px 20px 22px',
              maxWidth: 'min(560px, 95vw)', maxHeight: '90vh', overflow: 'auto',
              border: '1px solid var(--color-border)', boxShadow: '0 10px 40px rgba(0,0,0,0.3)',
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
              <span style={{ fontSize: 13, fontWeight: 700, color: 'var(--color-muted)', letterSpacing: '0.02em' }}>🔭 개념 탐구 · 인터랙티브</span>
              <button
                type="button" onClick={() => setOpen(false)} aria-label="닫기"
                style={{ border: 'none', background: 'transparent', cursor: 'pointer', fontSize: 18, color: 'var(--color-muted)', lineHeight: 1, padding: 4 }}
              >✕</button>
            </div>
            <Interactive spec={spec} interactive />
          </div>
        </div>
      )}
    </div>
  );
}
