// 관리자(어드민) 식별 — 이메일 allowlist 기반.
// DB 컬럼 대신 allowlist 를 쓰는 이유: 마이그레이션 불필요, DB 리셋·재가입과 무관하게
// 항상 결정적이며, 사장님 계정이 실수로 admin 권한을 잃는 사고를 원천 차단한다.
//
// 기본 관리자 = 사장님 계정. 추가 관리자는 env 로:
//   MATH_STUDY_ADMIN_EMAILS=a@x.com,b@y.com   (콤마 구분, env 지정 시 기본값 대체)
const DEFAULT_ADMIN_EMAILS = ['hwangi0404@gmail.com'];

const ADMIN_EMAILS = new Set(
  (process.env.MATH_STUDY_ADMIN_EMAILS
    ? process.env.MATH_STUDY_ADMIN_EMAILS.split(',')
    : DEFAULT_ADMIN_EMAILS
  )
    .map((e) => e.trim().toLowerCase())
    .filter(Boolean),
);

export function isAdminEmail(email: string | null | undefined): boolean {
  return !!email && ADMIN_EMAILS.has(email.toLowerCase());
}
