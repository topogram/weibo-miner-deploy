server {
    listen 80;
    server_name     {{ domain }};
    root            {{ root }};

    access_log      {{ log }}/nginx.access.log;
    error_log       {{ log }}/nginx.error.log;

    location / {
        proxy_pass http://{{ domain }}:{{port}};
        proxy_redirect off;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
            alias           {{ static }};
    }

    location /socket.io {
        proxy_pass http://{{ domain }}:{{port}}/socket.io;
        proxy_redirect off;
        proxy_buffering off;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
    }
}
