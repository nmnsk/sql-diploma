FROM python:3.10

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

#USER runner
#WORKDIR /code
RUN chmod +x docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT [ "/docker-entrypoint.sh" ]