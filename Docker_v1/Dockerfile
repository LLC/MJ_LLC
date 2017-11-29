FROM python:2
MAINTAINER LLC <d40614d@gmail.com>
COPY . /src
WORKDIR /src
RUN pip install -r requirements.txt
EXPOSE 80
#CMD python api_assist.py && python sort_offer_function.py && python get_tag_value_api.py && get_offer_api.py
CMD python create_table.py && python api_assist.py && python get_tag_value_api.py
#CMD python get_tag_value_api.py


# docker build -t get_tag_value_api:1.0 .
# docker build -t get_offer_api:1.0 .
# docker run -itd --name redis redis:latest
# docker run -itd --name postgres -e POSTGRES_PASSWORD=  postgres:latest
# docker run -it --name tagserver -p 6000:80 --link redis:redis --link postgres:postgres get_tag_value_api:1.0
# docker run -it --name recommend -p 6003:80 --link tagserver:tagserver --link redis:redis --link postgres:postgres get_offer_api:1.0






# docker build -t get_offer_api:1.0 ./RecommandSystem
# docker run -itd --name postgres -e POSTGRES_PASSWORD=lukechen0419 -d postgres
# docker run -it --name tagserver --link redis:redis --link postgres:postgres tag_api:1.0