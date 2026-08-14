// 검수 화면에서 찾은 카메라 각도를 스펙에 저장한다 — **어드민 전용, dev 도구**.
//
// ★왜 필요한가: 좋은 각도는 드래그로 찾는 게 제일 빠른데, 찾은 값을 스펙에 옮겨 적을
//   길이 없었다. 좌표가 완벽해도 각도가 나쁘면 도형이 안 보인다(2026-08-14: 접은 반원
//   평면의 법선과 시선이 거의 수직이라 반원이 선분 위에 겹쳐 사라졌다).
//
// ⚠️ **cameraPosition 만** 쓴다. 좌표·conditions·verify 는 sympy 로 검증된 값이라
//    이 경로로 절대 건드리지 않는다.
import type { APIRoute } from 'astro';
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { FIGURES_3D_DIR } from '../../../lib/figures-3d';

export const prerender = false;

const ok = (v: unknown): v is [number, number, number] =>
  Array.isArray(v) && v.length === 3 && v.every((n) => typeof n === 'number' && Number.isFinite(n));

export const POST: APIRoute = async ({ request, locals }) => {
  const user = (locals as { user?: { is_admin?: boolean } }).user;
  if (!user?.is_admin) return new Response('forbidden', { status: 403 });

  let body: { stem?: string; cameraPosition?: unknown; cameraTarget?: unknown };
  try { body = await request.json(); }
  catch { return new Response('bad json', { status: 400 }); }

  const stem = String(body.stem ?? '');
  // 경로 조작 차단 — stem 은 파일명 한 조각이어야 한다.
  if (!stem || stem.includes('/') || stem.includes('..')) return new Response('bad stem', { status: 400 });
  if (!ok(body.cameraPosition)) return new Response('bad cameraPosition', { status: 400 });

  const path = join(FIGURES_3D_DIR, `${stem}.json`);
  if (!existsSync(path)) return new Response('not found', { status: 404 });

  const e = JSON.parse(readFileSync(path, 'utf-8'));
  if (!e?.spec?.shapes || !e.conditions || !e.verify) {
    return new Response('spec 구조가 예상과 다르다 — 쓰지 않음', { status: 409 });
  }
  e.spec.cameraPosition = body.cameraPosition;
  // 회전 중심은 선택 — 안 주면 기존 값을 지운다(바운딩 박스 중심으로 되돌아간다).
  if (ok(body.cameraTarget)) e.spec.cameraTarget = body.cameraTarget;
  else delete e.spec.cameraTarget;
  writeFileSync(path, JSON.stringify(e, null, 1), 'utf-8');
  return new Response(JSON.stringify({ ok: true, cameraPosition: e.spec.cameraPosition, cameraTarget: e.spec.cameraTarget ?? null }), {
    headers: { 'Content-Type': 'application/json' },
  });
};
