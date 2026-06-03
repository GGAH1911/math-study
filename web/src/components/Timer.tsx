import { useEffect, useRef, useState } from 'react';

// 카운트다운 타이머. 0 도달 시 onExpire 1회 호출(자동 제출). 5분 이하 빨강.
export default function Timer({ seconds, onExpire, paused = false }: {
  seconds: number;
  onExpire: () => void;
  paused?: boolean;
}) {
  const [left, setLeft] = useState(seconds);
  const fired = useRef(false);

  useEffect(() => {
    if (paused) return;
    const t = setInterval(() => setLeft((l) => Math.max(0, l - 1)), 1000);
    return () => clearInterval(t);
  }, [paused]);

  useEffect(() => {
    if (left === 0 && !fired.current) {
      fired.current = true;
      onExpire();
    }
  }, [left, onExpire]);

  const mm = Math.floor(left / 60);
  const ss = left % 60;
  const warn = left <= 300;
  return (
    <span className={`tabular-nums font-mono text-sm ${warn ? 'text-rose-400' : 'text-zinc-200'}`}>
      ⏱ {String(mm).padStart(2, '0')}:{String(ss).padStart(2, '0')}
    </span>
  );
}
