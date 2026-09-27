FROM node:22-alpine AS build
WORKDIR /app
COPY package.json package-lock.json tsconfig.json ./
RUN npm ci
COPY src ./src
RUN npm run build && npm prune --omit=dev

FROM node:22-alpine
WORKDIR /app
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
COPY package.json ./
RUN mkdir -p /workspace && chown node:node /workspace
USER node
ENV DC_TRANSPORT=http \
    DC_HTTP_HOST=0.0.0.0 \
    DC_HTTP_PORT=3000 \
    DC_ALLOWED_DIRECTORIES=/workspace
EXPOSE 3000
HEALTHCHECK CMD wget -qO- http://127.0.0.1:3000/health || exit 1
CMD ["node", "dist/index.js"]
