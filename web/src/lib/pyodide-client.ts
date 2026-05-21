// 클라이언트 sympy 실행. /public/pyodide-worker.js 와 통신.
// 첫 호출 시 worker 생성 + pyodide 초기화 (~3-5초). 후속 호출은 빠름.
//
// fallback: pyodide 가 로드 실패하거나 worker 미지원 환경이면
// 호출자가 catch 해서 서버 /api/sympy 로 우회 가능.

type RunResult = { ok: boolean; stdout?: string; stderr?: string };

let worker: Worker | null = null;
let nextId = 0;
const pending = new Map<number, (r: RunResult) => void>();

function ensureWorker(): Worker {
  if (worker) return worker;
  worker = new Worker('/pyodide-worker.js');
  worker.onmessage = (e: MessageEvent) => {
    const { id, ok, stdout, stderr } = e.data ?? {};
    const cb = pending.get(id);
    if (cb) {
      pending.delete(id);
      cb({ ok: !!ok, stdout, stderr });
    }
  };
  worker.onerror = (err) => {
    console.error('[pyodide-worker] error', err);
    // 진행 중인 모든 호출 실패 처리
    for (const [id, cb] of pending) {
      pending.delete(id);
      cb({ ok: false, stderr: `worker error: ${err.message}` });
    }
  };
  return worker;
}

export function runSympyLocal(code: string): Promise<RunResult> {
  if (typeof window === 'undefined') {
    return Promise.reject(new Error('no window — server context'));
  }
  if (typeof Worker === 'undefined') {
    return Promise.reject(new Error('Worker API not available'));
  }
  const w = ensureWorker();
  return new Promise<RunResult>((resolve) => {
    const id = ++nextId;
    pending.set(id, resolve);
    w.postMessage({ id, type: 'run', code });
  });
}

// 선제적 워커 미리 띄우기 — 사용자가 채팅 페이지 열면 background 로 pyodide
// 로드 시작 → 첫 sympy 호출 시 대기 시간 단축.
export function prewarmPyodide(): void {
  if (typeof window === 'undefined' || typeof Worker === 'undefined') return;
  const w = ensureWorker();
  // ping 으로 worker 생성만 보장 — 실제 init 은 첫 run 호출 때.
  // 더 적극적으로 init 하려면 type='warmup' 추가 가능. 일단 lazy.
  w.postMessage({ id: -1, type: 'ping' });
}
