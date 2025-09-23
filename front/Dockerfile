####################################################
################### BASE IMAGE #####################
####################################################

FROM node:24.7.0-alpine AS base

WORKDIR /app

####################################################
############### INSTALL DEPENDENCIES ###############
####################################################

FROM base AS deps

COPY package*.json ./

RUN npm ci --omit=dev --prefer-offline --no-audit

####################################################
#################### BUILD APP #####################
####################################################

FROM base AS builder

COPY --from=deps /app/node_modules ./node_modules

COPY . .

RUN npm run build

####################################################
###################### FINAL #######################
####################################################

FROM base AS runner

# COPY --from=deps /app/node_modules ./node_modules

COPY --from=builder /app/.output ./.output

COPY package*.json ./

RUN addgroup -g 1001 -S nodejs && \
    adduser -S nuxtuser -u 1001 && \
    chown -R nuxtuser:nodejs /app

USER nuxtuser

EXPOSE 3000

ENV NODE_ENV=production
ENV HOST=0.0.0.0
ENV PORT=3000

CMD ["node", ".output/server/index.mjs"]
