FROM python:3.10 AS build

LABEL name="httpbin"
LABEL version="0.1.0"
LABEL description="My Awesome Project!"

WORKDIR /app

ADD . .

RUN pip install -U pip && \
    pip install -U poetry && \
    poetry install && \
    poetry build -f wheel


FROM python:3.10

LABEL name="httpbin"
LABEL version="0.1.0"
LABEL description="My Awesome Project!"

COPY --from=build /app/dist/*.whl /tmp

RUN pip install --no-cache-dir -U pip && \
    pip install /tmp/*.whl

CMD ["httpbin", "run"]