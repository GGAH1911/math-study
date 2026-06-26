// 남용방지 rate limit — 슬라이딩 윈도우(인메모리). 비싼 엔드포인트(LLM·sympy) per-user 제한.
//   ★단일 인스턴스 전제(현재 PaaS 단일 컨테이너). 멀티인스턴스로 확장 시 Redis 등 공유 스토어 필요.
//   ★빌링 메터링이 아니라 DoS/스팸 방지용 — 결제/쿼터 정산은 별도(향후).
const buckets = new Map<string, number[]>();
let lastSweep = 0;

/** key 가 windowMs 안에서 limit 회 미만이면 통과(true, 타임스탬프 기록), 초과면 false. */
export function rateLimit(key: string, limit: number, windowMs: number): boolean {
  const now = Date.now();
  const arr = (buckets.get(key) ?? []).filter((t) => now - t < windowMs);
  if (arr.length >= limit) { buckets.set(key, arr); return false; }
  arr.push(now);
  buckets.set(key, arr);
  return true;
}

/** 오래된 버킷 주기적 정리(메모리 누수 방지). windowMs 간격으로만 실제 수행. */
export function sweep(windowMs: number): void {
  const now = Date.now();
  if (now - lastSweep < windowMs) return;
  lastSweep = now;
  for (const [k, arr] of buckets) {
    const kept = arr.filter((t) => now - t < windowMs);
    if (kept.length) buckets.set(k, kept); else buckets.delete(k);
  }
}
