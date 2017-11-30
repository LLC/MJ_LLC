FROM python:2
MAINTAINER LLC <d40614d@gmail.com>
COPY . /src
WORKDIR /src
RUN pip install -r require.txt
EXPOSE 80
CMD python get_offer_api.py