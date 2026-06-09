// Thin React wrapper around MathLive's <math-field> web component.
// - Controlled input (value / onChange returns LaTeX)
// - onSubmit fires on Enter (Shift+Enter inserts newline inside the field)
// - Auto-focuses on mount when `autoFocus`
// - Dark-mode styled to match the rest of the UI
import { useEffect, useRef } from 'react';

// React 19 + @types/react@19 는 JSX 네임스페이스가 전역 `JSX` 가 아니라 `react`
// 모듈 안(`React.JSX`)에 있다. 따라서 커스텀 엘리먼트는 전역이 아니라 react 모듈을
// augment 해야 인식된다(전역 augment 는 무시됨 → ts2339). MathLive 의 <math-field>
// 는 서드파티 웹컴포넌트라 prop 타입은 any 로 둔다.
declare module 'react' {
  // eslint-disable-next-line @typescript-eslint/no-namespace
  namespace JSX {
    interface IntrinsicElements {
      'math-field': any;
    }
  }
}

type Props = {
  value: string;                        // LaTeX
  onChange: (latex: string) => void;
  onSubmit?: () => void;                 // Enter without shift
  placeholder?: string;
  autoFocus?: boolean;
  className?: string;
  rows?: number;                         // visual hint for height
  disabled?: boolean;
};

let MATHLIVE_LOADED: Promise<void> | null = null;
function ensureMathLive(): Promise<void> {
  if (typeof window === 'undefined') return Promise.resolve();
  if (MATHLIVE_LOADED) return MATHLIVE_LOADED;
  MATHLIVE_LOADED = import('mathlive').then(() => {
    // mathlive auto-registers <math-field> when imported
  });
  return MATHLIVE_LOADED;
}

export default function MathField({
  value, onChange, onSubmit, placeholder, autoFocus, className, rows = 2, disabled,
}: Props) {
  const ref = useRef<HTMLElement | null>(null);
  const ready = useRef(false);

  // Load MathLive once, then mark ready
  useEffect(() => {
    let cancelled = false;
    ensureMathLive().then(() => {
      if (!cancelled) ready.current = true;
      // Force re-attach options after load
      const el = ref.current as (HTMLElement & { setOptions?: (o: unknown) => void; value?: string }) | null;
      if (el) {
        // Configure
        el.setAttribute('virtual-keyboard-mode', 'manual');
        el.setAttribute('smart-mode', 'on');
        el.setAttribute('math-mode-space', 'space');
        if (autoFocus) {
          setTimeout(() => (el as HTMLElement & { focus?: () => void }).focus?.(), 0);
        }
      }
    });
    return () => { cancelled = true; };
  }, [autoFocus]);

  // Sync external value → element
  useEffect(() => {
    const el = ref.current as (HTMLElement & { value?: string }) | null;
    if (!el) return;
    if (el.value !== value) el.value = value;
  }, [value]);

  // Wire input + Enter handler
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const onInput = (e: Event) => {
      const t = e.target as HTMLElement & { value?: string };
      if (typeof t.value === 'string') onChange(t.value);
    };
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Enter' && !e.shiftKey && onSubmit) {
        e.preventDefault();
        onSubmit();
      }
    };
    el.addEventListener('input', onInput);
    el.addEventListener('keydown', onKey);
    return () => {
      el.removeEventListener('input', onInput);
      el.removeEventListener('keydown', onKey);
    };
  }, [onChange, onSubmit]);

  // Toggle disabled
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (disabled) el.setAttribute('readonly', '');
    else el.removeAttribute('readonly');
  }, [disabled]);

  return (
    <math-field
      ref={ref as unknown as React.Ref<HTMLElement>}
      style={{
        minHeight: `${1.5 + 1.4 * rows}rem`,
        fontSize: '1rem',
        padding: '0.5rem 0.75rem',
        background: 'var(--color-surface-2, #18181b)',
        border: '1px solid var(--color-border, #27272a)',
        borderRadius: '0.5rem',
        color: 'var(--color-text, #fafafa)',
        outline: 'none',
        display: 'block',
        width: '100%',
      }}
      class={className}
      data-placeholder={placeholder}
    />
  );
}
