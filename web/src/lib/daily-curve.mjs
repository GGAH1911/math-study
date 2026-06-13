// 「오늘의 페이지」 히어로 곡선(날짜 시드 6종)과 각 곡선의 개념 노드·짧은 설명 매핑.
// ★ index 는 PaperHero.tsx 의 곡선 선택과 반드시 일치해야 한다(같은 KST 날짜 → seed % 6).
//   label 문자열도 PaperHero buildScene 의 label 과 동일하게 유지(둘 중 하나 바꾸면 같이).
// concept = /concepts/<id> 로 이어질 실제 노드 id(언더스코어 포함, concept-graph.json 검증됨).

export const DAILY_CURVES = [
  // k=0
  {
    label: 'y = sin x',
    blurb: '단위원의 y좌표가 그리는 곡선. 주기 2π로 −1과 1 사이를 매끄럽게 오르내립니다.',
    concept: 'functions/math-1/삼각함수',
    conceptLabel: '삼각함수',
  },
  // k=1
  {
    label: '포물선과 접선',
    blurb: '곡선 위 한 점에서의 접선 기울기가 곧 미분계수 — 그 점에서 곡선을 가장 닮은 직선입니다.',
    concept: 'functions/math-2/미분',
    conceptLabel: '미분',
  },
  // k=2
  {
    label: '원과 내접삼각형',
    blurb: '한 호에 대한 원주각은 어디서 보든 같고, 지름이 빗변이면 그 원주각은 직각입니다.',
    concept: 'geometry/middle-3/원의_성질',
    conceptLabel: '원의 성질',
  },
  // k=3
  {
    label: '지수와 로그',
    blurb: '지수함수와 로그함수는 y = x 에 대해 대칭인 역함수 관계 — 곱셈을 덧셈으로 바꿔줍니다.',
    concept: 'functions/math-1/지수함수와_로그함수',
    conceptLabel: '지수함수와 로그함수',
  },
  // k=4
  {
    label: '삼각함수의 합성',
    blurb: '여러 삼각함수를 더하면 새로운 주기 파형이 됩니다 — 복잡한 진동을 분해해 보는 출발점.',
    concept: 'functions/math-1/삼각함수',
    conceptLabel: '삼각함수',
  },
  // k=5
  {
    label: '정규분포 곡선',
    blurb: '평균을 중심으로 좌우대칭인 종 모양 분포. 자연·사회 현상의 흩어짐을 설명하는 통계의 핵심입니다.',
    concept: 'probability-stats/prob-stats-elective/통계/정규분포',
    conceptLabel: '정규분포',
  },
];

// KST 날짜 시드 → 곡선 index (PaperHero 와 동일 계산). nowMs = Date.now().
export function curveIndexForMs(nowMs) {
  const kst = new Date(nowMs + 9 * 3600 * 1000);
  const seed = kst.getUTCFullYear() * 10000 + (kst.getUTCMonth() + 1) * 100 + kst.getUTCDate();
  return ((seed % 6) + 6) % 6;
}
