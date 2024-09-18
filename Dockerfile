FROM linuxserver/ffmpeg as ffmpeg
FROM dpokidov/imagemagick as imagemagick


FROM nikolaik/python-nodejs:python3.11-nodejs20 as base
RUN mkdir -p /opt/app && chown pn:pn /opt/app

USER root
 

RUN python -m venv /opt/app/venv
ENV PATH="/opt/app/venv/bin:$PATH"
ENV DOCKER sdfsese
# Copy SSH key
RUN mkdir /root/.ssh
COPY .ssh /root/.ssh
RUN chmod 600 /root/.ssh/id_rsa
COPY  requirements.txt .
COPY /api  /app/
RUN pip install   -r requirements.txt
FROM base AS deps
 
# Check https://github.com/nodejs/docker-node/tree/b4117f9333da4138b03a546ec926ef50a31506c3#nodealpine to understand why libc6-compat might be needed.
WORKDIR /app
 
# Install dependencies based on the preferred package manager
COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* ./
RUN \
  if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
  elif [ -f package-lock.json ]; then npm ci; \
  elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm i --frozen-lockfile; \
  else echo "Lockfile not found." && exit 1; \
  fi
# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
# Next.js collects completely anonymous telemetry data about general usage.
# Learn more here: https://nextjs.org/telemetry
# Uncomment the following line in case you want to disable telemetry during the build.
ENV NEXT_TELEMETRY_DISABLED 1

RUN \
  if [ -f yarn.lock ]; then yarn run build; \
  elif [ -f package-lock.json ]; then npm run build; \
  elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm run build; \
  else echo "Lockfile not found." && exit 1; \
  fi

# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_RUNTIME docker
# Uncomment the following line in case you want to disable telemetry during runtime.
# ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs


# Set the correct permission for prerender cache
RUN mkdir .next
RUN chown nextjs:nodejs .next

# Automatically leverage output traces to reduce image size
# https://nextjs.org/docs/advanced-features/output-file-tracing
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
COPY --from=builder /app/public ./public
RUN  apt-get clean
RUN apt-get update
RUN apt-get install -y ffmpeg libpng-dev libjpeg-dev libtiff-dev imagemagick ghostscript
RUN apt-get update && apt-get install -y wget && \
    apt-get install -y autoconf pkg-config

RUN apt-get update && apt-get install -y wget && \
    apt-get install -y build-essential curl libpng-dev && \
    wget https://github.com/ImageMagick/ImageMagick/archive/refs/tags/7.1.0-31.tar.gz && \
    tar xzf 7.1.0-31.tar.gz && \
    rm 7.1.0-31.tar.gz && \
    apt-get clean && \
    apt-get autoremove
COPY --from=imagemagick /usr/local/bin/magick /usr/local/bin/magick
COPY --from=imagemagick /usr/local/lib/ /usr/local/lib/
RUN    apt-get install -y ghostscript gsfonts
    
    
USER root

EXPOSE 8080
ENV PORT 8080
# set hostname to localhost
ENV HOSTNAME "localhost"

# server.js is created by next build from the standalone output
# https://nextjs.org/docs/pages/api-reference/next-config-js/output
CMD ["node", "server.js"]