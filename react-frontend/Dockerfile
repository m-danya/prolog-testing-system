FROM node:18.12.1-alpine
WORKDIR /app
COPY package.json /app/package.json
RUN npm install
COPY . /app
EXPOSE 443
CMD export PORT=443 && npm start