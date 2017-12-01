# MJ_LLC

使用Docker Run啟動服務流程

使用Dockerfile建立 tag_api:1.0 及 recommand_api:1.0 image
docker build -t get_tag_value_api:1.0 .
docker build -t get_offer_api:1.0 ./Offer
下載最新版本的redis
docker run -itd --name redis redis:latest
下載Postgresql並修改其環境變數
docker run -itd --name postgres -e POSTGRES_PASSWORD=  postgres:latest
啟用Tag Server
docker run -it --name tagserver -p 6004:80 --link redis:redis --link postgres:postgres tagserver:1.0
啟用Recommand System
docker run -it --name recommend -p 6003:80 --link tagserver:tagserver --link redis:redis --link postgres:postgres recommend:1.0
