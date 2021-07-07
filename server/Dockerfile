FROM node:14.16.0

WORKDIR /app

COPY ./src/package.json ./

RUN npm i

COPY ./src/ ./

ENTRYPOINT ["npm", "run"]
CMD ["start"]