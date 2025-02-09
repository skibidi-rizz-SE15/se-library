FROM python:3.12


ENV REDIS_URL=redis://redis PYTHONUNBUFFERED=1
ENV GOOGLE_MAPS_API=[YOUR_API_KEY]

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt


ENTRYPOINT ["reflex", "run", "--env", "prod", "--backend-only", "--loglevel", "debug" ]
