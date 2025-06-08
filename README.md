$ docker compose up --build -d   (-d  をつけると他のコマンドを)
-> コンテナの立ち上げ(docker-composes.yml)

$ docker-compose restart

$ docker exec -it app /bin/sh
-> コンテナ内に入る(shellを実行)

$ docker-compose down
-> containerの削除

~ Docker containerの削除
(base) keshi@kei-MacBook-Pro ss2312 % docker ps -a 
CONTAINER ID   IMAGE        COMMAND                   CREATED         STATUS                       PORTS     NAMES
a7740e990fa3   httpd        "httpd-foreground"        3 minutes ago   Exited (0) 2 minutes ago               festive_franklin
8d5c8ca6c3fa   ss2312-app   "docker-entrypoint.s…"   8 minutes ago   Exited (137) 2 minutes ago             app
(base) keshi@kei-MacBook-Pro ss2312 % docker rm a7740e990fa3
a7740e990fa3

$ docker container logs (app)
-> logの確認                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     