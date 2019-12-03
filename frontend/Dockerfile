FROM node:alpine as build

LABEL maintainer="vilhelm@prytznet.se"

WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH

COPY package.json /app/package.json
RUN npm install --silent

COPY . /app
RUN npm run build

FROM nginx:alpine
RUN echo 'server_tokens off;' > /etc/nginx/conf.d/server_tokens.conf
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]