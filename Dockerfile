FROM python:3.6-slim

ENV BACKEND_PATH /app
ENV WEB_PATH ${BACKEND_PATH}/src

WORKDIR ${BACKEND_PATH}

RUN pip install --upgrade pip
ADD . ${BACKEND_PATH}
RUN pip install -r src/requirements.txt

WORKDIR ${WEB_PATH}

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "fileshare.wsgi"]