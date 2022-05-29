source .env \
&& touch ${sqlite_path} \
&& docker-compose up --build -d