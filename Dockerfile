version: '2'

services:
  app:
    build: .
    image: app
    volumes:
      - /app

  web:
    restart: on-failure
    image: app
    command: bash ./scripts/web.sh
    env_file: .env
    links:
     - redis
    expose:
      - "8000"
    ports:
      - "127.0.0.1:8000:8000"
    depends_on:
      - app
      - redis

  worker:
    restart: on-failure
    image: app
    command: bash ./scripts/worker.sh
    env_file: .env
    links:
     - redis
    depends_on:
      - app
      - redis

  beat:
    restart: on-failure
    image: app
    command: bash ./scripts/beat.sh
    env_file: .env
    links:
     - redis
    depends_on:
      - app
      - redis

  redis:
    image: redis
    expose:
      - "6379"

  flower:
    restart: 'no'
    image: app
    env_file: .env
    ports:
      - 5555:5555
    depends_on:
      - worker
      - redis
