FROM node:18.12.1-alpine
WORKDIR /app
COPY package.json /app/package.json
RUN npm install --only=prod
COPY . /app
RUN npm run build
EXPOSE 80
CMD export PORT=80 && npm start