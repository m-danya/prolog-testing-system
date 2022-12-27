FROM node:18.12.1-alpine
WORKDIR /app
COPY package.json /app/package.json
RUN npm install --only=prod
COPY . /app
RUN npm run build
EXPOSE 443
CMD export PORT=443 && npm start