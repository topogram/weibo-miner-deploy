server {
        listen          80;
        server_name     {{ domain }};
        root            {{ root }};
 
        access_log      {{ root }}/access.log;
        error_log       {{ root }}/error.log;
 
        location / {
                uwsgi_pass      unix:///{{ root }}/uwsgi.sock;
                include         uwsgi_params;
        }
 
        location /static {
                alias           {{ root }}/{{ static }};
        }
}
