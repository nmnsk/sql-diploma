FROM python:3.10

WORKDIR /code

COPY . .
RUN pip3 install pip-tools

RUN pip3 install --no-cache-dir -r requirements.txt

RUN chmod +x docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT [ "sh", "docker-entrypoint.sh" ]