FROM node:18

WORKDIR /app

COPY . .

RUN npm install

# BAD: running as root
USER root

CMD ["node", "index.js"]
