# math-study — Astro (node standalone adapter) 프로덕션 이미지.
#
# ★빌드 컨텍스트는 반드시 레포 루트여야 한다(web/ 가 아님):
#     docker build -f web/Dockerfile -t math-study .
#   이유: web/package.json 의 prebuild(build-concept-hubs 등)가 ../docs 를 읽고,
#   web/astro.config.mjs 도 ../docs/concepts 를 읽는다. web/ 만 컨텍스트로 주면
#   docs/ 가 없어 빌드가 깨진다.
#   Railway/Render 의 Dockerfile 배포는 기본적으로 레포 루트를 컨텍스트로 잡으므로
#   Dockerfile Path = web/Dockerfile 로만 지정하면 된다.
#
# Node 22 고정: web/package.json engines.node ">=22.12.0".

# ─────────────────────────────────────────────────────────────
# 1) builder — npm ci + astro build (정적/SSR 번들 산출)
# ─────────────────────────────────────────────────────────────
FROM node:22-slim AS builder
WORKDIR /app

# 의존성 레이어 캐시: lockfile 먼저 복사 → 소스 변경 시에도 npm ci 재실행 회피.
COPY web/package.json web/package-lock.json* ./web/
WORKDIR /app/web
RUN npm ci

# 소스 + 빌드가 읽는 docs(개념/문제 마크다운, 자산) 복사.
WORKDIR /app
COPY web ./web
COPY docs ./docs

# prebuild(허브/그래프/인덱스 생성 + LWIP 감사) → astro build.
WORKDIR /app/web
RUN npm run build

# ─────────────────────────────────────────────────────────────
# 2) runner — 슬림 런타임. node 산출물 + python3/sympy(api/sympy.ts 의존).
# ─────────────────────────────────────────────────────────────
FROM node:22-slim AS runner
ENV NODE_ENV=production
# @astrojs/node standalone 은 HOST/PORT env 를 네이티브로 읽는다.
ENV HOST=0.0.0.0
ENV PORT=8080

# api/sympy.ts 는 ../.venv/bin/python 을 spawn 한다(런타임 cwd=/app/web → /app/.venv).
# python3 + sympy 를 전용 venv 에 설치(시스템 파이썬 오염 없이 경로 고정).
RUN apt-get update \
 && apt-get install -y --no-install-recommends python3 python3-venv \
 && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /app/.venv \
 && /app/.venv/bin/pip install --no-cache-dir --upgrade pip \
 && /app/.venv/bin/pip install --no-cache-dir "sympy>=1.14"

# 런타임에 필요한 것만 복사: 빌드 산출물 + 프로덕션 node_modules + 정적 public.
WORKDIR /app/web
COPY --from=builder /app/web/dist ./dist
COPY --from=builder /app/web/node_modules ./node_modules
COPY --from=builder /app/web/package.json ./package.json
COPY --from=builder /app/web/public ./public

# 비루트 실행(node:22-slim 에 내장된 node 유저).
RUN chown -R node:node /app
USER node

EXPOSE 8080

# 컨테이너 헬스체크(PaaS 자체 프로브와 별개로 docker 레벨에서도 점검).
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD node -e "fetch('http://127.0.0.1:'+(process.env.PORT||8080)+'/api/health').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"

# @astrojs/node standalone 엔트리.
CMD ["node", "./dist/server/entry.mjs"]
