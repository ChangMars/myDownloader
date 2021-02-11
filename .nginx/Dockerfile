FROM nginx:latest

RUN mkdir /etc/nginx/sites-enabled
RUN mkdir /etc/nginx/sites-available/

COPY nginx.conf /etc/nginx/nginx.conf
COPY my_nginx.conf /etc/nginx/sites-available/

RUN ln -s /etc/nginx/sites-available/my_nginx.conf /etc/nginx/sites-enabled/

CMD ["nginx", "-g", "daemon off;"]