FROM python:3.7

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 5001


CMD echo "[fixed_endpoint_parser]" > config.ini && \ 
    echo "host=$PARSER_HOSTNAME" >> config.ini && \ 
    echo "port=$PARSER_PORT" >> config.ini && \
    echo "[fixed_endpoint_planner]" >> config.ini && \
    echo "host=$PLANNER1_HOSTNAME" >> config.ini && \
    echo "port=$PLANNER1_PORT" >> config.ini && \
    echo "[fixed_endpoint_planner2]" >> config.ini && \
    echo "host=$PLANNER2_HOSTNAME" >> config.ini && \
    echo "port=$PLANNER2_PORT" >> config.ini && \
    python3 __main__.py
