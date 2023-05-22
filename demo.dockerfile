FROM postgres:15

COPY demo_small.sql .

#ADD demo_small.sql /docker-entrypoint-initdb.d

#RUN psql -f demo_small.sql -U postgres
