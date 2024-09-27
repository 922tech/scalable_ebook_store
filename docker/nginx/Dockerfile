FROM nginx:1.19-alpine

MAINTAINER Niayesh Sadeghi <niayesh.sadeghi@gmail.com>

ENV TZ=Asia/Tehran
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN rm /etc/nginx/conf.d/default.conf
COPY *.conf /etc/nginx/
COPY conf.d/* /etc/nginx/conf.d/

RUN  mkdir /static_pages
COPY error.html /static_pages/error.html
