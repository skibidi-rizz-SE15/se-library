FROM python:3.12

ENV REDIS_URL=redis://redis PYTHONUNBUFFERED=1
ENV GOOGLE_MAPS_API=[MY_API_KEY]

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]