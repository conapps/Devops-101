FROM nginx
ADD ./parametros/webserver2_nginx.conf /parametros/webserver2_nginx.conf
ADD ./parametros/uwsgi_params /parametros/uwsgi_params
RUN ln -s /parametros/webserver2_nginx.conf /etc/nginx/conf.d/webserver2_nginx.conf 

