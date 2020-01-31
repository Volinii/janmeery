upstream janmeery  {
    server janmeery:8000;
}
 
server {
    server_name  janmeery.cn;
 
    location /static {
        alias /apps/janmeery/static;
    }
 
    location / {
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
 
        proxy_pass http://janmeery;
    }
 
    listen 80;
}