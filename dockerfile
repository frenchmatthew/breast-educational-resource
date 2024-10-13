FROM node:16-alpine

WORKDIR /app

COPY frontend  .

RUN yarn \
    && yarn generate 


ENV PORT 3158  

EXPOSE 3158    

CMD ["yarn", "start"]