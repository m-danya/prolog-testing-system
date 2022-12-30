FROM node:18.12.1-alpine
WORKDIR /app
COPY package.json /app/package.json
RUN npm install
COPY . /app
EXPOSE ${FRONTEND_PORT}
CMD export PORT=${FRONTEND_PORT} && npm start