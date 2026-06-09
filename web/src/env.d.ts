/// <reference types="astro/client" />

declare namespace App {
  interface Locals {
    // 미들웨어가 세션에서 해석한 로그인 사용자. 미인증이면 null.
    user: import('./lib/auth.ts').User | null;
  }
}
