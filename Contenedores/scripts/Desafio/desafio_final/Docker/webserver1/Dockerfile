FROM nginx
ADD ./parametros/webserver1_nginx.conf /parametros/webserver1_nginx.conf
ADD ./parametros/uwsgi_params /parametros/uwsgi_params
RUN ln -s /parametros/webserver1_nginx.conf /etc/nginx/conf.d/webserver1_nginx.conf 

