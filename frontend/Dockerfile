ARG NODE_IMAGE=node:20-alpine

FROM ${NODE_IMAGE} AS builder
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci 2>/dev/null || npm install
COPY . .
ARG NEXT_PUBLIC_API_URL=http://localhost:8000
ARG API_REWRITE_TARGET=http://backend:8000
ARG MINIO_REWRITE_TARGET=http://minio:9000
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV API_REWRITE_TARGET=$API_REWRITE_TARGET
ENV MINIO_REWRITE_TARGET=$MINIO_REWRITE_TARGET
RUN npm run build

FROM ${NODE_IMAGE} AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
EXPOSE 3000
ENV PORT=3000
ENV HOSTNAME=0.0.0.0
CMD ["node", "server.js"]
