// 「오늘의 페이지」 히어로 '장식' 곡선 계열(6종). 곡선은 장식일 뿐 — '오늘의 개념'은
// 별도(daily-concept.mjs, 전체 개념 풀에서 매일 새로 고름)다.
// ★ 곡선 모양은 정준(canonical) 고정 — 진폭·주기·표준편차를 흔들면 정규분포 등이 왜곡되므로
//   흔들지 않는다(사용자 지침). 계열만 curveIndexForMs(연속 일수%N)로 매일 바뀐다.
// ★ curveSeedForMs 는 이제 PaperHero 의 연필 wobble(손그림 질감)에만 쓰인다(모양 불변).
// label 은 PaperHero buildScene 의 label 과 동일하게 유지. concept/blurb 필드는 옛 결합의
// 잔재(현재 미사용) — 곡선↔개념 결합은 폐지됨.

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

// KST 연속 일수(자정마다 +1). 계열 선택·파라미터 시드의 단일 기준.
// 옛 YYYYMMDD 는 달 경계에서 점프해 어제와 같은 곡선이 나올 수 있었음 → 연속 일수로 교체.
export function kstEpochDay(nowMs) {
  return Math.floor((nowMs + 9 * 3600 * 1000) / 86400000);
}

// 그날의 곡선 '계열' index — 연속 일수 % N. 매일 한 칸씩 깔끔히 순환(달 경계 점프 없음).
// PaperHero 와 index.astro 가 이 함수를 공유해 그림·캡션이 항상 같은 계열을 가리킨다.
export function curveIndexForMs(nowMs) {
  const n = DAILY_CURVES.length;
  return ((kstEpochDay(nowMs) % n) + n) % n;
}

// 그날의 시드 — PaperHero 의 연필 wobble(손그림 질감) 전용. 곡선 모양은 안 바뀌고 질감만
// 미세하게 매일 달라진다. 연속 일수를 잘 섞어(Knuth multiplicative) mulberry32 입력으로 쓴다.
export function curveSeedForMs(nowMs) {
  const d = kstEpochDay(nowMs) | 0;
  return (Math.imul(d, 2654435761) ^ 0x9e3779b9) >>> 0;
}
