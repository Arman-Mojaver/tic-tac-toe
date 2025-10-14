FROM python:3.13
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN mkdir /code
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt
COPY . /code/
RUN chmod +x /code/entrypoint.sh
RUN pip install -e . || true
EXPOSE 8000
ENTRYPOINT ["/bin/sh", "/code/entrypoint.sh"]
