ARG NODE_VERSION=24.13.1

FROM node:${NODE_VERSION}-alpine3.23 AS base

WORKDIR /usr/src/app

RUN corepack enable \
    && corepack prepare pnpm@10.30.0 --activate

FROM base AS deps

COPY src/package.json ./

COPY src/pnpm-lock.yaml ./

RUN pnpm install --frozen-lockfile

FROM deps AS build

COPY src/ ./

RUN pnpm run generate

FROM nginx:1.29.5-alpine3.23 AS prod

COPY .deploy/docker/nginx/conf /etc/nginx/

COPY --from=build /usr/src/app/.output/public /var/www/html
