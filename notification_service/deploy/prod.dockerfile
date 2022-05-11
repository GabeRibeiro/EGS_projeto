# Common build stage
FROM node:16-alpine

WORKDIR /app

# Copy project files required for building
COPY package*.json tsconfig.json tslint.json /app/
#copy source code
COPY ./src /app/src

#install dependencies, build code and prune dependencies inline as to save layer size
RUN npm ci && npm run build && npm prune --production

ENV NODE_ENV production

CMD ["npm", "run", "prod"]