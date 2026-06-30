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
# ★문제 이미지: web/public/problem-images/*.png 4천여 개가 ../../../db/raw 로 가는 심링크다.
#   런타임 이미지엔 db/(872M)를 안 넣으므로 빌드 단계에서 db 를 복사해 심링크를 실파일로 풀어 박는다
#   (깨진 심링크는 제거). 그래야 runner 가 public 만 복사해도 문제 이미지가 서빙된다.
COPY db ./db
RUN set -e; cd /app/web/public/problem-images && for l in *; do \
      if [ -L "$l" ]; then t="$(readlink -f "$l")"; \
        if [ -f "$t" ]; then cp --remove-destination "$t" "$l"; else rm -f "$l"; fi; \
      fi; done

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
 && apt-get install -y --no-install-recommends python3 python3-venv curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /app/.venv \
 && /app/.venv/bin/pip install --no-cache-dir --upgrade pip \
 && /app/.venv/bin/pip install --no-cache-dir "sympy>=1.14"

# 비루트 실행(node:22-slim 내장 node 유저). ★앱 코드보다 *먼저* claude CLI 를 설치해 레이어 캐시:
#   소스만 바뀌는 재빌드에선 이 레이어가 캐시 적중 → claude 재다운로드 안 함.
# ★튜터(chat.ts)가 spawn 하는 claude CLI(네이티브). 구독 인증(~/.claude)은 *런타임 마운트*(시크릿
#   미베이크). 캐싱은 chat.ts 의 CLEAN_DIR+DISABLE_GIT 담당 → 컨테이너서도 유지. [[project_claude_p_caching]]
USER node
RUN curl -fsSL https://claude.ai/install.sh | bash
ENV PATH="/home/node/.local/bin:${PATH}"

# 런타임 산출물 복사 — 소유권을 COPY 시점에 지정(--chown)해 별도 `chown -R /app`(이전 5.5분!) 제거.
WORKDIR /app/web
COPY --chown=node:node --from=builder /app/web/dist ./dist
COPY --chown=node:node --from=builder /app/web/node_modules ./node_modules
COPY --chown=node:node --from=builder /app/web/package.json ./package.json
COPY --chown=node:node --from=builder /app/web/public ./public

EXPOSE 8080

# 컨테이너 헬스체크(PaaS 자체 프로브와 별개로 docker 레벨에서도 점검).
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD node -e "fetch('http://127.0.0.1:'+(process.env.PORT||8080)+'/api/health').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"

# @astrojs/node standalone 엔트리.
CMD ["node", "./dist/server/entry.mjs"]

# ─────────────────────────────────────────────────────────────
# 3) dev — 즉시 반영(astro dev + HMR). 소스/콘텐츠/db 는 런타임 바인드마운트(compose.dev),
#    node_modules 는 named volume. 앱코드를 굽지 않으므로 git pull 만 하면 HMR 로 바로 반영
#    (재빌드 불필요 = laptop 과 동일). ★프로덕션 아님 — 단일 사용자 프리런치 반복용.
# ─────────────────────────────────────────────────────────────
FROM node:22-slim AS dev
ENV NODE_ENV=development HOST=0.0.0.0 PORT=8080 HOME=/root
RUN apt-get update \
 && apt-get install -y --no-install-recommends python3 python3-venv curl ca-certificates git openssh-client \
 && rm -rf /var/lib/apt/lists/*
# sympy(api/sympy.ts) — /app/.venv 는 /app/web 만 바인드하므로 가려지지 않는다.
RUN python3 -m venv /app/.venv \
 && /app/.venv/bin/pip install --no-cache-dir --upgrade pip \
 && /app/.venv/bin/pip install --no-cache-dir "sympy>=1.14"
# 튜터 claude CLI(루트 설치 → /root/.claude 마운트로 인증). 캐싱은 chat.ts CLEAN_DIR+DISABLE_GIT.
RUN curl -fsSL https://claude.ai/install.sh | bash
ENV PATH="/root/.local/bin:${PATH}"
WORKDIR /app/web
# node_modules(named volume)가 비어 있으면 npm ci 후 astro dev. 이후 기동은 캐시 → 빠름.
CMD ["sh","-c","[ -e node_modules/astro ] || npm ci; exec npm run dev -- --host 0.0.0.0 --port 8080"]
