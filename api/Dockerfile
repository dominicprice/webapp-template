FROM python:3.13-slim

ARG API_VERSION
WORKDIR /wheel
COPY dist/api-${API_VERSION}-py3-none-any.whl .

RUN pip install api-${API_VERSION}-py3-none-any.whl

EXPOSE 8000

CMD [ "api" ]