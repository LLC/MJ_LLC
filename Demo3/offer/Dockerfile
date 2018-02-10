FROM python:2
MAINTAINER LLC <d40614d@gmail.com>
COPY . /src
WORKDIR /src
RUN pip install -r require.txt
EXPOSE 80
CMD sleep 10 && python sort_offer_function.py && python get_offer_api.py
