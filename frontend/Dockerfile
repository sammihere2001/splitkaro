# Image for the React frontend, built in two stages.

# ---- Stage 1: build the app with Node ----
FROM node:24-alpine AS build
WORKDIR /app

# Same caching trick as the backend: install packages before copying the source code.
COPY package.json package-lock.json ./
RUN npm ci

COPY . .

# Vite bakes the API address into the JavaScript at build time, so it is a build argument.
ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

# ---- Stage 2: serve the built files with nginx ----
# Only the finished files from stage 1 are copied over. Node and node_modules are left behind,
# so the final image is tiny.
FROM nginx:stable-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
