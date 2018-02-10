FROM python:2
MAINTAINER LLC <d40614d@gmail.com>
COPY . /src
WORKDIR /src
RUN pip install -r requirements.txt
EXPOSE 80
CMD sleep 10 && python create_table.py && python api_assist.py && python get_tag_value_api.py


# docker run -itd --name redis redis:latest
# docker run -itd --name postgres -e POSTGRES_PASSWORD=  postgres:latest
# docker build -t tagserver:1.0 ./Demo3
# docker build -t recommend:1.0 ./Demo3/offer
# docker run -it --name tagserver -p 6004:80 --link redis:redis --link postgres:postgres tagserver:1.0
# docker run -it --name recommend -p 6003:80 --link tagserver:tagserver --link redis:redis --link postgres:postgres recommend:1.0
