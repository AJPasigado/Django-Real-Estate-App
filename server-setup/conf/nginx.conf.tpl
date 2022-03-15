upstream {program_name} {
    server unix:/tmp/{program_name}.sock fail_timeout=0;
}

server {
    listen 80;
    server_name {sub}.{domain}.{com};

    error_log /opt/{project_folder}/logs/nginx_error.log;
    access_log /opt/{project_folder}/logs/nginx_access.log;

    client_max_body_size 150m;  # adjust as needed by the project
    client_header_timeout 120s;  # adjust as needed by the project

    location / {
        try_files $uri @proxy_to_{program_name};
    }

    location /static/ {
        alias /opt/{project_folder}/dashboard-metrics/static/;
    }

    location /media/ {
        alias /opt/{project_folder}/dashboard-metrics/media/;
    }

    location @proxy_to_{program_name} {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
        proxy_connect_timeout 1200;
        proxy_read_timeout 1200;
        proxy_send_timeout 1200;
        proxy_pass http://{program_name};
    }
}
